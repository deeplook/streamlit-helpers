from branca.colormap import linear, step

import streamlit as st


def app():
    st.title("Branca colormaps")
    st.markdown("Overview over linear and step colormaps defined by [Branca](https://github.com/python-visualization/branca).", unsafe_allow_html=True)
    st.header("Linear")
    st.markdown(linear._repr_html_(), unsafe_allow_html=True)
    st.header("Step")
    st.markdown(step._repr_html_(), unsafe_allow_html=True)
