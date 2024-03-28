import json
from glob import glob
from z_pdf_tree import *


def generate_benchmark(file_paths: list[str]) -> tuple[dict, float]:
    agg_score = 0
    benchmark = {}
    for file_path in file_paths:
        print('Parsing:', file_path)
        z_pdf_tree = ZPDFTree(file_path=file_path, debug=True)

        with open(f"temp/{file_path.replace('data/', '').replace('.pdf', '')}_cache.json", 'w') as f:
            f.write(json.dumps(z_pdf_tree.get_cache(), indent=2))

        benchmark[file_path] = z_pdf_tree.get_benchmark()
        agg_score += benchmark[file_path]['coverage_metric']
    return benchmark, (agg_score / len(file_paths))


sample_file_paths = glob('data/*.pdf')
res = generate_benchmark(sample_file_paths)
print(json.dumps(res[0], indent=2))
print('Benchmarked Files:', len(sample_file_paths))
print('Benchmark Score:', res[1])
