import re


def clean_text(text: str) -> str:
    text = re.sub(r'\[\d+(?:[\s,;-]+\d+)*\]', '', text)
    text = re.sub(r'\([A-Za-z][A-Za-z\s.]+,\s*\d{4}[^)]*\)', '', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\n\n+', '\n\n', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'[\ue000-\uf8ff]', '', text)
    text = re.sub(r'[\u200b-\u200f\u2028\u2029\ufeff]', '', text)
    text = re.sub(r'[\xa0\u202f\u205f\u3000]', ' ', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()
