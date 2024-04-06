import json
from glob import glob
from z_pdf_tree import *


RXI_TEST_FILE = 'sample_rxi_12'
MAC_TEST_FILE = 'sample_mac_1'


def _check_testbench(z_pdf_map: dict[str, ZPDFTree]) -> bool:
    # load testbench
    with open('data/testbench.json', 'r') as f:
        testbench = json.loads(f.read())

    # bounds testbench
    success_count = 0
    failed_count = 0

    def success_routine(item):
        nonlocal success_count
        print('SUCCESS:', item['file_path'], '-', item['toc_header'])
        success_count += 1

    def failed_routine(item):
        nonlocal failed_count
        print('FAILED:', item['file_path'], '-', item['toc_header'])
        failed_count += 1

    for idx, item in enumerate(testbench):
        print(idx, 'Testing:', item['file_path'], '-', item['toc_header'])
        z_pdf_tree = z_pdf_map[item['file_path']]
        toc_header: str = item['toc_header']
        toc_header_key = toc_header.split(' ')[0]
        toc_tree_node = z_pdf_tree.find_toc_tree_node(toc_header_key)
        if not toc_tree_node:
            failed_routine(item)
            continue
        if toc_tree_node.start_page != item['start_page'] or toc_tree_node.end_page != item['end_page'] or toc_tree_node.end_link_label != item['end_link_label']:
            failed_routine(item)
            continue
        if item['text_file_path']:
            node_text = z_pdf_tree.get_toc_node_text(toc_tree_node)
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


def test_create_cache_file_rxi_sample():
    file_path = f"data/{RXI_TEST_FILE}.pdf"
    z_pdf_tree = ZPDFTree(file_path=file_path, debug=True)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(z_pdf_tree.get_cache(), indent=2))
    assert glob('test_cache.json')


def test_create_cache_file_mac_sample():
    file_path = f"data/{MAC_TEST_FILE}.pdf"
    z_pdf_tree = ZPDFTree(file_path=file_path, debug=True)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(z_pdf_tree.get_cache(), indent=2))
    assert glob('test_cache.json')


def test_testbench():
    # load testbench
    with open('data/testbench.json', 'r') as f:
        testbench = json.loads(f.read())

    # load testbench pdfs
    pdf_paths: set[str] = set(x['file_path'] for x in testbench)
    z_pdf_map: dict[str, ZPDFTree] = {}
    for pdf_path in pdf_paths:
        z_pdf_map[pdf_path] = ZPDFTree(file_path=pdf_path)

    _check_testbench(z_pdf_map)


def test_caching():
    # load testbench
    with open('data/testbench.json', 'r') as f:
        testbench = json.loads(f.read())

    # load testbench pdfs
    pdf_paths: set[str] = set(x['file_path'] for x in testbench)
    z_pdf_map: dict[str, ZPDFTree] = {}
    for pdf_path in pdf_paths:
        cache_path = f"temp/{pdf_path.replace('data/', '').replace('.pdf', '')}_cache.json"
        # load cache file
        with open(cache_path, 'r') as f:
            cache = json.loads(f.read())
        z_pdf_map[pdf_path] = ZPDFTree(file_path=pdf_path, cache=cache)

    _check_testbench(z_pdf_map)


def test_extract_node_text():
    # load cache
    with open(f"temp/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    z_pdf_tree = ZPDFTree(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    # test node text extraction
    toc_tree_node = z_pdf_tree.find_toc_tree_node('8')
    node_text = z_pdf_tree.get_toc_node_text(toc_tree_node)
    with open('node_text.txt', 'w') as f:
        f.write(node_text)
    assert glob('node_text.txt')


def test_extract_text_no_overlap():
    # load cache
    with open(f"temp/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    z_pdf_tree = ZPDFTree(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    # test text extraction no overlap
    toc_keys = ['12', '11.4.1', '10.10', '10.9.2']
    sections = z_pdf_tree.extract_text(toc_keys)
    assert None not in sections
    assert len(sections) == len(toc_keys)


def test_overlaps_filter():
    # load cache
    with open(f"temp/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    z_pdf_tree = ZPDFTree(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    test_set = [
        (['8.1.7', '8.2.3', '8', '8.4'], ['8']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5'], ['1.1', '1.5']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5', '2'], ['1.1', '1.5', '2']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5', '2', '7.4.1', '7.4'], ['1.1', '1.5', '2', '7.4']),
        (['1.1.3', '1.1', '1.5.2', '1.5', '1.1.5', '2', '7.4.1', '7.4', '7.3.2.2'], ['1.1', '1.5', '2', '7.3.2.2', '7.4']),
    ]
    for test_sample in test_set:
        inp, target_out = test_sample
        assert z_pdf_tree._remove_key_overlaps(inp) == target_out


def test_extract_text_overlap():
    # load cache
    with open(f"temp/{RXI_TEST_FILE}_cache.json", 'r') as f:
        cache = json.loads(f.read())
    z_pdf_tree = ZPDFTree(file_path=f"data/{RXI_TEST_FILE}.pdf", cache=cache)

    # test text extraction no overlap
    toc_keys = ['8.1.7', '8.2.3', '8', '8.4']
    sections = z_pdf_tree.extract_text(toc_keys)
    assert None not in sections
    assert len(sections) == 1
    with open('data/8.txt', 'r') as f:
        target_text = f.read()
    assert sections[0] == target_text
