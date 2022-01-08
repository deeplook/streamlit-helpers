import json

import awkward as ak
import streamlit as st

from .generic import Tool


class Awkward(Tool):
    name = "Awkward"
    description = """
    Manipulate [JSON](https://en.wikipedia.org/wiki/JSON)-like data with NumPy-like idioms using [Awkward](https://github.com/scikit-hep/awkward-1.0).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "[[1.1, 2.2, 3.3], [], [4.4, 5.5]]",
        }

    def make_config(self):
        expr = st.text_input('Expression')
        st.session_state.config = dict(
            expr=expr
        )

    def make_output(self):
        expr = st.session_state.config["expr"]
        arr = ak.from_json(self.text)
        res = ak.to_json(eval("arr" + expr))
        st.json(res)
        st.write(res)
