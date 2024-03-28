# ZPDFTree
## Generic PDF Content Tree Parser
ZPDFTree Python module converts PDFs into structured data, focusing on extracting and organizing table of contents. It uses fitz for PDF processing and pydantic for validation.
**Key Features:**  
1. Creates searchable TOC links tree
2. Non overlapping text extraction
3. Smart self correction for missing TOC parent links
4. Supports caching
5. Estimated PDF coverage metrics

## Install - TODO

## How to Use
### Create ZPDFTree Object
```python
file_path = 'data/sample_file.pdf'
z_pdf_tree = ZPDFTree(file_path=file_path)
```

### Query TocTreeNode
```python
def find_toc_tree_node(toc_key: str) -> TocTreeNode | None:
  pass

# example
z_pdf_tree.find_toc_tree_node('4.2.2')
```

### Create ZPDFTree Cache
```python
def get_cache() -> list[dict]:
  pass

# example
file_path = 'data/sample_file.pdf'
z_pdf_tree = ZPDFTree(file_path=file_path)
with open('test_cache.json', 'w') as f:
    f.write(json.dumps(z_pdf_tree.get_cache(), indent=2))
```

### Load ZPDFTree Cache
```python
file_path = 'data/sample_file.pdf'
cache_path = 'data/sample_cache.json'
with open(cache_path, 'r') as f:
    cache = json.loads(f.read())
z_pdf_tree = ZPDFTree(file_path=pdf_path, cache=cache)
```

### PDF Text Extraction
```python
# non overlap extraction
def extract_text(toc_keys: list[str]) -> list[str]:
  pass

# example
# output will only contain chapter 8 text
toc_keys = ['8.1.7', '8.2.3', '8', '8.4']
sections = z_pdf_tree.extract_text(toc_keys)

# single node text extraction
def find_toc_tree_node(toc_key: str) -> TocTreeNode | None:
  pass

def get_toc_node_text(node: TocTreeNode) -> str | None:
  pass

# example
toc_tree_node = z_pdf_tree.find_toc_tree_node('1.5.2')
z_pdf_tree.get_toc_node_text(toc_tree_node)
```

## Testing
### Generate Full Benchmark
```bash
python benchmark.py > temp/benchmark.txt
```
<details>
<summary>data/benchmark.txt</summary>

```
Parsing: data/sample_rxi_5.pdf
Initializing ZPDFTree for file: data/sample_rxi_5.pdf
5.1 Duplicate
Found 174 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_1.pdf
Initializing ZPDFTree for file: data/sample_rxi_1.pdf
Found 63 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
0.2 not Found
0.3 not Found
0.4 not Found
0.5 not Found
0.6 not Found
0.7 not Found
0.8 not Found
0.9 not Found
0.10 not Found
0.11 not Found
0.11.1 not Found
0.11.2 not Found
0.11.3 not Found
TOC Coverage Metric: 0.7936507936507937
Running Post Correction...
Running Post Correction...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_6.pdf
Initializing ZPDFTree for file: data/sample_rxi_6.pdf
Found 187 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_13.pdf
Initializing ZPDFTree for file: data/sample_rxi_13.pdf
Found 101 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_4.pdf
Initializing ZPDFTree for file: data/sample_rxi_4.pdf
Found 170 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_7.pdf
Initializing ZPDFTree for file: data/sample_rxi_7.pdf
Found 110 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_9.pdf
Initializing ZPDFTree for file: data/sample_rxi_9.pdf
Found 146 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_8.pdf
Initializing ZPDFTree for file: data/sample_rxi_8.pdf
Found 280 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_2.pdf
Initializing ZPDFTree for file: data/sample_rxi_2.pdf
Found 119 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_3.pdf
Initializing ZPDFTree for file: data/sample_rxi_3.pdf
Found 92 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_15.pdf
Initializing ZPDFTree for file: data/sample_rxi_15.pdf
Found 109 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_11.pdf
Initializing ZPDFTree for file: data/sample_rxi_11.pdf
Found 119 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_12.pdf
Initializing ZPDFTree for file: data/sample_rxi_12.pdf
Found 409 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_10.pdf
Initializing ZPDFTree for file: data/sample_rxi_10.pdf
Found 270 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
Parsing: data/sample_rxi_14.pdf
Initializing ZPDFTree for file: data/sample_rxi_14.pdf
Found 60 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
{
  "data/sample_rxi_5.pdf": {
    "toc_headers_count": 174,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_1.pdf": {
    "toc_headers_count": 63,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_6.pdf": {
    "toc_headers_count": 187,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_13.pdf": {
    "toc_headers_count": 101,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_4.pdf": {
    "toc_headers_count": 170,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_7.pdf": {
    "toc_headers_count": 110,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_9.pdf": {
    "toc_headers_count": 146,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_8.pdf": {
    "toc_headers_count": 280,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_2.pdf": {
    "toc_headers_count": 119,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_3.pdf": {
    "toc_headers_count": 92,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_15.pdf": {
    "toc_headers_count": 109,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_11.pdf": {
    "toc_headers_count": 119,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_12.pdf": {
    "toc_headers_count": 409,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_10.pdf": {
    "toc_headers_count": 270,
    "coverage_metric": 1.0
  },
  "data/sample_rxi_14.pdf": {
    "toc_headers_count": 60,
    "coverage_metric": 1.0
  }
}
Benchmarked Files: 15
Benchmark Score: 1.0
```
</details>

### Benchmark Certain PDF File
```python
import json
from z_pdf_tree import *


def test_create_cache_file():
    file_path = 'data/sample_rxi_5.pdf'
    z_pdf_tree = ZPDFTree(file_path=file_path, debug=True)
    with open('test_cache.json', 'w') as f:
        f.write(json.dumps(z_pdf_tree.get_cache(), indent=2))
```
```
Initializing ZPDFTree for file: data/sample_rxi_5.pdf
5.1 Duplicate
Found 174 TOC Headers
Building TOC Tree...
Building TOC Tree...OK
Validating TOC Tree...
TOC Coverage Metric: 1.0
```

### Testbench Data
<details>
<summary>data/testbench.json</summary>

```json
[
    {
        "file_path": "data/sample_rxi_1.pdf",
        "toc_header": "2 CASS ORGANIZATION ",
        "start_page": 34,
        "end_page": 42,
        "end_link_label": "3 CASS FUNCTIONAL DIAGRAM ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_1.pdf",
        "toc_header": "2.3 CRB MEETINGS ",
        "start_page": 37,
        "end_page": 39,
        "end_link_label": "2.4 DUTIES AND RESPONSIBILITIES ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_1.pdf",
        "toc_header": "2.4.5 ROLE OF OUTSIDE AUDITORS",
        "start_page": 40,
        "end_page": 42,
        "end_link_label": "3 CASS FUNCTIONAL DIAGRAM ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_5.pdf",
        "toc_header": "1 DANGEROUS GOODS  GENERAL ",
        "start_page": 46,
        "end_page": 58,
        "end_link_label": "2 CLASSIFICATION AND PACKAGING OF DANGEROUS GOODS ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_5.pdf",
        "toc_header": "3.2 DANGEROUS GOODS PROHIBITED IN AIR TRANSPORT ",
        "start_page": 87,
        "end_page": 90,
        "end_link_label": "3.3 DANGEROUS GOODS CARRIED BY PASSENGERS AND CREW ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_5.pdf",
        "toc_header": "3.2.3 APPROVAL OF EXEMPTIONS ",
        "start_page": 88,
        "end_page": 88,
        "end_link_label": "3.2.4 RESTRICTIONS ON SPECIFIC DANGEROUS GOODS ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_10.pdf",
        "toc_header": "3 PROCEDURES FOR TRAINING AND CHECKING ",
        "start_page": 235,
        "end_page": 277,
        "end_link_label": "4 RECORD KEEPING ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_10.pdf",
        "toc_header": "4.2 STORAGE OF TRAINING RECORDS ",
        "start_page": 279,
        "end_page": 281,
        "end_link_label": "5 APPENDICES ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_10.pdf",
        "toc_header": "1.1.4 MANAGER CABIN CREW TRAINING  STANDARDS ",
        "start_page": 58,
        "end_page": 60,
        "end_link_label": "1.1.5 HUMAN FACTORS MANAGER ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_12.pdf",
        "toc_header": "8 STANDARD OPERATING PROCEDURES ",
        "start_page": 234,
        "end_page": 372,
        "end_link_label": "9 DANGEROUS GOODS AND WEAPONS ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_12.pdf",
        "toc_header": "11.3 REPORTING ACCIDENTS ANDOR SERIOUS INCIDENTS ",
        "start_page": 447,
        "end_page": 449,
        "end_link_label": "11.4 ACCIDENT SERIOUS INCIDENT AND INCIDENT NOTIFICATION AND REPORTING ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_12.pdf",
        "toc_header": "9.9.4 PROVISIONS FOR CARRIAGE ",
        "start_page": 384,
        "end_page": 392,
        "end_link_label": "9.10 ACCEPTANCE AND HANDLING OF DANGEROUS GOODS CARGO ",
        "text_file_path": null
    },
    {
        "file_path": "data/sample_rxi_12.pdf",
        "toc_header": "4.4.1 PROTOCOL FOR RELIEVING THE PIC ",
        "start_page": 182,
        "end_page": 182,
        "end_link_label": "4.4.2 PROTOCOL FOR RELIEVING THE FIRST OFFICER ",
        "text_file_path": "data/4_4_1.txt"
    },
    {
        "file_path": "data/sample_rxi_12.pdf",
        "toc_header": "8.3.6 TRAFFIC COLLISION AVOIDANCE SYSTEM TCASAIRBORNE COLLISION AVOIDANCE SYSTEM ACAS ",
        "start_page": 304,
        "end_page": 305,
        "end_link_label": "8.3.7 POLICY AND PROCEDURES FOR INFLIGHT FUEL MANAGEMENT ",
        "text_file_path": "data/8_3_6.txt"
    },
    {
        "file_path": "data/sample_rxi_12.pdf",
        "toc_header": "8 STANDARD OPERATING PROCEDURES ",
        "start_page": 234,
        "end_page": 372,
        "end_link_label": "9 DANGEROUS GOODS AND WEAPONS ",
        "text_file_path": "data/8.txt"
    }
]
```
</details>
