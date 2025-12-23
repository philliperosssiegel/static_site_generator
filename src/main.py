from textnode import TextNode, TextType

def main():
    """
    The main function of the script.
    Contains the primary logic to be executed.
    """
    print("hello world")
    
    text_node = TextNode("This is some anchor text", TextType("link"), "https://www.boot.dev")
    print(text_node)

if __name__ == "__main__":
    main()