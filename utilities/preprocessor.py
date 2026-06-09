import re


def clean_text(text: str) -> str:
    text = re.sub(r'\[\d+(?:[,\-\s]\d+)*\]', '', text)
    text = re.sub(r'\([A-Za-z][A-Za-z\s.]+,\s*\d{4}[^)]*\)', '', text)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    text = re.sub(r'\n\n+', '\n\n', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'[\ue000-\uf8ff]', '', text)
    return text.strip()
