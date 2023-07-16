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

# Write HTML content to the output file
with open(output_file, 'w') as file:
    file.write(html_content)

sys.exit(0)
