import autopep8
import streamlit as st
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
    
from .generic import Tool


class Pep8(Tool):
    name = "PEP-8"
    description = """
    Reformat Python source code to follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) style guide.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": '''\
def example1():
    ####This is a long comment. This should be wrapped to fit within 72 characters.
    some_tuple=(   1,2, 3,'a'  );
    some_variable={'long':'Long code lines should be wrapped within 79 characters.',
    'other':[math.pi, 100,200,300,9876543210,'This is a long string that goes on'],
    'more':{'inner':'This whole logical line should be wrapped.',some_tuple:[1,
    20,300,40000,500000000,60000000000000000]}}
    return (some_tuple, some_variable)
''',
        }

    def make_config(self):
        max_line_length = st.number_input("Max. line length", min_value=40, max_value=120, value=72)
        aggressive = st.number_input("Aggressive level", min_value=0, value=0)
        st.session_state.config = dict(
            max_line_length=max_line_length,
            aggressive=aggressive
        )

    def make_output(self):
        options = st.session_state.config
        # pep8_code = st.text(autopep8.fix_code(self.text, options=options))
        style = HtmlFormatter().get_style_defs('.highlight')
        st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
        st.markdown(highlight(autopep8.fix_code(self.text, options=options), PythonLexer(), HtmlFormatter()), unsafe_allow_html=True)
