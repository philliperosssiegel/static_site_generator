import re

from textnode import TextType, TextNode

def markdown_to_blocks(markdown: str):
    markdown_blocks = []
    for block in markdown.split("\n\n"): #presumed that all input markdown is "well-formed" --> double newline block separation
        clean_block = block.strip()
        if not (clean_block in ["", "\n"]):
            markdown_blocks.append(clean_block)
    
    return markdown_blocks

def text_to_textnodes(text):
    nodes = [TextNode(text)]
    delimiter_dict = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`"
    }
    for text_type, delimiter in delimiter_dict.items():
        nodes.extend(split_nodes_delimiter(text_type, delimiter))
    
    nodes.extend(split_nodes_image(nodes))
    nodes.extend(split_nodes_link(nodes))

    return nodes

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

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        split_images = extract_markdown_images(remaining_text)
        if not split_images:
            new_nodes.append(node)
            continue 

        while len(split_images) > 0:
            image_alt, image_link = split_images.pop(0)
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            remaining_text = sections[1]
            split_images = extract_markdown_images(remaining_text)

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        split_links = extract_markdown_links(remaining_text)
        if not split_links:
            new_nodes.append(node)
            continue 

        while len(split_links) > 0:
            link_description, link_url = split_links.pop(0)
            sections = remaining_text.split(f"[{link_description}]({link_url})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_description, TextType.LINK, link_url))
            
            remaining_text = sections[1]
            split_links = extract_markdown_links(remaining_text)

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)