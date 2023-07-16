#!/usr/bin/python3
"""
Markdown to HTML Converter
"""

import sys
import os.path
import markdown

def convert_markdown_to_html(markdown_file, output_file):
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as file:
        markdown_content = file.read()
        html_content = markdown.markdown(markdown_content)

    with open(output_file, 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_markdown_to_html(markdown_file, output_file)

    sys.exit(0)
