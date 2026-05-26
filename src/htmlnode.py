class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self) -> str:
        if self.tag is None:
            return self.value or ""
        props_str = self.props_to_html()
        if props_str:
            props_str = " " + props_str
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

    def props_to_html(self) -> str:
        return " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        if props_str:
            props_str = " " + props_str

        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        props_str = self.props_to_html()
        if props_str:
            props_str = " " + props_str
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
