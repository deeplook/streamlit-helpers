import streamlit as st


def app():
    st.title("Online Coding Tools")

    st.markdown(
        """
        This web app offers simple versions of common tools useful for developers under a [Streamlit](https://streamlit.io) interface,
        e.g. to preview popular formats like Markdown or RestructuredText, convert between different representations of data like text and QR codes, or visualize simple data structures like JSON or GraphViz.
        
        The goal is to make this collection easily accessible and extensible for others,
        and to explore and stretch Streamlit as an interface for such tasks.
        Therefore, this is a free, open-source project and you are very welcome to contribute your comments, questions, resources, and apps as [issues](https://github.com/deeplook/streamlit-helpers/issues) or 
        [pull requests](https://github.com/deeplook/streamlit-helpers/pulls) to the [GitHub repository](https://github.com/deeplook/streamlit-helpers).
        """
    )

    st.info("Click on the left sidebar menu to open the different tools.")
