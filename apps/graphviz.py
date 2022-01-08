import streamlit as st

from graphviz import Digraph

from .generic import Tool


def graph1():

    t = Digraph('TrafficLights', filename='traffic_lights.gv', engine='neato')

    t.attr('node', shape='box')
    for i in (2, 1):
        t.node('gy%d' % i)
        t.node('yr%d' % i)
        t.node('rg%d' % i)

    t.attr('node', shape='circle', fixedsize='true', width='0.9')
    for i in (2, 1):
        t.node('green%d' % i)
        t.node('yellow%d' % i)
        t.node('red%d' % i)
        t.node('safe%d' % i)

    for i, j in [(2, 1), (1, 2)]:
        t.edge('gy%d' % i, 'yellow%d' % i)
        t.edge('rg%d' % i, 'green%d' % i)
        t.edge('yr%d' % i, 'safe%d' % j)
        t.edge('yr%d' % i, 'red%d' % i)
        t.edge('safe%d' % i, 'rg%d' % i)
        t.edge('green%d' % i, 'gy%d' % i)
        t.edge('yellow%d' % i, 'yr%d' % i)
        t.edge('red%d' % i, 'rg%d' % i)

    t.attr(overlap='false')
    t.attr(label=r'PetriNet Model TrafficLights\n'
                 r'Extracted from ConceptBase and layed out by Graphviz')
    t.attr(fontsize='12')

    return t


class GraphViz(Tool):
    name = "GraphViz"
    description = """
    Render text in [GraphViz](https://graphviz.org) [DOT](https://graphviz.org/doc/info/lang.html) format to graphs.
    """

    def __init__(self):
        self.text = ""

    def make_examples(self):
        return {
            "Example 1": """\
digraph G {
  bgcolor="purple:pink" label="agraph" fontcolor="white"
  subgraph cluster1 {
    fillcolor="blue:cyan" label="acluster" fontcolor="white" style="filled" gradientangle="270"
    node [shape=box fillcolor="red:yellow" style="filled" gradientangle=90] anode;
  }
""",
            "Example 2": graph1(),
        }

    def make_config(self):
        use_container_width = st.checkbox("Use container width")
        st.session_state.config = dict(
            use_container_width = use_container_width
        )

    def make_output(self):
        use_container_width = st.session_state.config["use_container_width"]
        st.graphviz_chart(self.text, use_container_width=use_container_width)
        # st.write(st.session_state)        
