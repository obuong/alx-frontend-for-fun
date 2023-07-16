#!/usr/bin/python3

import sys
import os.path
import re

if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

markdown_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isfile(markdown_file):
    sys.stderr.write(f"Missing {markdown_file}\n")
    sys.exit(1)

# Read the Markdown file
with open(markdown_file, 'r') as file:
    markdown_content = file.read()

# Parse headings syntax and generate HTML
html_content = re.sub(r'^(#{1,6})\s+(.+)$', r'<\1>\2</\1>', markdown_content, flags=re.MULTILINE)

# Parse unordered listing syntax and generate HTML
html_content = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'(?<=</h[1-6]>)(.*)(?=\n<ul>)', r'\1\n', html_content, flags=re.DOTALL)
html_content = re.sub(r'(?<=</ul>)(.*)(?=<h[1-6]>)', r'\n\1', html_content, flags=re.DOTALL)
html_content = re.sub(r'^\s*<h[1-6]>', r'\n<\g<0>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'</h[1-6]>\s*$', r'\g<0>\n', html_content, flags=re.MULTILINE)
html_content = re.sub(r'(?<=</ul>)\s*$', r'\n', html_content)

# Write HTML content to the output file
with open(output_file, 'w') as file:
    file.write(html_content)

sys.exit(0)
