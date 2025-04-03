import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from views import show_data_input_view, show_overview_view, show_sales_team_view, show_detailed_data_view
from auth import check_password, init_session_state

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .custom-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .custom-header h1 {
        color: white;
        margin: 0;
        text-align: center;
        font-size: 2.2em;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .custom-header p {
        color: white;
        margin: 10px 0 0 0;
        text-align: center;
        font-size: 1.2em;
        opacity: 0.9;
    }
    .upload-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .info-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .info-box h4 {
        color: #2a5298;
        margin: 0 0 15px 0;
        font-size: 1.2em;
        font-weight: 600;
    }
    .info-box ul {
        margin: 0;
        padding-left: 20px;
        color: #666;
    }
    .info-box li {
        margin: 8px 0;
    }
    .metric-label {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #2a5298;
        font-size: 2em;
        font-weight: 700;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Sidebar
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Select a page",
        ["Data Input", "Overview", "Sales Team", "Detailed Data"]
    )
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Main content
if st.session_state.authenticated:
    if page == "Data Input":
        show_data_input_view(st.session_state.get('df'))
    elif page == "Overview":
        show_overview_view(st.session_state.get('df'))
    elif page == "Sales Team":
        show_sales_team_view(st.session_state.get('df'))
    elif page == "Detailed Data":
        show_detailed_data_view(st.session_state.get('df'))
else:
    check_password()
