# ZPDF
## Generic AI Based PDF Content Tree Parser
ZPDF is a python module that converts PDFs into structured data, focusing on extracting and organizing table of contents. It uses fitz for PDF processing and pydantic for validation.  
It also uses LangChain with OpenAI API to do semantic text retrieval for very large PDFs.  
**Key Features:**  
1. Creates searchable TOC links tree
2. Non overlapping text extraction
3. Smart self correction for missing TOC parent links
4. Supports caching
5. Estimated PDF coverage metrics
6. Semantic Text Retrieval - TODO

## Install - TODO

## Future Work
1. [ ] Add install instructions to README.md
2. [ ] Add LangChain integration for advanced semantic text retrieval
3. [ ] Add generic post correction mechanism

## How to Use
### Create ZPDF Object
```python
file_path = 'data/sample_file.pdf'
zpdf = ZPDF(file_path=file_path)
```

### Query TocTreeNode
```python
def find_toc_tree_node(toc_key: str) -> TocTreeNode | None:
  pass

# example
zpdf.find_toc_tree_node('4.2.2')
```

### Create ZPDF Cache
```python
def get_cache() -> list[dict]:
  pass

# example
file_path = 'data/sample_file.pdf'
zpdf = ZPDF(file_path=file_path)
with open('test_cache.json', 'w') as f:
    f.write(json.dumps(zpdf.get_cache(), indent=2))
```

### Load ZPDF Cache
```python
file_path = 'data/sample_file.pdf'
cache_path = 'data/sample_cache.json'
with open(cache_path, 'r') as f:
    cache = json.loads(f.read())
zpdf = ZPDF(file_path=pdf_path, cache=cache)
```

### PDF Text Extraction
```python
# non overlapping extraction
def extract_text(toc_keys: list[str]) -> list[str]:
  pass

# example
# output will only contain chapter 8 text
toc_keys = ['8.1.7', '8.2.3', '8', '8.4']
sections = zpdf.extract_text(toc_keys)

# single node text extraction
def find_toc_tree_node(toc_key: str) -> TocTreeNode | None:
  pass

def get_toc_node_text(node: TocTreeNode) -> str | None:
  pass

# example
toc_tree_node = zpdf.find_toc_tree_node('1.5.2')
zpdf.get_toc_node_text(toc_tree_node)
```

## Testing
### Generate Full Benchmark
```bash
python benchmark.py > cache/benchmark_log.txt
```

### Benchmark Certain PDF File
```python
import json
from zpdf import *


def test_create_cache_file():
    file_path = 'data/sample_rxi_5.pdf'
    zpdf = ZPDF(file_path=file_path, debug=True)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(zpdf.get_cache(), indent=2))
```
```
Initializing ZPDF for file: data/sample_rxi_5.pdf
5.1 Duplicate
Found 174 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
```
