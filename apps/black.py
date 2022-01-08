import black
import streamlit as st
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
    
from .generic import Tool


class Black(Tool):
    name = "Black"
    description = """
    Reformat Python 3 code following [Black](https://github.com/psf/black) rules. See the [documentation](https://black.readthedocs.io/en/stable/).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": """\
pass
""",
            "Example 2": """\
def foo(bar, baz = None) :
    return { 2:42}
"""
        }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        black_code = black.format_str(self.text, mode=black.FileMode())
        style = HtmlFormatter().get_style_defs('.highlight')
        st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
        st.markdown(highlight(black_code, PythonLexer(), HtmlFormatter()), unsafe_allow_html=True)
        st.text(black_code)
