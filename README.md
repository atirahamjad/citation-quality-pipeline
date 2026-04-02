# Citation Quality Assessment Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Precision](https://img.shields.io/badge/Precision-95%25-green) ![Time Saved](https://img.shields.io/badge/Time%20Saved-98%25-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

An end-to-end ML pipeline that automates citation quality assessment for academic theses. Built during a Research Assistantship at Sunway Business School — reduces manual review time by **98%** while maintaining **95% precision** across five citation styles.

> Currently under consideration for university-wide adoption. Pending publication.

---

## Key results

| Metric | Value |
|---|---|
| Precision | 95% |
| Review time reduction | 98% |
| Citation styles supported | APA, IEEE, Chicago, Harvard, MLA |
| Codebase size | 12,500+ lines |
| Journal databases matched | JCR Web of Science, ABDC, AJG-ABS |

---

## How it works

The pipeline processes a thesis PDF through six stages:

1. **Document ingestion** — extracts full text using `pdfplumber`, detects citation style (APA, IEEE, Chicago, Harvard, MLA) with a confidence score, and identifies section boundaries (Introduction, Methods, Results, etc.)
2. **Reference parsing** — extracts the reference list and parses each entry into structured fields: authors, year, title, journal, DOI, volume, pages, and publisher
3. **In-text citation extraction** — detects all in-text citation markers per style, captures surrounding sentence context, and classifies the citation's role (support, contrast, finding, method, argument)
4. **Citation-reference linking** — fuzzy-matches each in-text marker to its reference list entry using `rapidfuzz`, with a confidence score per match
5. **Journal quality scoring** — matches each reference against three databases: JCR Web of Science, ABDC, and AJG-ABS; assigns quality tier per journal
6. **Outlier detection and export** — flags Q1 exceptional citations and problematic references into separate sheets; generates a multi-sheet Excel report

---

## Output

The pipeline produces an Excel workbook with the following sheets:

- **All citations** — every in-text citation with context, match confidence, and linked reference
- **Journal quality matches** — each reference scored against JCR, ABDC, and AJG-ABS
- **Exceptional references** — Q1 outlier citations flagged separately
- **Problematic references** — low-confidence matches and unverified entries
- **Internal similarity** — how consistently each source is cited across the document
- **External similarity** — cross-reference overlap analysis

---

## Tech stack

| Layer | Tools |
|---|---|
| PDF processing | `pdfplumber` |
| Citation matching | `rapidfuzz` (fuzzy matching) |
| Data handling | `pandas`, `openpyxl` |
| Pattern detection | `re` (regex), custom multi-style parsers |
| Data structures | Python `dataclasses` |
| Export | Multi-sheet Excel via `openpyxl` |

---

## Quick start
```bash
# Install dependencies
pip install -r requirements.txt

# Run on a thesis PDF
python enhanced_citation_extraction.py
```

---

## Project background

Developed during a 6-month Research Assistantship at Sunway Business School. The pipeline was built to replace a fully manual citation review process that previously took hours per thesis. It has been presented to faculty and is currently under consideration for university-wide adoption, with a related paper pending publication.

---

## Author

**Atirah Amjad** — Master of Business Analytics (Distinction), Sunway University  
[LinkedIn] (https://www.linkedin.com/in/atirah-amjad-148092223/)
