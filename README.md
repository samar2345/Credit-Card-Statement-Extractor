# Credit Card Statement Parser (Python)

A robust PDF/text parser that extracts 5+ key data points from **5 issuers** (India-focused) and outputs clean JSON.

**Issuers covered**
- HDFC Bank
- ICICI Bank
- SBI Card
- Axis Bank
- American Express India

**Data points extracted (at least 5)**
- `cardholder_name`
- `card_last4`
- `statement_period` (from_date, to_date)
- `payment_due_date`
- `total_amount_due`
- (also returns `minimum_amount_due` if found)

## Quick start

### 1) Create a virtual environment and install deps
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run on a PDF
```bash
python main.py --input path/to/statement.pdf --out out.json
```

### 3) Run on provided **example texts** (for demo without PDFs)
```bash
# HDFC sample
python main.py --text-file example_texts/hdfc_sample.txt --out out_hdfc.json

# All samples at once
python demo_run.py
```

### 4) Run tests
```bash
pytest -q
```

## Output JSON schema
```json
{
  "issuer": "HDFC Bank",
  "confidence": 0.93,
  "fields": {
    "cardholder_name": "John Doe",
    "card_last4": "1234",
    "statement_period": {"from": "2025-09-06", "to": "2025-10-05"},
    "payment_due_date": "2025-10-25",
    "total_amount_due": 15432.55,
    "minimum_amount_due": 1000.0
  },
  "raw_hints": { "matched_patterns": ["due_date:...","total_due:..."] }
}
```

## Notes
- PDF text is extracted via **pdfplumber**. If a page is image-only, enable OCR with `--ocr` (requires Tesseract installed locally).
- Issuer detection is pattern-based and fuzzy; the parser reports a `confidence` score.
- Clean separation between **base parser**, **issuer-specific extractors**, and **PDF utilities** makes it easy to add more issuers.
