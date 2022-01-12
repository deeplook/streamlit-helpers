import json
import os

import requests
import streamlit as st

from .generic import Tool
from .aws_translate import translate_text


class TranslateText(Tool):
    name = "Text Translation"
    description = """
    Translate text using the [AWS Translate](https://aws.amazon.com/translate/) cloud service.
    
    This needs AWS credentials. Your credentials are used only temporarily, but are not stored
    anywhere as you can see in the [GitHub repository](https://github.com/deeplook/streamlit-helpers).
    You can also create additional temporary credentials on AWS, and use them here.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "The quick brown fox jumped over the lazy old dog.",
        }
    
    def make_input(self):
        examples = self.make_examples()
        option = st.selectbox("Source",
            list(examples.keys()) + ["URL", "File Upload", "Text"])
        self.text = ""
        if option.startswith("Example"):
            self.text = examples[option]
        elif option == "URL":
            url = st.text_input("Enter URL:", value="")
            if url:
                self.text = requests.get(url).text
        elif option == "File Upload":
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file:
                self.text = uploaded_file.read()
        elif option == "Text":
            self.text = st.text_area("Content", value="", height=200, key=1)

    def make_config(self):
        key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        msg1 = f"Using {key_id} found in env. if left empty."
        msg2 = "Env. variable AWS_ACCESS_KEY_ID not found."
        aws_access_key_id = st.text_input('AWS Access Key ID',
            placeholder=f"Found AWS_ACCESS_KEY_ID in env." if key_id else "",
            help=msg1 if key_id else msg2)

        access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        msg1 = f"Using {access_key} found in env. if left empty."
        msg2 = "Env. variable AWS_SECRET_ACCESS_KEY not found."
        aws_secret_access_key = st.text_input('AWS Secret Access Key',
            placeholder=f"Found AWS_SECRET_ACCESS_KEY in env." if access_key else "",
            help=msg1 if access_key else msg2)
        
        source_lang = st.text_input("Source Language",
            value="auto",
            help="Two-letter language code (eg. en, fr, de, zh, ...) or auto.",
        )
        target_lang = st.text_input("Target Language",
            value="en",
            help="Two-letter language code (eg. en, fr, de, zh, ...) or auto.",
        )

        # st.text_input = dict(
        st.session_state.config = dict(
            aws_access_key_id = aws_access_key_id or key_id,
            aws_secret_access_key = aws_secret_access_key or access_key,
            text = self.text,
            source_lang = source_lang,
            target_lang = target_lang,
        )

    def make_output(self):
        if self.text:
            aws_access_key_id = st.session_state.config["aws_access_key_id"]
            aws_secret_access_key = st.session_state.config["aws_secret_access_key"]
            if aws_access_key_id and aws_secret_access_key:
                res = translate_text(self.text,
                    source_lang=st.session_state.config["source_lang"],
                    target_lang=st.session_state.config["target_lang"],
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                )
                st.write(res["TranslatedText"])
                st.json(res)
            else:
                st.error("No AWS credentials provided.")
