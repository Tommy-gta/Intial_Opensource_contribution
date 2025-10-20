# File Search by Keyword

A Python script to search for files containing specific keywords in a directory and its subdirectories. Supports multiple keywords, case sensitivity options, and different output formats.

## Introduction

This script helps you find files containing specific keywords within a directory structure. It's useful for:
- Codebase analysis
- Documentation searches
- Log file investigations
- Any scenario where you need to locate files based on their content

## Features

- Multi-keyword Search: Search for multiple keywords at once
- Case Sensitivity Control: Choose between case-sensitive and case-insensitive searches
- Two Output Formats:
  - Simple list of files containing any keyword
  - Dictionary mapping each keyword to files containing it
- Efficient File Reading: Uses memory-mapped files for faster I/O
- Error Handling: Skips binary files and files with encoding issues
- Recursive Search: Traverses all subdirectories
- Command-line Interface: Easy to use with clear arguments

## Usage

### Prerequisites

- Python 3.x

### Running the Script

#### Basic Usage

```bash
python file_keyword_search.py /path/to/search keyword1 keyword2
```

#### Case-Insensitive Search

```bash
python file_keyword_search /path/to/search keyword1 keyword2 --case-insensitive  
```

#### Dictionary Output Format

```bash
python file_keyword_search /path/to/search keyword1 keyword2 --feature 1
```

#### Arguments

| Argument | Description |
path | Directory path to search (required) |
keywords | One or more keywords to search for (required) |
--feature | Output format: 0 for list, 1 for dictionary (default: 0) |
--case-insensitive | Perform case-insensitive search |

### License

This project is licensed under the MIT License.  
