import autopep8
import streamlit as st
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
    
from .generic import Tool


class Pep8(Tool):
    name = "PEP-8"
    description = """
    Reformat Python source code to follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) rules.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": '''\
import math, sys;

def example1():
    ####This is a long comment. This should be wrapped to fit within 72 characters.
    some_tuple=(   1,2, 3,'a'  );
    some_variable={'long':'Long code lines should be wrapped within 79 characters.',
    'other':[math.pi, 100,200,300,9876543210,'This is a long string that goes on'],
    'more':{'inner':'This whole logical line should be wrapped.',some_tuple:[1,
    20,300,40000,500000000,60000000000000000]}}
    return (some_tuple, some_variable)
def example2(): return {'has_key() is deprecated':True}.has_key({'f':2}.has_key(''));
class Example3(   object ):
    def __init__    ( self, bar ):
     #Comments should have a space after the hash.
     if bar : bar+=1;  bar=bar* bar   ; return bar
     else:
                    some_string = """
                       Indentation in multiline strings should not be touched.
Only actual code should be reindented.
"""
                    return (sys.path, some_string)
''',
        }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        pep8_code = st.text(autopep8.fix_code(self.text))
        style = HtmlFormatter().get_style_defs('.highlight')
        st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
        st.markdown(highlight(pep8_code, PythonLexer(), HtmlFormatter()), unsafe_allow_html=True)
