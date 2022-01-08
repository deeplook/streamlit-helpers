import os

import streamlit as st

from .generic import Tool


class Text2Speech(Tool):
    name = "Text to Speech"
    description = """
    Convert text to speech using the [AWS Polly](https://docs.aws.amazon.com/polly/) cloud service.
    This needs AWS credentials. Your credentials are used only temporarily, but are not stored
    anywhere as you can see in the [GitHub repository](https://github.com/deeplook/streamlit-helpers).
    You can also create additional temporary credentials on AWS, and use them here.
    
    Beware, that some voices support only the "standard", but not the "neural" speech synthesis engine!
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": """\
Hello Text-to-Speech world!
""",
            "Example 2": """\
Hello amazing Text-to-Speech world!
"""
        }
    
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
        
        voice = st.selectbox("Voice",
            """Joey Nicole Kevin Enrique Tatyana Russell Olivia Lotte Geraint Carmen Ayanda
Mads Penelope Mia Joanna Matthew Brian Seoyeon Ruben Ricardo Maxim Lea Giorgio Carla
Aria Naja Maja Astrid Ivy Kimberly Chantal Amy Vicki Marlene Ewa Conchita Camila
Karl Zeina Miguel Mathieu Justin Lucia Jacek Bianca Takumi Ines Gwyneth Cristiano
Mizuki Celine Zhiyu Jan Liv Raveena Filiz Dora Salli Aditi Vitoria Emma Lupe
Hans Kendra Gabrielle""".split()
        )
        engine = st.selectbox("Engine", "neural standard".split())
        st.session_state.config = dict(
            aws_access_key_id = aws_access_key_id or key_id,
            aws_secret_access_key = aws_secret_access_key or access_key,
            voice=voice,
            engine=engine,
        )


    def make_output(self):
        aws_access_key_id = st.session_state.config["aws_access_key_id"]
        aws_secret_access_key = st.session_state.config["aws_secret_access_key"]
        voice = st.session_state.config["voice"]
        engine = st.session_state.config["engine"]
        if aws_access_key_id and aws_secret_access_key:
            data = synthesize_speech(self.text,
                out="output.mp3",
                voice=voice,
                engine=engine,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                save=False)
            st.audio(data, format="audio/mp3")
        else:
            st.error("No AWS credentials provided.")
