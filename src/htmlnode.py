class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    # autogen code
    def to_html(self) -> str:
        if self.tag is None:
            return self.value or ""
        props_str = " ".join(f'{k}="{v}"' for k, v in self.props.items())
        if props_str:
            props_str = " " + props_str
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

    def props_to_html(self) -> str:
        return " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
