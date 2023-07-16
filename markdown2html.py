#!/usr/bin/python3
"""
Markdown to HTML conversion 
"""

import sys
from os import path
import re
import hashlib

def convert_md_to_html(md_file, html_file):
    
    if not path.exists(md_file):
        print("Error: Markdown file not found")
        sys.exit(1)
        
    html = []
    
    with open(md_file) as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith("#"):
            level = line.count("#") 
            html.append(f"<h{level}>{line.lstrip('#').strip()}</h{level}>")
            
        elif line.startswith("-") or line.startswith("*"):
            if line.startswith("-"):
                tag = "ul"
            else:
                tag = "ol"
                
            if not html or "</li>" in html[-1]:
                html.append(f"<{tag}>")
                
            html.append(f"<li>{line.lstrip('-').lstrip('*').strip()}</li>")
            
        elif line.startswith("```"):
            continue
            
        else:
            if not html or html[-1].startswith("<h") or html[-1].startswith("</li>"):
                html.append("<p>")
                
            line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
            
            line = re.sub(r"\[\[(.+?)\]\]", lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
            line = re.sub(r"\(\((.+?)\)\)", lambda m: re.sub("[cC]", "", m.group(1)), line)
            
            if "<br/>" not in line:
                line = line.replace("\n", "<br/>\n")
                
            html.append(line)
            
    for tag in ["ul", "ol", "p"]:
        if html[-1].startswith(f"<{tag}>"):
            html.append(f"</{tag}>")
            
    with open(html_file, "w") as f:
        f.write("\n".join(html))
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)
        
    md_file = sys.argv[1]
    html_file = sys.argv[2]
    
    convert_md_to_html(md_file, html_file)

