# License Header Adder

A Python script to automatically add developer info and license headers to source code files in various languages (Python, C, Java, JavaScript, Rust, etc.).


## Introduction

This script helps you maintain consistent license headers across your project by:
- Adding developer information and license notices to source files
- Supporting multiple programming languages with appropriate comment styles
- Creating a LICENSE file if one doesn't exist
- Avoiding duplicate headers by checking existing content


## Features

- **Multi-language Support**: Handles Python, C, Java, JavaScript, Rust, Go, Shell, and more
- **Smart Detection**: Skips files that already have license headers
- **Customizable Templates**: Easily modify the header format for different languages
- **Recursive Processing**: Works through directories and subdirectories
- **MIT License Generation**: Automatically creates a LICENSE file


## Usage

### Prerequisites

- Python 3.x

### Running the Script

1. Save the script as `add_license_headers.py`
2. Customize the `DEVELOPER_INFO` and `LICENSE_TEXT` variables in the script
3. Run the script:
   ```bash
   python add_license_headers.py /path/to/your/project
   ```
   
   Replace `/path/to/your/project` with your project directory. Defaults to current directory.
  
  
### Example Output
 
```bash
Processing directory: /path/to/your/project
Created LICENSE file at /path/to/your/project/LICENSE
Added license header to /path/to/your/project/src/main.py
Skipping /path/to/your/project/src/utils.py: Already has a license header.
Added license header to /path/to/your/project/lib/helper.c
```
   
### License 

This project is licensed under the MIT License.
