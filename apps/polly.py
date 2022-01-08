# https://docs.aws.amazon.com/polly/latest/dg/voicelist.html

from contextlib import closing
from os.path import splitext

import boto3


def synthesize_speech(
    text,
    out="foo.mp3",
    format=None,
    engine="neural",
    voice="Kevin",
    aws_access_key_id="",
    aws_secret_access_key="",
    save=False
):
    """Synthesize speech with AWS Polly into an audio output.
    """
    formats = "ogg_vorbis json mp3 pcm".split()
    if format:
        assert format in formats
    assert type(out) in [str]
    if type(out) == str:
        if "." in out:
            ext = splitext(out)[-1]
            assert ext[1:] in formats
        if not format:
            format = "mp3"
        else:
            assert format in formats
            out = f"{out}.{format}"
            
    assert engine in "standard neural".split()

    voices = """Nicole Kevin Enrique Tatyana Russell Olivia Lotte Geraint Carmen Ayanda
Mads Penelope Mia Joanna Matthew Brian Seoyeon Ruben Ricardo Maxim Lea Giorgio Carla
Aria Naja Maja Astrid Ivy Kimberly Chantal Amy Vicki Marlene Ewa Conchita Camila
Karl Zeina Miguel Mathieu Justin Lucia Jacek Bianca Takumi Ines Gwyneth Cristiano
Mizuki Celine Zhiyu Jan Liv Joey Raveena Filiz Dora Salli Aditi Vitoria Emma Lupe
Hans Kendra Gabrielle""".split()
    # Beware, some voices don't support the "neural" engine...
    assert voice in voices

    polly = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    params = dict(Text=text, OutputFormat=format, Engine=engine, VoiceId=voice)
    synth = polly.synthesize_speech
    resp = synth(**params)
    if "AudioStream" in resp:
        with closing(resp["AudioStream"]) as stream:
            if save:
                with open(out, "wb") as f:
                    f.write(stream.read())
            else:
                return stream.read()
