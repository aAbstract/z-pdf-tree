import json
from glob import glob
from zpdf import *


RXI_TEST_FILE = 'sample_rxi_12'
MAC_TEST_FILE = 'sample_mac_1'


def _check_testbench(z_pdf_map: dict[str, ZPDF]) -> bool:
    # load testbench
    with open('data/testbench.json', 'r') as f:
        testbench = json.loads(f.read())

    # bounds testbench
    success_count = 0
    failed_count = 0

    def success_routine(item):
        nonlocal success_count
        print('SUCCESS:', item['file_path'], '-', item['toc_key'])
        success_count += 1

    def failed_routine(item):
        nonlocal failed_count
        print('FAILED:', item['file_path'], '-', item['toc_key'])
        failed_count += 1

    for idx, item in enumerate(testbench):
        print(idx, 'Testing:', item['file_path'], '-', item['toc_key'])
        zpdf = z_pdf_map[item['file_path']]
        toc_key: str = item['toc_key']
        toc_tree_node = zpdf.find_toc_tree_node(toc_key)
        if not toc_tree_node:
            failed_routine(item)
            continue
        if toc_tree_node.start_page != item['start_page'] or toc_tree_node.end_page != item['end_page'] or toc_tree_node.end_tag != item['end_tag']:
            failed_routine(item)
            continue
        if item['text_file_path']:
            node_text = zpdf.get_toc_node_text(toc_tree_node)
            with open(item['text_file_path'], 'r') as f:
                target_node_text = f.read()
            if node_text != target_node_text:
                failed_routine(item)
                continue
        success_routine(item)

    print('Total Testbench Items:', len(testbench))
    print('SUCCESS:', success_count)
    print('FAILED:', failed_count)
    assert failed_count == 0
    assert success_count + failed_count == len(testbench)


def _validate_cache_bounds(cache: dict) -> bool:
    for root_node in cache:
        if len(root_node['children']) == 0:
            return True
        root_link_idx: str = root_node['link_idx']
        first_child_link_idx: str = root_node['children'][0]['link_idx']
        last_child_link_idx: str = root_node['children'][-1]['link_idx']
        if not first_child_link_idx.startswith(root_link_idx) or not last_child_link_idx.startswith(root_link_idx):
            return False
    return True


def test_create_cache_file_rxi_sample():
    file_path = f"data/{RXI_TEST_FILE}.pdf"
    zpdf = ZPDF(file_path=file_path)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(zpdf.get_cache(), indent=2))
    assert glob('test_cache.json')


def test_create_cache_file_mac_sample():
    file_path = f"data/{MAC_TEST_FILE}.pdf"
    zpdf = ZPDF(file_path=file_path)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(zpdf.get_cache(), indent=2))
    assert glob('test_cache.json')


def test_testbench():
    # load testbench
    with open('data/testbench.json', 'r') as f:
        testbench = json.loads(f.read())

    # load testbench pdfs
    pdf_paths: set[str] = set(x['file_path'] for x in testbench)
    z_pdf_map: dict[str, ZPDF] = {}
    for pdf_path in pdf_paths:
        z_pdf_map[pdf_path] = ZPDF(file_path=pdf_path)

    _check_testbench(z_pdf_map)


def test_caching():
    # load testbench
    with open('data/testbench.json', 'r') as f:
        testbench = json.loads(f.read())

    # load testbench pdfs
    pdf_paths: set[str] = set(x['file_path'] for x in testbench)
    z_pdf_map: dict[str, ZPDF] = {}
    for pdf_path in pdf_paths:
        cache_path = f"cache/{pdf_path.replace('data/', '').replace('.pdf', '')}_cache.json"
        # load cache file
        with open(cache_path, 'r') as f:
            cache = json.loads(f.read())
        z_pdf_map[pdf_path] = ZPDF(file_path=pdf_path, cache=cache)

    _check_testbench(z_pdf_map)


def test_extract_node_text():
    # load cache
    with open(f"cache/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    zpdf = ZPDF(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    # test node text extraction
    toc_tree_node = zpdf.find_toc_tree_node('8')
    node_text = zpdf.get_toc_node_text(toc_tree_node)
    with open('node_text.txt', 'w') as f:
        f.write(node_text)
    assert glob('node_text.txt')


def test_extract_text_no_overlap():
    # load cache
    with open(f"cache/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    zpdf = ZPDF(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    # test text extraction no overlap
    toc_keys = ['12', '11.4.1', '10.10', '10.9.2']
    sections = zpdf.extract_text(toc_keys)
    assert None not in sections
    assert len(sections) == len(toc_keys)


def test_overlaps_filter():
    test_set = [
        (['8.1.7', '8.2.3', '8', '8.4'], ['8']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5'], ['1.1', '1.5']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5', '2'], ['1.1', '1.5', '2']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5', '2', '7.4.1', '7.4'], ['1.1', '1.5', '2', '7.4']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5', '2', '7.4.1', '7.4', '7.3.2.2'], ['1.1', '1.5', '2', '7.3.2.2', '7.4']),
    ]
    for test_sample in test_set:
        inp, target_out = test_sample
        assert ZPDF._remove_key_overlaps(inp) == target_out


def test_link_pattern_match():
    test_set = [
        ('1.4.5 CABIN CREW TRAINING SUPERVISOR .............................................................................................. 19   ', ('1.4.5 CABIN CREW TRAINING SUPERVISOR ', '1.4.5')),
        ('1.3.1 DELEGATION OF NOMINATED MANAGEMENT PERSONNEL OF CABIN CREW DEPARTMENT ', ('1.3.1 DELEGATION OF NOMINATED MANAGEMENT PERSONNEL OF CABIN CREW DEPARTMENT ', '1.3.1')),
        ('8.5 CC POSITION B737800 NORMALEMERGENCY DEMONSTRATION ......................................... 85   ', ('8.5 CC POSITION B737800 NORMALEMERGENCY DEMONSTRATION ', '8.5')),
        ('8.18 GALLEYS  B737800 FWD AND AFT GALLEY .................................................................................. 832   ', ('8.18 GALLEYS  B737800 FWD AND AFT GALLEY ', '8.18')),
        ('8.27 B737 EMERGENCY EQUIPMENT CHECKLISTS ................................................................................ 845   ', ('8.27 B737 EMERGENCY EQUIPMENT CHECKLISTS ', '8.27')),
        ('5.2.1 B737 RECURRENT TRAINING ................................................................................................. 522   ', ('5.2.1 B737 RECURRENT TRAINING ', '5.2.1')),
    ]

    for inp, target_out in test_set:
        assert ZPDF._link_pattern_match(inp) == target_out


def test_links_gap_check_by_idx():
    test_set = [
        (['1', '1.1', '1.2', '1.3', '1.4', '2', '2.1', '2.1.1', '2.1.2', '2.1.3', '2.1.4'], []),
        (['1', '1.1', '1.2', '1.3', '1.6', '1.7', '2', '2.1', '2.1.1', '2.1.2', '2.1.3', '2.1.4', '2.1.7'], ['1.4', '1.5', '2.1.5', '2.1.6']),
    ]

    for inp, target_out in test_set:
        assert ZPDF._links_gap_check_by_idx(inp) == target_out


def test_extract_text_overlap():
    # load cache
    with open(f"cache/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    zpdf = ZPDF(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    # test text extraction no overlap
    toc_keys = ['8.1.7', '8.2.3', '8', '8.4']
    sections = zpdf.extract_text(toc_keys)
    assert None not in sections
    assert len(sections) == 1
    with open('data/sample_rxi_12_8.txt', 'r') as f:
        target_text = f.read()
    assert sections[0] == target_text


def test_validate_bounds_using_cache_files():
    cache_file_paths = glob('cache/*.json')
    for cache_file_path in cache_file_paths:
        with open(cache_file_path, 'r') as f:
            cache = json.loads(f.read())
            print('Validating file:', cache_file_path)
            assert _validate_cache_bounds(cache)


def test_terminal_text_extraction():
    with open(f"cache/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    zpdf = ZPDF(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)
    sections = zpdf.extract_text(['14'])
    assert None not in sections
    assert len(sections) == 1
    with open('data/sample_rxi_12_14.txt', 'r') as f:
        target_text = f.read()
    assert sections[0] == target_text


def _test_create_cache_file_function():
    file_path = 'data/sample_mac_6.pdf'
    zpdf = ZPDF(file_path=file_path)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(zpdf.get_cache(), indent=2))
    assert glob('test_cache.json')


def _test_extract_text_function():
    file_name = 'sample_mac_6'
    file_path = f"data/{file_name}.pdf"
    cache_file_path = f"cache/{file_name}_cache.json"
    with open(cache_file_path, 'r') as f:
        cache = json.loads(f.read())
    zpdf = ZPDF(file_path=file_path, cache=cache)
    link_idx = '8.9.3'
    sections = zpdf.extract_text([link_idx])
    with open(f"data/{file_name}_{link_idx}.txt", 'w') as f:
        f.write(sections[0])
