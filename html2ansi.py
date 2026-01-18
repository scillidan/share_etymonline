# Usage: python file.py <input_file> <output_file>

import sys
import re

def convert(text):
    convert_dict = {
        "<blockquote>": "    ",
        "</blockquote>": "",
        "<br>": r"\n",
        '<span style="color:green;">': "\033[32m",
        "</span>": "\033[0m",
        '<i>': "\033[3m",
        "</i>": "\033[0m",
    }

    for html, ansi in convert_dict.items():
        text = text.replace(html, ansi)

    # Replace an HTML link tag with ANSI-escaped underlined blue text
    def convert_link(match):
        a_tag = match.group(1)
        text_inner = match.group(2)
        return f"\033[4;34m{text_inner}\033[0m"

    # Replace all HTML anchor tags with ANSI-escaped text
    text = re.sub(r'<a\s+href="([^"]*)">([^<]*)</a>', convert_link, text)

    return text

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    result = convert(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Conversion completed: {input_file} to {output_file}")

if __name__ == '__main__':
    main()