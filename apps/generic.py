import io

import requests

import streamlit as st


class Tool:
    name = "Generic"
    description = "A dummy tool."

    def __init__(self):
        self.text = ""


    def make_examples(self):
        return {
            "Example 11": "Foo",
            "Example 22": "Bar",
        }


    def make_config(self):
        genre = st.radio("What's your favorite movie genre",
             ('Comedy', 'Drama', 'Documentary')
        )
        agree = st.checkbox("I disagree")
        values = st.slider("Select a range of values",
             0.0, 100.0, (25.0, 75.0)
        )
        st.session_state.config = dict(genre=genre, agree=agree, values=values)


    def make_input(self):
        examples = self.make_examples()
        option = st.selectbox("Source",
            list(examples.keys()) + ["URL", "File Upload", "Text"])
        code = ""
        if option.startswith("Example"):
            code = examples[option]
        elif option == "URL":
            url = st.text_input("Enter URL:", value="")
            if url:
                code = requests.get(url).text
        elif option == "File Upload":
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file:
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                # st.write(stringio)
                # To read file as string:
                code = stringio.read()
                # st.write(string_data)
        elif option == "Text":
            code = ""
        self.text = st.text_area("Content", value=code, height=300, key=1)


    def make_output(self):
        st.markdown(self.text, unsafe_allow_html=True)
        st.write(st.session_state)


    def __call__(self):
        st.title(self.name)
        st.markdown(self.description)

        layout = st.session_state.layout
        if layout == "Horizontal":
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Input"):
                    self.make_input()
                with st.expander("Parameters"):
                    self.make_config()
            with col2:
                with st.expander("Output"):
                    self.make_output()
        elif layout == "Vertical":
            with st.expander("Input"):
                self.make_input()
            with st.expander("Parameters"):
                self.make_config()
            with st.expander("Output"):
                self.make_output()
