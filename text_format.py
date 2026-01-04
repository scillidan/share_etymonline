# Authors: GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python file.py <input_file> <output_file>

import sys
import re
from html import unescape

def match_remove(text):
    # Remove ANSI control character U+0085 (NEL)
    text = text.replace('\x85','')
    # Remove "bword://" from <a ...>
    def rm_bword(m):
        url = m.group(1)
        inner_text = m.group(2)
        if url.startswith('bword://'):
            url = url[len('bword://'):]
        return f'<a href="{url}">{inner_text}</a>'
    text = re.sub(r'<a href="([^"]+)">(.*?)</a>', rm_bword, text, flags=re.DOTALL)
    # Remove <dd></dd>
    text = re.sub(r'</?dd>', '', text)
    # Remove <dt>...</dt>
    text = re.sub(r'<dt>.*?</dt>', '', text, flags=re.DOTALL)
    # Remove <p style="font-style: normal; font-size: x-small; text-align: right"></p>
    text = re.sub(
        r'<p style="font-style:\s*normal;\s*font-size:\s*x-small;\s*text-align:\s*right">(.*?)</p>',
        r'\1', text, flags=re.DOTALL)
    # Remove <span></span>
    text = re.sub(r'<span[^>]*>\s*</span>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = text.replace('\\n', '<br>')
    # Replace all variations of <br> tags with <br>
    text = re.sub(r'<br\s*/?>', '<br>', text, flags=re.IGNORECASE)
    # Replace repeated <br> with <br>
    text = re.sub(r'(<br>\s*)+', '<br>', text)
    # Replace repeated ' ' with ' '
    return re.sub(r' {2,}', ' ', text)
    # Remove <br> after <blockquote>
    text = re.sub(r'(\\n<blockquote>\\n)', '<blockquote>', text, flags=re.IGNORECASE)
    return text

def match_replace(text):
    # Replace <span style="color: #47A">...</span> with <font style="color:green">...</font>
    source_color = "#47A"
    target_color = "green"
    color_pattern = re.compile(
        rf'<span\s+style="[^"]*color\s*:\s*{re.escape(source_color)}\s*;?[^"]*">(.*?)</span>',
        flags=re.DOTALL | re.IGNORECASE
    )
    def replace_span(match: re.Match) -> str:
        # Get the content inside the span
        content = match.group(1)
        return f'<font style="color:{target_color}">{content}</font>'
    return color_pattern.sub(replace_span, text)

def match_convert(text):
    # Convert <ol></ol> to numbering list
    def repl(match):
        ol_tag = match.group(1)
        li_tag = re.findall(r'<li>(.*?)</li>', ol_tag, flags=re.DOTALL | re.IGNORECASE)
        cleaned_li_tag = [f"{i + 1}. {item.strip()}" for i, item in enumerate(li_tag)]
        return '<br><br>'.join(cleaned_li_tag)
    return re.sub(r'<ol>(.*?)</ol>', repl, text, flags=re.DOTALL | re.IGNORECASE)

def format(line):
    if '\t' not in line:
        return line.strip()
    parts = line.split('\t', 1)
    word = parts[0]
    meaning = parts[1].strip()

    meaning = match_remove(meaning)
    meaning = match_replace(meaning)
    meaning = match_convert(meaning)
    meaning = unescape(meaning)
    meaning = meaning.strip()

    result = f"{word}\t{meaning}"
    return result

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    result = format(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

if __name__ == '__main__':
    main()