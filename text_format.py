# Write by GPT-4o mini🧙‍♂️, scillidan🤡
# Usage: python text_format.py <input_file> <output_file>

import sys
import re

def process_text(text):
	# 9. remove ansi code <0x85> (which is U+0085, NEL)
	text = text.replace('\x85','')

	# 1. remove all content with <dt></dt>, including tag and content inside
	# use DOTALL to remove multiline content inside <dt>...</dt>
	text = re.sub(r'<dt>.*?</dt>', '', text, flags=re.DOTALL)

	# 3. remove all <dd> and </dd> tags, keep content inside
	text = re.sub(r'</?dd>', '', text)

	# 4. convert <span style="color: #47A">Some String</span> to <font style="color:green">Some String</font>
	# remove empty spans as well, more robust to variations
	span_color_pattern = re.compile(
	    r'<span\s+style="[^"]*color\s*:\s*#47A\s*;?[^"]*">(.*?)</span>',
	    flags=re.DOTALL | re.IGNORECASE
	)

	def span_to_font(m):
	    content = m.group(1)
	    if content.strip() == '':
	        return ''  # Remove empty spans entirely
	    return f'<font style="color:green">{content}</font>'

	text = span_color_pattern.sub(span_to_font, text)

	# 5. remove bword:// from all <a href="bword://Word String">Word String</a>
	# Also keep the rest intact.
	def fix_anchor(m):
		url = m.group(1)
		text_inside = m.group(2)
		if url.startswith('bword://'):
			url = url[len('bword://'):]
		return f'<a href="{url}">{text_inside}</a>'
	text = re.sub(r'<a href="([^"]+)">(.*?)</a>', fix_anchor, text, flags=re.DOTALL)

	# 6. convert <p style="font-style: normal; font-size: x-small; text-align: right">String</p>
	# to just String (keep content)
	text = re.sub(
		r'<p style="font-style:\s*normal;\s*font-size:\s*x-small;\s*text-align:\s*right">(.*?)</p>',
		r'\1', text, flags=re.DOTALL)

	# 7. delete trailing spaces per line
	lines = text.splitlines()
	lines = [line.rstrip() for line in lines]
	text = "\n".join(lines)

	# 8. convert all literal \n char (backslash+n) to <br />
	text = text.replace(r'\n', '<br />')

	# remove duplicated <br /> repeated multiple in a row -> just one <br />
	text = re.sub(r'(<br />\s*){2,}', r'<br />', text)

	# remove trailing <br /> (with optional spaces) at line ends
	lines = text.splitlines()
	lines = [re.sub(r'<br />\s*$', '', line) for line in lines]
	text = "\n".join(lines)

	# Replace sequences of <br />, <br/>, possibly mixed and with spaces, to a single <br />
	text = re.sub(r'(?:<br\s*/?>\s*){2,}', r'<br />', text, flags=re.IGNORECASE)

	# Remove <br /> or <br/> immediately after <blockquote>
	text = re.sub(r'(<blockquote>)\s*(<br\s*/?>)', r'\1', text, flags=re.IGNORECASE)

	return text

def main():
	if len(sys.argv) != 3:
		print("Usage: python script.py <input> <output>", file=sys.stderr)
		sys.exit(1)

	input_path = sys.argv[1]
	output_path = sys.argv[2]

	# read input file with utf-8 encoding
	with open(input_path, 'r', encoding='utf-8') as f:
		content = f.read()

	output = process_text(content)

	with open(output_path, 'w', encoding='utf-8') as f:
		f.write(output)

if __name__ == '__main__':
	main()
