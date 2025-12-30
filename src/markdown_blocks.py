from enum import Enum
from functools import reduce

from htmlnode import HTMLNode
from textnode import TextNode

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
        
    return HTMLNode(tag="div", value=None, children=html_nodes)

def create_block_html_parent_node(block_text: str):

    block_type = block_to_block_type(block_text) 

    match block_type:
        case BlockType.PARAGRAPH:
            tag = "p"
            inline_text = block_text
            # break
        case BlockType.HEADING:
            tag = "h"
            inline_text = block_text.lstrip("#").lstrip(" ")
            # break
        case BlockType.CODE:
            tag = "code"
            inline_text = block_text
            # break
        case BlockType.QUOTE:
            tag = "blockquote"
            inline_text = block_text.lstrip("> ")
            # break
        case BlockType.OLIST:
            tag = "ol"
            inline_text = block_text.split(". ")[1]
            # break
        case BlockType.ULIST:
            tag = "ul"
            inline_text = block_text.lstrip("- ")
            # break

    children_nodes = text_to_children(inline_text)
    
    return HTMLNode(tag=tag, value=None, children=children_nodes) #missing handling of inner list components and heading level in nodes atm

def get_heading_type(text):
    return len(text) - len(text.lstrip("#"))

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