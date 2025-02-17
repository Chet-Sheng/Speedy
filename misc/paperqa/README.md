# Build Environment
```bash
conda env create -f environment.yml
conda env update -f environment.yml

conda env list
conda activate paperqa_speedy
```

# Folder Content
- [paperqa_zotero.py](paperqa_zotero.py): Parse pdf from zotero library, retrieve metadata from Semantic Scholar and CrossRef APIs, and load it as `paperqa.Docs` instance.