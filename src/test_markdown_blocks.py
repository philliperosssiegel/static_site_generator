import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_get_markdown_block_type__paragraph(self):
        mk = """
general markdown
line
line
asdvkmglkgmnd fm fdmf f kmm fmd fm fdsm ;fsdmf 121948 8 1848193148 38 1831 
"""
        self.assertEqual(block_to_block_type(mk), BlockType.PARAGRAPH)

    def test_get_markdown_block_type__headers(self):
        mk = """
# general markdown
## line
### line
###### asdvkmglkgmnd fm fdmf f kmm fmd fm fdsm ;fsdmf 121948 8 1848193148 38 1831
#
### 
"""
        self.assertEqual(block_to_block_type(mk), BlockType.PARAGRAPH)
    
    # def test_get_markdown_block_type__code(self):
    #     mk = """ ``` fdlmfk mdf m13r13prmrp2 mp1mr m ``` """
    #     self.assertEqual(block_to_block_type(mk), BlockType.CODE)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_order_list_block_checks(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "2. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. one\nnot list\n2. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()