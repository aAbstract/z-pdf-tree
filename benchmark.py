import os
import json
from glob import glob
from zpdf import *


def generate_benchmark(file_paths: list[str]) -> tuple[dict, float, list]:
    agg_score = 0
    benchmark = {}
    files_to_check = []
    for file_path in file_paths:
        print('Parsing:', file_path)
        zpdf = ZPDF(file_path=file_path)

        with open(f"cache/{file_path.replace('data/', '').replace('.pdf', '')}_cache.json", 'w') as f:
            f.write(json.dumps(zpdf.get_cache(), indent=2))

        _benchmark = zpdf.get_benchmark()
        if _benchmark['coverage_metric'] != 1.0 or _benchmark['untitled_labels_count'] != 0 or _benchmark['link_gap_count'] != 0:
            files_to_check.append(file_path)

        benchmark[file_path] = _benchmark
        agg_score += _benchmark['coverage_metric']
    return benchmark, (agg_score / len(file_paths)), files_to_check


os.system('rm cache/*.json')
sample_file_paths = glob('data/*.pdf')
benchmark, agg_score, files_to_check = generate_benchmark(sample_file_paths)
print(json.dumps(benchmark, indent=2))
print('Benchmarked Files:', len(sample_file_paths))
print('Benchmark Score:', agg_score)
print('Files to Check:', files_to_check)
