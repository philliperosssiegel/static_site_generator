import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid text, index-parity failure for delimiter={delimiter}")

        for i, text in enumerate(split_text):
            if text == "":
                continue
            elif i % 2 == 0: #even --> not inline text
                new_nodes.append(TextNode(text, TextType.TEXT))
            else: #odd --> inline text
                new_nodes.append(TextNode(text, text_type))
    
    return new_nodes

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)