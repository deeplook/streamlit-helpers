import io

from pyzbar.pyzbar import decode
from PIL import Image
import requests
import streamlit as st

from .generic import Tool


class QRdecode(Tool):
    name = "QR Decode"
    description = """
    Decode an image with [QR code(s)](https://en.wikipedia.org/wiki/QR_code) to text.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "https://aaronparecki.com/2015/10/05/12/image-3.png",
            "Example 2": "http://www.dailydooh.com/wp-content/uploads/2011/08/generic-QR-code.jpg",
        }

    def make_input(self):
        headers = {'User-agent': 'Mozilla/5.0'}
        examples = self.make_examples()
        option = st.selectbox("Source",
            list(examples.keys()) + ["URL", "File Upload"])
        self.im = None
        if option.startswith("Example"):
            url = examples[option]
            data = requests.get(url, headers=headers).content
            f = io.BytesIO(data)
            self.im = Image.open(f)
        elif option == "URL":
            url = st.text_input("Enter URL:", value="")
            if url:
                data = requests.get(url, headers=headers).content
                f = io.BytesIO(data)
                self.im = Image.open(f)
        elif option == "File Upload":
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file:
                f = io.BytesIO(uploaded_file.getvalue())
                self.im = Image.open(f)
        if self.im:
            st.image(self.im)

    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        codes = decode(self.im)
        for code in codes:
            st.text(code.data.decode("utf-8"))
