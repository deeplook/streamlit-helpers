import streamlit as st

from .generic import Tool


class JSON(Tool):
    name = "JSON"
    description = """
    Show a navigatable tree of [JSON](https://en.wikipedia.org/wiki/JSON) code.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "[1, 2, 3]",
            "Example 2": '{"foo": 42, "bar": 24}',
        }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        st.json(self.text)
