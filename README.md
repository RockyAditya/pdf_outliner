# PDF Outline Extractor

This project extracts structured headings from PDF documents using text position, font size, and font weight. It identifies titles, H1, and H2 levels and optionally filters them based on a user-defined persona.

---

## Features

- Parses headings using PDF font properties
- Supports bulk PDF processing
- Outputs JSON with page numbers and heading hierarchy
  
---

## Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/RockyAditya/pdf_outliner.git
cd pdf_outliner
pip install -r requirements.txt
```

## How to Run

```bash
docker build --platform=linux/amd64 -t pdf-outline-extractor .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor

```
## How to run after this

.\run_extractor.ps1
## then output goes to outputfolder_name.json

## Boom you get the summary

# pdf_outliner
