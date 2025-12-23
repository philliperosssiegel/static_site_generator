from enum import Enum

class Bender(Enum):
    AIR_BENDER = "air"
    WATER_BENDER = "water"
    EARTH_BENDER = "earth"
    FIRE_BENDER = "fire"

class TextType(Enum):
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType , url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, text_node: "TextNode"):
        return self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url
        # # for prop in self:
        # #     if self[prop] != text_node[prop]:
        # #         return False
        # # return True
        # return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    