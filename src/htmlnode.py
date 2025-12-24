class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html() method not implemented for HTMLNode class")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_str = ""
        for k, v in self.props.items():
            props_str = f'{props_str} {k}="{v}"'
        return props_str

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode missing required value parameter value")
        if self.tag is None:
            return self.value 
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"