import re
from typing import Dict, Any
from .base import BaseIssuerParser

class SBICardParser(BaseIssuerParser):
    issuer_name = "SBI Card"
    issuer_markers = ['SBI Card', 'State Bank of India', 'sbicard.com']

    def extract_fields(self, text: str, res) -> Dict[str, Any]:
        fields: Dict[str, Any] = {}
        fields["cardholder_name"] = self._find_name(text, [
            r"Cardholder\s*Name[:\s]+([A-Z][A-Z\s\.'-]+)",
            r"Name\s*[:\-]\s*([A-Za-z][A-Za-z\s\.'-]+)",
        ])
        fields["card_last4"] = self._find_last4(text, [
            r"Card\s*Number[:\s]+(?:X+|\*+)?\s*([0-9]{4})",
            r"XXXX[-\s]*XXXX[-\s]*XXXX[-\s]*([0-9]{4})",
            r"ending\s*with\s*([0-9]{4})",
        ])
        from_date = self._find_date(text, [
            r"Statement\s*Period\s*[:\-]\s*([0-9]{1,2}[^\n\-]+?)[\-–]",
            r"Billing\s*Period\s*[:\-]\s*([0-9]{1,2}[^\n]+?)\s*to",
        ])
        to_date = self._find_date(text, [
            r"Statement\s*Period.*?[to\-–]\s*([0-9]{1,2}[^\n]+?)\n",
            r"to\s*([0-9]{1,2}[^\n]+)",
        ])
        fields["statement_period"] = {{"from": from_date, "to": to_date}}
        fields["payment_due_date"] = self._find_date(text, [
            r"Payment\s*Due\s*Date[:\s]+([A-Za-z0-9 ,\/\-]+)",
            r"Due\s*Date[:\s]+([A-Za-z0-9 ,\/\-]+)",
        ])
        fields["total_amount_due"] = self._find_amount(text, [
            r"Total\s*Amount\s*Due[:\s]+([₹Rs\.\s0-9,]+)",
            r"Total\s*Due[:\s]+([₹Rs\.\s0-9,]+)",
            r"Amount\s*Payable[:\s]+([₹Rs\.\s0-9,]+)",
        ])
        mad = self._find_amount(text, [
            r"Minimum\s*Amount\s*Due[:\s]+([₹Rs\.\s0-9,]+)",
            r"Min\s*Due[:\s]+([₹Rs\.\s0-9,]+)",
        ])
        if mad is not None:
            fields["minimum_amount_due"] = mad
        return fields
