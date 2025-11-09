import argparse, json
from parsers.router import parse_statement_from_pdf, parse_statement_from_text

def main():
    ap = argparse.ArgumentParser(description='Credit Card Statement Parser')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--input', help='Path to PDF statement')
    g.add_argument('--text-file', help='Path to plaintext file (demo)')
    g.add_argument('--text', help='Raw text string')
    ap.add_argument('--out', help='Write JSON result to this file (optional)')
    ap.add_argument('--ocr', action='store_true', help='Enable OCR fallback for scanned PDFs')
    args = ap.parse_args()

    if args.input:
        result = parse_statement_from_pdf(args.input, use_ocr=args.ocr)
    elif args.text_file:
        with open(args.text_file, 'r', encoding='utf-8') as fh:
            txt = fh.read()
        result = parse_statement_from_text(txt)
    else:
        result = parse_statement_from_text(args.text or '')

    out = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(out)
    else:
        print(out)

if __name__ == '__main__':
    main()
