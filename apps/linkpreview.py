from textwrap import dedent

import streamlit as st

from .generic import Tool
from .link_preview import LinkPreview as LP

                
class LinkPreview(Tool):
    name = "LinkPreview"
    description = """
    Render little HTML previews of URLs.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": dedent("""\
            https://www.linkedin.com/posts/simonsinek_all-companies-have-a-goal-they-aim-to-achieve-ugcPost-6876906195769163776-sQz2
            
            https://youtu.be/djk159kLBwA0
"""),
            "Example 2": "https://youtu.be/djk159kLBwA0",
        }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        urls = [url for url in self.text.strip().split("\n") if url]
        lp = LP()
        st.markdown(lp.css, unsafe_allow_html=True)
        for url in urls:
            lp.process(url)
            div = lp.make_preview()
            st.markdown(div, unsafe_allow_html=True)
        st.markdown(lp.javascript, unsafe_allow_html=True)
