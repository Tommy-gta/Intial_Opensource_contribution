import os
import mmap
import sys
import argparse

def find_files_by_keyword(path, keywords, feature=0, caseSensitive=True):
    """
    Search for files containing specific keywords in a directory and its subdirectories.

    Args:
        path (str): Directory path to search.
        keywords (list): List of keywords to search for.
        feature (int): 0 to return list of files, 1 to return dictionary mapping keywords to files.
        caseSensitive (bool): If False, perform case-insensitive search.

    Returns:
        list or dict: Files containing keywords, format depends on feature parameter.
    """
    # Convert all keywords to lowercase if caseSensitive is False
    if not caseSensitive:
        keywords = [keyword.lower() for keyword in keywords]

    filesfound = []
    filesbykeywords = {}

    # Initialize the filesbykeywords dictionary with an empty list for each keyword
    for word in keywords:
        filesbykeywords.setdefault(word, [])

    # For each file, check if it contains the keywords
    for root, dirs, files in os.walk(path):
        for afile in files:
            filepath = os.path.join(root, afile)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    # mmap.mmap() method creates a bytearray object, and allows for faster I/O
                    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

                    for kword in keywords:
                        # Convert search term to bytes for mmap search
                        search_term = bytes(kword, 'utf-8') if caseSensitive else bytes(kword.lower(), 'utf-8')
                        if s.find(search_term) != -1:
                            if afile not in filesfound:  # Avoid duplicates
                                filesfound.append(afile)
                            print(f"Keyword '{kword}' found in the file '{afile}' at: {filepath}")
                            filesbykeywords[kword].append(afile)
            except (IOError, UnicodeDecodeError, ValueError) as e:
                # Skip binary files or files with encoding issues
                print(f"Skipping file {filepath} due to error: {str(e)}")
                continue

    # Return as per requirement specified by feature parameter
    if len(filesfound) == 0:
        print("No files found")
        return 0

    if feature == 0:
        return filesfound
    elif feature == 1:
        return filesbykeywords

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Search for files containing specific keywords.')
    parser.add_argument('path', help='Directory path to search')
    parser.add_argument('keywords', nargs='+', help='Keywords to search for')
    parser.add_argument('--feature', type=int, default=0, choices=[0, 1],
                       help='0: return list of files, 1: return dictionary mapping keywords to files')
    parser.add_argument('--case-insensitive', action='store_false', dest='caseSensitive',
                       help='Perform case-insensitive search')

    args = parser.parse_args()

    # Call the function with the provided arguments
    result = find_files_by_keyword(args.path, args.keywords, args.feature, args.caseSensitive)

    # Print the result in a readable format
    if result and result != 0:
        print("\nResults:")
        if args.feature == 0:
            print("\n".join(result))
        elif args.feature == 1:
            for keyword, files in result.items():
                print(f"Files containing '{keyword}':")
                print("\n".join(files))
                print()

if __name__ == "__main__":
    main()
