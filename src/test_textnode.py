import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_is_valid_node(self):
        try:
            node = TextNode("This is a text node", TextType.ASTERISK)
        except:
            node = "invalid node"
        self.assertNotEqual(type(node), TextNode)

    def test_is_valid_text_type(self):
        try:
            text_type = TextType("ASTERISK")
        except:
            text_type = "invalid text_type"
        self.assertNotEqual(type(text_type), TextType)
    
    def missing_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()