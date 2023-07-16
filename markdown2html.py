#!/usr/bin/python3
"""
Markdown to HTML converter
"""
import sys
import hashlib

MARKDOWN_TO_HTML = {
    "#": "h1",
    "##": "h2",
    "###": "h3",
    "####": "h4",
    "#####": "h5",
    "######": "h6",
    "-": "ul",
    "*": "ol"
}


def print_error(message):
    sys.stderr.write(message + '\n')


def convert_heading(line):
    level = line.count('#')
    tag = MARKDOWN_TO_HTML.get('#' * level)
    return f"<{tag}>{line.strip('# ').strip()}</{tag}>\n"


def convert_list(line):
    symbol = line[0]
    tag = MARKDOWN_TO_HTML.get(symbol)
    return f"<{tag}><li>{line.strip(symbol + ' ')}</li></{tag}>\n"


def convert_inline_markdown(line):
    line = line.replace("**", "<b>", 1).replace("**", "</b>", 1)
    line = line.replace("__", "<em>", 1).replace("__", "</em>", 1)
    return line


def convert_md5_hash(line):
    while "[[" in line and "]]" in line:
        start_index = line.index("[[")
        end_index = line.index("]]")
        to_hash = line[start_index+2:end_index]
        md5_hash = hashlib.md5(to_hash.encode()).hexdigest()
        line = line.replace("[[" + to_hash + "]]", md5_hash)
    return line


def convert_case_insensitive(line):
    while "((" in line and "))" in line:
        start_index = line.index("((")
        end_index = line.index("))")
        to_replace = line[start_index+2:end_index]
        to_replace = to_replace.replace('c', '').replace('C', '')
        line = line.replace("((" + line[start_index+2:end_index] + "))", to_replace)
    return line


def convert_paragraph(line, in_paragraph):
    if line.strip():
        if not in_paragraph:
            line = "<p>\n" + line
            in_paragraph = True
        else:
            line = line.replace("\n", "<br/>\n")
    else:
        if in_paragraph:
            line = "</p>\n" + line
            in_paragraph = False
    return line, in_paragraph


def convert_markdown_to_html(input_file, output_file):
    in_paragraph = False

    try:
        with open(input_file, 'r') as input_fp, open(output_file, 'w') as output_fp:
            for line in input_fp:
                line = convert_inline_markdown(line)
                line = convert_md5_hash(line)
                line = convert_case_insensitive(line)

                if line.startswith("#"):
                    line = convert_heading(line)
                elif line.startswith("-") or line.startswith("*"):
                    line = convert_list(line)
                else:
                    line, in_paragraph = convert_paragraph(line, in_paragraph)

                output_fp.write(line)

            if in_paragraph:
                output_fp.write("</p>\n")

    except FileNotFoundError:
        print_error(f"Missing {input_file}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_error("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
