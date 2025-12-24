class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html() method not implemented for HTMLNode class")
    
    def props_to_html(self):
        if not self.props:
            return f"""{{\n\t"href": "{href_value}",\n\t"target": "{target_value}",\n}}"""
        return None

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode missing required value parameter value")
        if not self.tag:
            return self.value
        if self.props:
            props_str = ""
            for k, v in self.props.items():
                props_str = f'{props_str} {k}="{v}"'
            
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"