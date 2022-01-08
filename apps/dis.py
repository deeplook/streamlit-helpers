import dis
import io

import streamlit as st
    
from .generic import Tool


class Dis(Tool):
    name = "Dis"
    description = """
    Disassemble Python bytecode into assembly language using the [Disassembler](https://en.wikipedia.org/wiki/Disassembler) in the Python [standard library](https://docs.python.org/3/library/dis.html).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": '''\
pass
''',
            "Example 2": '''\
def foo(dummy):
    return 42
''',
    }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        f = io.StringIO()
        dis.dis(self.text, file=f)
        f.seek(0)
        dis_text = f.read()
        st.markdown(f"<pre>{dis_text}</pre>", unsafe_allow_html=True)
