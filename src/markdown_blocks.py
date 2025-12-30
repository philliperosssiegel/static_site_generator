from enum import Enum
from functools import reduce

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    # html_nodes = []
    # for block in blocks:
    #     block_type = block_to_block_type(block)
        
    #     if block_type != TextType.CODE:
    #         parent_text_node = TextNode("", block_type)
    #         parent_html_node = text_node_to_html_node(parent_text_node)
    #         parent_html_node.children = text_to_textnodes(block)
    #         html_nodes.append(parent_html_node)
    #     else:
    #         parent_text_node = TextNode(block, block_type)
    #         parent_html_node = text_node_to_html_node(parent_text_node)
    #         html_nodes.append(parent_html_node)

    # return htmlNode(tag="div", value=None, children=html_nodes)

    html_nodes = []
    for block in blocks:
        html_nodes.append(create_block_html_parent_node(block))    
        
    return ParentNode(tag="div", children=html_nodes)

def create_block_html_parent_node(block_text: str):

    block_type = block_to_block_type(block_text) 

    if block_type in [BlockType.PARAGRAPH, BlockType.HEADING, BlockType.QUOTE]:
        if block_type == BlockType.PARAGRAPH:
            parent_tag = "p"
            lines = block_text.split("\n")
            stripped = [line.strip() for line in lines]
            inline_text = " ".join(stripped)
        elif block_type == BlockType.HEADING:
            parent_tag = f"h{get_heading_type(block_text)}"
            inline_text = block_text.lstrip("#").lstrip(" ")
        else: #QUOTE
            parent_tag = "blockquote"
            # inline_text = ""
            # for line in block_text.split("\n"):
            #     inline_text += f"\n{line.lstrip('>').lstrip()}"
            lines = block_text.split("\n")
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("Invalid quote block")
            stripped = [line.lstrip(">").lstrip() for line in lines]
            inline_text = " ".join(stripped)
            # inline_text = block_text.lstrip(">").lstrip()
        parent_node = ParentNode(tag=parent_tag, children=text_to_children(inline_text))
    elif block_type == BlockType.CODE:
        if not block_text.startswith("```") or not block_text.endswith("```"):
            raise ValueError("Invalid code block")
        # inline_text = block_text.lstrip("`").rstrip("`")
        # inline_text = ""

        # for line in block_text.split("\n"):
        #     if line != "```":
        #         # inline_text += f"\n{line}"
        #         lines.append(line)

        # lines = block_text.split("\n")
        # inline_text = "\n".join(lines[1:-1]) + "\n" #drop ``` first and last lines

        inline_text = block_text[4:-3]
        raw_text_node = TextNode(inline_text, TextType.TEXT)
        child_node = text_node_to_html_node(raw_text_node)
        parent_node = ParentNode(tag="pre", children=[ParentNode(tag="code", children=[child_node])])
    elif block_type in [BlockType.OLIST, BlockType.ULIST]:
        if block_type == BlockType.OLIST:
            parent_tag = "ol"
        else: #ULIST
            parent_tag = "ul"
        lines = block_text.split("\n")
        parent_node = ParentNode(tag=parent_tag, children=[]) 
        # ul_node = HTMLNode(tag="ul", children=[])
        for line in lines:
            if block_type == BlockType.OLIST:
                line_text = line.split(".", 1)[1].lstrip()
            else: #ULIST
                line_text = line.lstrip("- ").lstrip()
            inline_children = text_to_children(line_text)
            parent_node.children.append(ParentNode(tag="li", children=inline_children))
        
    return parent_node

def get_heading_type(text):
    heading_level = len(text) - len(text.lstrip("#"))
    if heading_level + 1 >= len(text):
        raise ValueError(f"Invalid heading level: {heading_level}") 
    return heading_level

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]

    return children

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str):
    markdown_blocks = []
    for block in markdown.split("\n\n"): #presumed that all input markdown is "well-formed" --> double newline block separation
        clean_block = block.strip()
        if not (clean_block in ["", "\n"]):
            markdown_blocks.append(clean_block)
    
    return markdown_blocks