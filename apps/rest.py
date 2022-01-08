import io

import docutils.core
import streamlit as st
    
from .generic import Tool


class Rest(Tool):
    name = "ReST"
    description = """
    Render text in [ReStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) format into HTML.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": '''\
Foo *italics* bar **bold**, and ``monospace``.
''',
            "Example 2": '''\
A (buggy?) `example <http://example.com>`_ link.

1. fruits
  * apple
  * banana
2. vegetables
  * carrot
  * broccoli

::

    rST uses :: prior to a paragraph
    for blockquoting.
    Multiple paragraphs need to be prepended individually.
''',
    }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        html = docutils.core.publish_file(
            source=io.StringIO(self.text),
            settings_overrides={'output_encoding': 'unicode'},
            writer_name="html"
        )
        st.markdown(self.text, unsafe_allow_html=True)