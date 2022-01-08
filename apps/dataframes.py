import streamlit as st
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

from .generic import Tool


iris = pd.DataFrame(load_iris()["data"])
df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

# st.dataframe(df)  # Same as st.write(df)


class Dataframe(Tool):
    name = "Dataframes"
    description = """
    Render tabular input in formats like [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) to [dataframes](https://databricks.com/glossary/what-are-dataframes).
    """
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html.

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": iris,
            "Example 2": pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"),
        }

    def make_input(self):
        pass
    
    def make_config(self):
        use_container_width = st.checkbox("Use container width")
        st.session_state.config = dict(
            use_container_width = use_container_width
        )

    def make_output(self):
        use_container_width = st.session_state.config["use_container_width"]
        st.write(iris) # , use_container_width=use_container_width)
        # st.write(st.session_state)        
