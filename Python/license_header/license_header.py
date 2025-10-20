#!/usr/bin/env python3
import os
import re
from datetime import datetime

# --- Configuration ---
DEVELOPER_INFO = f"""\
// Copyright (c) {datetime.now().year} Your Name or Organization
// Author: Your Name <your.email@example.com>
// License: MIT (see LICENSE file for details)
"""

LICENSE_TEMPLATE = {
    "py": f'# {DEVELOPER_INFO.replace("// ", "# ")}',
    "c": f'/* {DEVELOPER_INFO.replace("// ", " * ")} */',
    "h": f'/* {DEVELOPER_INFO.replace("// ", " * ")} */',
    "java": f'/* {DEVELOPER_INFO.replace("// ", " * ")} */',
    "js": f'/* {DEVELOPER_INFO.replace("// ", " * ")} */',
    "rs": f'//! {DEVELOPER_INFO.replace("// ", "//! ")}',
    "go": f'/* {DEVELOPER_INFO.replace("// ", " * ")} */',
    "sh": f'# {DEVELOPER_INFO.replace("// ", "# ")}',
    "default": f'// {DEVELOPER_INFO}'
}

FILE_EXTENSIONS = {
    '.py': 'py',
    '.c': 'c',
    '.h': 'h',
    '.java': 'java',
    '.js': 'js',
    '.rs': 'rs',
    '.go': 'go',
    '.sh': 'sh'
}

LICENSE_TEXT = """\
MIT License

Copyright (c) {year} Your Name or Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""".format(year=datetime.now().year)

def get_license_header(file_path):
    """Determine the appropriate license header for a file."""
    ext = os.path.splitext(file_path)[1].lower()
    for file_ext, license_type in FILE_EXTENSIONS.items():
        if ext == file_ext:
            return LICENSE_TEMPLATE[license_type]
    return LICENSE_TEMPLATE["default"]

def has_license_header(file_path):
    """Check if a file already has a license header."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        license_header = get_license_header(file_path)
        # Use regex to check if any line in the header exists in the file
        pattern = re.compile(re.escape(license_header.split('\n')[0].strip()))
        return bool(pattern.search(content))

def add_license_header(file_path):
    """Add license header to a file if it doesn't already have one."""
    if has_license_header(file_path):
        print(f"Skipping {file_path}: Already has a license header.")
        return

    license_header = get_license_header(file_path)
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(license_header + '\n\n' + content)
    print(f"Added license header to {file_path}")

def create_license_file(directory='.'):
    """Create a LICENSE file if it doesn't exist."""
    license_path = os.path.join(directory, 'LICENSE')
    if not os.path.exists(license_path):
        with open(license_path, 'w', encoding='utf-8') as f:
            f.write(LICENSE_TEXT)
        print(f"Created LICENSE file at {license_path}")
    else:
        print(f"Skipping LICENSE: Already exists at {license_path}")

def process_directory(directory='.'):
    """Process all files in a directory and add license headers."""
    create_license_file(directory)

    supported_extensions = set(FILE_EXTENSIONS.keys())
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file_path)[1].lower()
            if ext in supported_extensions:
                add_license_header(file_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add license headers to source code files.")
    parser.add_argument("directory", nargs='?', default='.', help="Directory to process (default: current directory)")
    args = parser.parse_args()

    print(f"Processing directory: {args.directory}")
    process_directory(args.directory)

