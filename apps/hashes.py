import hashlib

import streamlit as st

from .generic import Tool


class Hashes(Tool):
    name = "Hashes"
    description = """
    Generate hex-digests for all hashes available in the [Python standard library](https://docs.python.org/3/library/hashlib.html).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "Hello world",
        }

    def make_config(self):
        digest_length = st.slider('Digest length',
            min_value=0, max_value=256, value=32,
            help="Digest length for hashes like SHAKE.")
        st.session_state.config = dict(
            digest_length=digest_length
        )

    def make_output(self):
        digest_length = st.session_state.config["digest_length"]
        res = {}
        for name in sorted(hashlib.algorithms_available):
            h = hashlib.new(name)
            h.update(self.text.encode("utf-8"))
            try:
                digest = h.hexdigest()
            except:
                # Use desired hash length for SHAKE hashes:
                digest = h.hexdigest(digest_length)
            res[name] = digest
        st.json(res)
