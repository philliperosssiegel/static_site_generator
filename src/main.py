import os

from textnode import TextNode, TextType
from copystatic import recursive_directory_copy
from gencontent import generate_pages_recursive

def main():  
    recursive_directory_copy(os.path.abspath("static"), os.path.abspath("public"))
    generate_pages_recursive(os.path.abspath("content"), os.path.abspath("public"), os.path.abspath("template.html"))

if __name__ == "__main__":
    main()