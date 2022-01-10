import io
import json
import os

import requests
import streamlit as st
from PIL import Image

from .generic import Tool
from .rekognition import find_text


class TextRecognition(Tool):
    name = "Text Recognition"
    description = """
    Recognize text on images using the [AWS Rekognition](https://aws.amazon.com/rekognition/) cloud service.
    
    This needs AWS credentials. Your credentials are used only temporarily, but are not stored
    anywhere as you can see in the [GitHub repository](https://github.com/deeplook/streamlit-helpers).
    You can also create additional temporary credentials on AWS, and use them here.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": "https://fr.mathworks.com/help/examples/matlab/win64/SpecifyWordColorsExample_01.png",
            "Example 2": "https://1.bp.blogspot.com/-0x-JONxUkCg/URpXpUe7L_I/AAAAAAAAACY/hLS0uGY2F1E/s1600/ADBUSTER,+EVAN+MAZIERSKI.jpg",
        }
    
    def make_input(self):
        examples = self.make_examples()
        option = st.selectbox("Source",
            list(examples.keys()) + ["URL", "File Upload"])
        self.im = None
        if option.startswith("Example"):
            url = examples[option]
            data = requests.get(url).content
            f = io.BytesIO(data)
            self.im = Image.open(f)
        elif option == "URL":
            url = st.text_input("Enter URL:", value="")
            if url:
                data = requests.get(url).content
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
        
        box_color = st.text_input("Box color",
            placeholder="black",
            help="The color for the box used to label the detcted found.")

        # st.text_input = dict(
        st.session_state.config = dict(
            aws_access_key_id = aws_access_key_id or key_id,
            aws_secret_access_key = aws_secret_access_key or access_key,
            box_color = box_color or "black",
        )

    def make_output(self):
        if self.im:
            aws_access_key_id = st.session_state.config["aws_access_key_id"]
            aws_secret_access_key = st.session_state.config["aws_secret_access_key"]
            if aws_access_key_id and aws_secret_access_key:
                res, im = find_text(self.im,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    box_color=st.session_state.config["box_color"]
                )
                st.image(im)
                with io.BytesIO() as f:
                    im.save(f, format="PNG")
                    btn = st.download_button(
                        label=f"Download image",
                        data=f,
                        file_name="image.png",
                        mime="image/png"
                    )

                st.subheader("Lines")
                lines = "<br/>".join([
                    td["DetectedText"]
                        for td in res["TextDetections"] if td["Type"]=="LINE"
                ])
                st.markdown(lines, unsafe_allow_html=True)

                st.subheader("Words")
                words = "<br/>".join([
                    td["DetectedText"]
                        for td in res["TextDetections"] if td["Type"]=="WORD"
                ])
                st.markdown(words, unsafe_allow_html=True)

                st.subheader("JSON")
                st.json(res)
                data = json.dumps(res)
                btn = st.download_button(
                    label=f"Download JSON",
                    data=data,
                    file_name="content.json",
                    mime="text/json"
                )
            else:
                st.error("No AWS credentials provided.")
