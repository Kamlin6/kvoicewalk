import re


import re


def _strip_unwanted(text: str) -> str:
    return ''.join(
        c for c in text
        if not (0xD800 <= ord(c) <= 0xDFFF)
        and not (0xE000 <= ord(c) <= 0xF8FF)
        and not (0x200B <= ord(c) <= 0x200F)
        and ord(c) not in (0x2028, 0x2029, 0xFEFF)
    )


def clean_text(text: str) -> str:
    text = re.sub(r'\[\d+(?:[\s,;-]+\d+)*\]', '', text)
    text = re.sub(r'\([A-Za-z][A-Za-z\s.]+,\s*\d{4}[^)]*\)', '', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\n\n+', '\n\n', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'[\xa0\u202f\u205f\u3000]', ' ', text)
    text = _strip_unwanted(text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()
