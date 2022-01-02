#!/usr/bin/env python

"""
A collection of frequently used coding helpers with a Streamlit interface.

This is a prototype only, so far...

Run the app:

    $ streamlit run streamlit_helpers.py
"""

import ast
import dis
import io
import json
import sys
from textwrap import dedent

import astpretty
import autopep8
import black
import docutils.core
import folium
import numpy as np
import pygments
import qrcode
import requests
import streamlit as st
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from streamlit_folium import folium_static

from link_preview import LinkPreview


# config

st.set_page_config(
    page_title="Streamlit Helpers",
    layout="wide",
    initial_sidebar_state="auto",
)

# sidebar

with st.sidebar:
    st.sidebar.header("Streamlit Helpers")
    # st.sidebar.markdown("Helpers")
    converter = st.radio("",
        ["Home"] + list(sorted(["JSON", "QRcode", 'GraphViz', "GeoJSON", 'Black', "Pygments", "LaTeX", "Regexp", "AST", "Dis", "SVG", "Markdown", "ReST", "PEP-8", "Link Preview"])) + ["..."]
    )
    layout = st.radio("Layout",
        ["Horizontal", "Vertical"]
    )
    st.sidebar.markdown("About")
    st.sidebar.markdown("See [code on GitHub](https://github.com/deeplook/streamlit-helpers).")

# main

st.title(converter)
if converter == "GraphViz":
    col1, col2 = st.columns(2)
    with col1:
        sample = """\
digraph G {
  bgcolor="purple:pink" label="agraph" fontcolor="white"
  subgraph cluster1 {
    fillcolor="blue:cyan" label="acluster" fontcolor="white" style="filled" gradientangle="270"
    node [shape=box fillcolor="red:yellow" style="filled" gradientangle=90] anode;
  }
}"""
        with st.expander("Input"):
            code = st.text_area("", value=sample, height=300)
    with col2:
        with st.expander("Output"):
            st.graphviz_chart(code, use_container_width=False)

elif converter == "Black":
    col1, col2 = st.columns(2)
    with col1:
        sample = """\
def foo(bar, baz = None) :
    return { 2:42}
"""
        with st.expander("Input"):
            url = st.text_input("URL", value="")
            code = st.text_area("", value=sample, height=300, key=1)
    with col2:
        with st.expander("Output"):
            if url:
                code = requests.get(url).text
            black_code = black.format_str(code, mode=black.FileMode())
            style = HtmlFormatter().get_style_defs('.highlight')
            st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
            st.markdown(highlight(black_code, PythonLexer(), HtmlFormatter()), unsafe_allow_html=True)

elif converter == "Link Preview":
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Input"):
            value = dedent("""\
            https://www.linkedin.com/posts/simonsinek_all-companies-have-a-goal-they-aim-to-achieve-ugcPost-6876906195769163776-sQz2
            https://youtu.be/3GvWh3XlJ-0
            """)
            urls = st.text_area("URLs", value=value).strip().split("\n")
            urls = [url for url in urls if url]
    with col2:
        with st.expander("Output"):
            if urls:
                lp = LinkPreview()
                st.markdown(lp.css, unsafe_allow_html=True)
                for url in urls:
                    lp.process(url)
                    div = lp.make_preview()
                    st.markdown(div, unsafe_allow_html=True)
                st.markdown(lp.javascript, unsafe_allow_html=True)

elif converter == "PEP-8":
    col1, col2 = st.columns(2)
    with col1:
        sample = '''\
import math, sys;

def example1():
    ####This is a long comment. This should be wrapped to fit within 72 characters.
    some_tuple=(   1,2, 3,'a'  );
    some_variable={'long':'Long code lines should be wrapped within 79 characters.',
    'other':[math.pi, 100,200,300,9876543210,'This is a long string that goes on'],
    'more':{'inner':'This whole logical line should be wrapped.',some_tuple:[1,
    20,300,40000,500000000,60000000000000000]}}
    return (some_tuple, some_variable)
def example2(): return {'has_key() is deprecated':True}.has_key({'f':2}.has_key(''));
class Example3(   object ):
    def __init__    ( self, bar ):
     #Comments should have a space after the hash.
     if bar : bar+=1;  bar=bar* bar   ; return bar
     else:
                    some_string = """
                       Indentation in multiline strings should not be touched.
Only actual code should be reindented.
"""
                    return (sys.path, some_string)
'''
        with st.expander("Input"):
            code = st.text_area("", value=sample, height=300, key=1)
    with col2:
        with st.expander("Output"):
            st.text(autopep8.fix_code(code))
            if 0:
                pep8_code = autopep8.fix_code(sample)
                style = HtmlFormatter().get_style_defs('.highlight')
                st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
                st.markdown(highlight(sample, PythonLexer(), HtmlFormatter()), unsafe_allow_html=True)

elif converter == "QRcode":
    col1, col2 = st.columns(2)
    with col1:
        sample_code = "foobar"
        with st.expander("Source"):
            code = st.text_area("", value=sample_code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            img = qrcode.make(code)
            # st.image(img.tobytes())
            qr = qrcode.QRCode()
            qr.add_data(code)
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            st.image(f.read())

elif converter == "GeoJSON":
    col1, col2 = st.columns(2)
    with col1:
        code = """\
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [ -90.0715, 29.9510 ]
      },
      "properties": {
        "name": "Fred",
           "gender": "Male"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [ -92.7298, 30.7373 ]
      },
      "properties": {
        "name": "Martha",
           "gender": "Female"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [ -91.1473, 30.4711 ]
      },
      "properties": {
        "name": "Zelda",
        "gender": "Female"
      }
    }
  ]
}
"""
        with st.expander("Source"):
            py_code = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Map"):
            m = folium.Map(location=[0, 0], zoom_start=1)
            folium.GeoJson(json.loads(py_code)).add_to(m)
            folium_static(m)

elif converter == "JSON":
    col1, col2 = st.columns(2)
    with col1:
        code = """\
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [ -90.0715, 29.9510 ]
      },
      "properties": {
        "name": "Fred",
           "gender": "Male"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [ -92.7298, 30.7373 ]
      },
      "properties": {
        "name": "Martha",
           "gender": "Female"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [ -91.1473, 30.4711 ]
      },
      "properties": {
        "name": "Zelda",
        "gender": "Female"
      }
    }
  ]
}
"""
        with st.expander("Source"):
            py_code = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            st.json(py_code)

elif converter == "Pygments":
    col1, col2 = st.columns(2)
    with col1:
        sample_code = """\
def foo(bar, baz = None) :
    return { 2:42}
"""
        with st.expander("Source"):
            py_code = st.text_area("", value=sample_code, height=300, key=1)
    with col2:
        with st.expander("Pygmented"):
            style = HtmlFormatter().get_style_defs('.highlight')
            st.markdown(f"<style>\n{style}\n</style>", unsafe_allow_html=True)
            st.markdown(highlight(py_code, PythonLexer(), HtmlFormatter()), unsafe_allow_html=True)

elif converter == "LaTeX":
    col1, col2 = st.columns(2)
    with col1:
        sample_code = r"""
\sum_{k=0}^{n-1} ar^k =
a \left(\frac{1-r^{n}}{1-r}\right)
"""
        with st.expander("LaTeX Source"):
            dot_text = st.text_area("", value=sample_code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            st.latex(dot_text)

elif converter == "SVG":
    col1, col2 = st.columns(2)
    with col1:
        code = r"""
<svg height="400" width="450">
<path id="lineAB" d="M 100 350 l 150 -300" stroke="red" stroke-width="3" fill="none" />
  <path id="lineBC" d="M 250 50 l 150 300" stroke="red" stroke-width="3" fill="none" />
  <path d="M 175 200 l 150 0" stroke="green" stroke-width="3" fill="none" />
  <path d="M 100 350 q 150 -300 300 0" stroke="blue" stroke-width="5" fill="none" />
  <!-- Mark relevant points -->
  <g stroke="black" stroke-width="3" fill="black">
    <circle id="pointA" cx="100" cy="350" r="3" />
    <circle id="pointB" cx="250" cy="50" r="3" />
    <circle id="pointC" cx="400" cy="350" r="3" />
  </g>
  <!-- Label the points -->
  <g font-size="30" font-family="sans-serif" fill="black" stroke="none" text-anchor="middle">
    <text x="100" y="350" dx="-30">A</text>
    <text x="250" y="50" dy="-10">B</text>
    <text x="400" y="350" dx="30">C</text>
  </g>
  Sorry, your browser does not support inline SVG.
</svg>
"""
        with st.expander("Source"):
            svg = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            st.markdown(svg, unsafe_allow_html=True)

elif converter == "Markdown":
    col1, col2 = st.columns(2)
    with col1:
        code = r"""Foo *italics* bar **bold**.

$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$
"""
        with st.expander("Source"):
            text = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            st.markdown(text, unsafe_allow_html=True)

elif converter == "AST":
    col1, col2 = st.columns(2)
    with col1:
        code = """\
async def f():
    await other_func()
"""
        with st.expander("Input (Python)"):
            text = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            res = astpretty.pformat(ast.parse(text), indent="  ")
            st.markdown(f"<pre>{res}</pre>", unsafe_allow_html=True)

elif converter == "Dis":
    col1, col2 = st.columns(2)
    with col1:
        code = """\
def foo(dummy):
    return 42
"""
        with st.expander("Source"):
            text = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            f = io.StringIO()
            dis.dis(text, file=f)
            f.seek(0)
            dis_text = f.read()
            st.markdown(f"<pre>{dis_text}</pre>", unsafe_allow_html=True)

elif converter == "ReST":
    col1, col2 = st.columns(2)
    with col1:
        code = """
Foo *italics* bar **bold**.
"""
        with st.expander("Source"):
            text = st.text_area("", value=code, height=300, key=1)
    with col2:
        with st.expander("Output"):
            html = docutils.core.publish_file(
                source=io.StringIO(text),
                settings_overrides={'output_encoding': 'unicode'},
                writer_name="html")
            st.markdown(text, unsafe_allow_html=True)

else:
    st.markdown('More to come...')
    def make_input(code):
        with st.expander("URL"):
            url = st.text_input("", value="")
        with st.expander("File Upload"):
            uploaded_file = st.file_uploader("Choose a file")
        with st.expander("Text"):
            text = st.text_area("", value=code, height=300, key=1)
        with st.expander("Config"):
            genre = st.radio("What's your favorite movie genre",
                 ('Comedy', 'Drama', 'Documentary')
            )
            agree = st.checkbox("I agree")
            values = st.slider("Select a range of values",
                 0.0, 100.0, (25.0, 75.0)
            )
    if layout == "Horizontal":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Input")
            make_input("foo")
        with col2:
            st.markdown("Output")
            with st.expander(""):
                st.markdown("", unsafe_allow_html=True)
    elif layout == "Vertical":
        st.markdown("Input")
        make_input("foo")
        st.markdown("Output")
        with st.expander(""):
            st.markdown("", unsafe_allow_html=True)
