import os
import sys

from textnode import TextNode, TextType
from copystatic import recursive_directory_copy
from gencontent import generate_pages_recursive

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    recursive_directory_copy(os.path.abspath("static"), os.path.abspath("docs"))
    generate_pages_recursive(os.path.abspath("content"), os.path.abspath("docs"), os.path.abspath("template.html"), basepath)    

if __name__ == "__main__":
    main()