import requests
import streamlit as st

from apps import home, ast, awkward, black, dataframes, dis, graphviz, generic, json, linkpreview, pep8, qrcode, rest, svg, text2speech


st.set_page_config(
    page_title="Coding Tools - Streamlit",
    # layout="wide",
    # initial_sidebar_state="auto",
)

with st.sidebar:
    st.sidebar.header("Menu")
    tool = st.selectbox("",
        ["Home", "AST", "Awkward", "Black", "Dataframe", "Dis", "GraphViz", "Generic", "JSON", "Link Preview", "PEP-8", "QR Code", "ReST", "SVG", "Text to Speech"]
    )
    st.sidebar.header("Settings")
    st.session_state.layout = st.radio("Input/Output Orientation",
        ["Horizontal", "Vertical"]
    )
    st.session_state.verify_code = st.checkbox("Verify code", help="Verify this code is the latest available.")

    if 0:
        st.sidebar.header("Session State")
        st.write(st.session_state)

def main():    
    if tool == "Home":
        home.app()
    elif tool == "AST":
        ast.AST()()
    elif tool == "Awkward":
        awkward.Awkward()()
    elif tool == "Black":
        black.Black()()
    elif tool == "Dataframe":
        dataframes.Dataframe()()
    elif tool == "Dis":
        dis.Dis()()
    elif tool == "GraphViz":
        graphviz.GraphViz()()
    elif tool == "Generic":
        generic.Tool()()
    elif tool == "JSON":
        json.JSON()()
    elif tool == "Link Preview":
        linkpreview.LinkPreview()()
    elif tool == "PEP-8":
        pep8.Pep8()()
    elif tool == "QR Code":
        qrcode.QRcode()()
    elif tool == "ReST":
        rest.Rest()()
    elif tool == "SVG":
        svg.SVG()()
    elif tool == "Text to Speech":
        text2speech.Text2Speech()()
        if st.session_state.verify_code:
            repo_url = "https://github.com/deeplook/streamlit-helpers/"
            url = "https://github.com/deeplook/streamlit-helpers/blob/main/apps/text2speech.py"
            raw_url = "https://raw.githubusercontent.com/deeplook/streamlit-helpers/main/apps/text2speech.py"
            repo_file = requests.get(raw_url).text
            the_file = open(text2speech.__file__).read()
            if the_file != repo_file:
                st.warning(f"**WARNING:** The code you see running here is **not** the [latest one]({url}) in the [repo]({repo_url})!")
            else:
                st.info(f"The code running here was verified right now to be the [latest one]({url}) in the [repo]({repo_url})!")

            st.write(f"[Source]({url})")

main()
