import io

import qrcode
import streamlit as st

from .generic import Tool


class QRcode(Tool):
    name = "QR Code"
    description = """
    Convert simple text to a [QR code](https://en.wikipedia.org/wiki/QR_code).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "foobar",
            "Example 2": "If you can read this you are a nerd!",
        }

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        img = qrcode.make(self.text)

        st.image(img.get_image())
        
        f = io.BytesIO()
        with io.BytesIO() as file:
            img.save(f, "PNG")
            f.seek(0)
            data = f.read()
            btn = st.download_button(
                label=f"Download image ({len(data)} bytes)",
                data=data,
                file_name="qrcode.png",
                mime="image/png"
            )