import requests
import streamlit as st

from apps import home, ast, awkward, black, dataframes, graphviz, generic, json, linkpreview, qrcode, text2speech


st.set_page_config(
    page_title="Coding Tools - Streamlit",
    # layout="wide",
    # initial_sidebar_state="auto",
)

with st.sidebar:
    st.sidebar.header("Menu")
    tool = st.selectbox("",
        ["Home", "AST", "Awkward", "Black", "Dataframe", "GraphViz", "Generic", "JSON", "Link Preview", "QR Code", "Text to Speech"]
    )
    st.sidebar.header("Settings")
    st.session_state.layout = st.radio("Input/Output Orientation",
        ["Horizontal", "Vertical"]
    )
    st.session_state.check_updates = st.checkbox("Check for updates")
    
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
    elif tool == "GraphViz":
        graphviz.GraphViz()()
    elif tool == "Generic":
        generic.Tool()()
    elif tool == "JSON":
        if st.session_state.check_updates:
            this_file = open(__file__).read()
            repo_url = "https://github.com/deeplook/streamlit-helpers/"
            url = "https://github.com/deeplook/streamlit-helpers/blob/main/apps/json.py"
            raw_url = "https://raw.githubusercontent.com/deeplook/streamlit-helpers/main/apps/json.py"
            repo_file = requests.get(raw_url).text
            if this_file != repo_file:
                st.warning(f"**WARNING:** The code you see running here is **not** the [latest one]({url}) in the [repo]({repo_url})!")

        json.JSON()()
        if st.session_state.check_updates:
            st.write(f"[Source]({url})")
    elif tool == "Link Preview":
        linkpreview.LinkPreview()()
    elif tool == "QR Code":
        qrcode.QRcode()()
    elif tool == "Text to Speech":
        text2speech.Text2Speech()()

main()