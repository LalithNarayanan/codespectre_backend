import streamlit as st
from streamlit_option_menu import option_menu
import menu_upload_code
import menu_functional_specs
import menu_oo_design
import menu_code
from utils.job_util import get_job_run_id_persistent, load_job_run_state
import os

st.set_page_config(layout="wide")
css_path = os.path.join(os.path.dirname(__file__), 'design.css')
with open(css_path) as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True) 

st.markdown("<div class='main-title'>CodeSpectre</div>", unsafe_allow_html=True)
st.markdown("<div class='main-sub-title'>Mainframe Application Modernization powered by Generative AI</div>", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Upload Source Code", "Functional Specification", "Design Docs", "Code"],
        icons=['cloud-upload', 'file-earmark-text', 'diagram-3-fill', 'file-code'],
        menu_icon="grid-fill",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#3B446B"},
            # "icon": {"color": "#003C74", "font-size": "20px"},
            # "nav-link": {"font-size": "16px", "text-align": "left", "margin": "2px", "color":"#000"},
            # "nav-link-selected": {"background-color": "#003C74", "color": "white"},
        }
    )

# Routing to appropriate pages
if selected == "Upload Source Code":
    menu_upload_code.app()
elif selected == "Functional Specification":
    menu_functional_specs.app()
elif selected == "Design Docs":
    menu_oo_design.app()
elif selected == "Code":
    menu_code.app()
