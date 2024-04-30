import os
import json
from glob import glob
from zpdf import *


def generate_benchmark(file_paths: list[str]) -> tuple[dict, float]:
    agg_score = 0
    benchmark = {}
    for file_path in file_paths:
        print('Parsing:', file_path)
        zpdf = ZPDF(file_path=file_path)

        with open(f"cache/{file_path.replace('data/', '').replace('.pdf', '')}_cache.json", 'w') as f:
            f.write(json.dumps(zpdf.get_cache(), indent=2))

        benchmark[file_path] = zpdf.get_benchmark()
        agg_score += benchmark[file_path]['coverage_metric']
    return benchmark, (agg_score / len(file_paths))


os.system('rm cache/*.json')
sample_file_paths = glob('data/*.pdf')
res = generate_benchmark(sample_file_paths)
print(json.dumps(res[0], indent=2))
print('Benchmarked Files:', len(sample_file_paths))
print('Benchmark Score:', res[1])
