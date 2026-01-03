import os

from textnode import TextNode, TextType
from copystatic import recursive_directory_copy
from generator import generate_page

def main():  

    source_path, target_path, generator_template = os.path.abspath("static"), os.path.abspath("public"), os.path.abspath("template.html")

    recursive_directory_copy(source_path, target_path)
    generate_page(os.path.join("content", "index.md"), os.path.join(target_path, "index.html"), generator_template)

if __name__ == "__main__":
    main()