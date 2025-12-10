import streamlit as st
from streamlit_option_menu import option_menu
import menu_functional_specs_ui as menu_functional_specs_ui
import menu_preprocessor_ui as menu_preprocessor_ui
import menu_preprocessor_ui_calling_restapi as menu_preprocessor_ui_calling_restapi
import os

st.set_page_config(layout="wide")
css_path = os.path.join(os.path.dirname(__file__), 'design.css')
with open(css_path) as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True) 

st.markdown("<div class='main-title'>CodeSpectre</div>", unsafe_allow_html=True)
st.markdown("<div class='main-sub-title'>Java Application Modernization powered by Generative AI</div>", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options =["Preprocess", "Functional Specification"],
        icons=['gear', 'file-earmark-text'],
        menu_icon="grid-fill",
        default_index=0,
        # styles={
        #     "container": {"padding": "1px", "background-color": "#3B446B"},
        # }
        styles={
            "container": {"padding": "1px", "background-color": "#3B446B"},
            "nav-link": { # Style for the entire menu item (icon + text)
                "font-size": "16px",
                "text-align": "left",
                "margin":"0px",
                "--hover-color": "#eee",
                "display": "flex",        # Use flexbox for alignment
                "align-items": "center",  # Vertically center icon and text
            },
            "nav-link-text": { # Style specifically for the text label
                "white-space": "nowrap",  # Prevent text from wrapping
                "padding-left": "10px",   # Add some space between icon and text
            },
            "icon": { # Style for the icon itself
                "font-size": "20px",
                "padding-right": "5px"
            }
        }
    )

# Routing to appropriate pages
if selected == "Functional Specification":
    menu_functional_specs_ui.app()
if selected == "Preprocess":
    # menu_preprocessor_ui.app()
    menu_preprocessor_ui_calling_restapi.app()