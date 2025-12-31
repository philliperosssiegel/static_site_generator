from textnode import TextNode, TextType
from generator import recursive_directory_copy

def main():  
    recursive_directory_copy(os.path.abspath("static"), os.path.abspath("public"))

if __name__ == "__main__":
    main()