import ast
import platform

import astpretty
import streamlit as st

from .generic import Tool


py_version = list(map(int, platform.python_version_tuple()))


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
        st.session_state.config = dict()
        if py_version >= [3, 8, 0]:
            type_comments = st.checkbox("Type comments")
            st.session_state.config ["type_comments"] = type_comments

    def make_output(self):
        params = {}
        if py_version >= [3, 8, 0]:
            params["type_comments"] = st.session_state.config["type_comments"]
        res = astpretty.pformat(ast.parse(self.text, **params), indent="  ")
        st.markdown(f"<pre>{res}</pre>", unsafe_allow_html=True)
        st.write(st.session_state)
