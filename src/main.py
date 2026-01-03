import os

from textnode import TextNode, TextType
from copystatic import recursive_directory_copy
from gencontent import generate_pages_recursive

def main():  

    # source_path, target_path, generator_template = os.path.abspath("static"), os.path.abspath("public"), os.path.abspath("template.html")

    source_path = os.path.abspath("static")
    target_path = os.path.abspath("public")
    template_path = os.path.abspath("template.html")

    recursive_directory_copy(source_path, target_path)

    # generate_pages_recursive(source_path, target_path, template_path)
    generate_pages_recursive(os.path.abspath("content"), target_path, template_path)
    # generate_page(os.path.join("content", "index.md"), os.path.join(target_path, "index.html"), generator_template)
    # generate_page(os.path.join("content/blog/glorfindel", "index.md"), os.path.join(target_path, "index.html"), generator_template)

    # generate_page(os.path.join("content/blog/tom", "index.md"), os.path.join(target_path, "index.html"), generator_template)

    # generate_page(os.path.join("content/blog/majesty", "index.md"), os.path.join(target_path, "index.html"), generator_template)
    # generate_page(os.path.join("content/contact", "index.md"), os.path.join(target_path, "index.html"), generator_template)

if __name__ == "__main__":
    main()