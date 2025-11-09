import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from dateutil import parser as dtp

@dataclass
class ParseResult:
    issuer: str
    fields: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    raw_hints: Dict[str, Any] = field(default_factory=dict)

class BaseIssuerParser:
    issuer_name: str = 'Unknown'
    issuer_markers: List[str] = []

    def detect_confidence(self, text: str) -> float:
        score = 0
        for m in self.issuer_markers:
            if m.lower() in text.lower():
                score += 1
        return min(1.0, score / max(1, len(self.issuer_markers)))

    def parse(self, text: str) -> 'ParseResult':
        res = ParseResult(issuer=self.issuer_name)
        res.confidence = self.detect_confidence(text)
        res.fields.update(self.extract_fields(text, res))
        return res

    def _find_date(self, text: str, patterns: List[str]) -> Optional[str]:
        for p in patterns:
            m = re.search(p, text, flags=re.I)
            if m:
                raw = m.group(1).strip()
                try:
                    return dtp.parse(raw, dayfirst=True).date().isoformat()
                except Exception:
                    pass
        return None

    def _find_amount(self, text: str, patterns: List[str]) -> Optional[float]:
        for p in patterns:
            m = re.search(p, text, flags=re.I)
            if m:
                raw = m.group(1).replace(',', '').strip()
                raw = re.sub(r'[^\d.]', '', raw)
                try:
                    return float(raw)
                except Exception:
                    pass
        return None

    def _find_name(self, text: str, patterns: List[str]) -> Optional[str]:
        for p in patterns:
            m = re.search(p, text, flags=re.I)
            if m:
                return re.sub(r'\s{2,}', ' ', m.group(1).strip())
        return None

    def _find_last4(self, text: str, patterns: List[str]) -> Optional[str]:
        for p in patterns:
            m = re.search(p, text, flags=re.I)
            if m:
                last4 = re.sub(r'\D', '', m.group(1))[-4:]
                if len(last4) == 4:
                    return last4
        return None

    def extract_fields(self, text: str, res: 'ParseResult') -> Dict[str, Any]:
        raise NotImplementedError
