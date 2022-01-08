import ast

import astpretty
import streamlit as st

from .generic import Tool


class AST(Tool):
    name = "AST"
    description = """
    Show [Abstract Syntax Trees](https://en.wikipedia.org/wiki/Abstract_syntax_tree) for Python source code. See the [documentation](https://docs.python.org/3/library/ast.html) in the Python 3 [standard library](https://docs.python.org/3/library/).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": """\
pass
""",
            "Example 2": """\
async def func():
    await other_func()
"""
        }

    def make_config(self):
        type_comments = st.checkbox("Type comments")
        st.session_state.config = dict(
            type_comments = type_comments
        )

    def make_output(self):
        type_comments = st.session_state.config["type_comments"]
        res = astpretty.pformat(ast.parse(self.text, type_comments=type_comments), indent="  ")
        st.markdown(f"<pre>{res}</pre>", unsafe_allow_html=True)
        st.write(st.session_state)
