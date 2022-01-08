import streamlit as st
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
    
from .generic import Tool


class Pygments(Tool):
    name = "Pygments"
    description = """
    Add syntax highlighting to [arbitrary](https://pygments.org/languages/) code using [Pygments](https://pygments.org/).
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": """\
#!/bin/bash
for (( counter=10; counter>0; counter-- ))
do
echo -n "$counter "
done
printf "\n"
""",
            "Example 2": """\
def foo(bar, baz = None) :
    import wrong
    return { 2:42}
""",
            "Example 3": """\
UPDATE Customers
SET ContactName='John Smith', City='Chicago'
WHERE CustomerID=1;
""",
        }
    def make_config(self):
        st.session_state.config = dict()

    def make_output(self):
        style = HtmlFormatter().get_style_defs('.highlight')
        st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
        lexer = guess_lexer(self.text)
        st.markdown(highlight(self.text, lexer, HtmlFormatter()), unsafe_allow_html=True)
        st.text(lexer.__class__.__name__)
