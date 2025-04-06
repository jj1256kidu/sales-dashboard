import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os
from views import show_data_input_view, show_overview_view, show_sales_team_view, show_detailed_data_view, show_login_page
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
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'data_input'
if 'sales_target' not in st.session_state:
    st.session_state.sales_target = 0.0
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'last_attempt' not in st.session_state:
    st.session_state.last_attempt = 0
if 'locked_until' not in st.session_state:
    st.session_state.locked_until = 0
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

def load_data():
    """Load and process the sales data"""
    try:
        # Check if data file exists
        if not os.path.exists("sales_data.xlsx"):
            st.warning("No data file found. Please upload data first.")
            return pd.DataFrame()  # Return empty dataframe if no file exists
        
        # Read the Excel file
        df = pd.read_excel("sales_data.xlsx")
        
        # Check if dataframe is empty
        if df.empty:
            st.warning("The data file is empty. Please upload valid data.")
            return pd.DataFrame()
            
        # Check for required columns
        required_columns = ['Expected Close Date', 'Year in FY', 'Probability', 
                          'Sales Stage', 'Amount', 'Sales Owner']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        # Process dates and calculate time-based columns
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
        df['Month'] = df['Expected Close Date'].dt.strftime('%B')
        df['Year'] = df['Year in FY']  # Use Year in FY directly
        df['Quarter'] = df['Expected Close Date'].dt.quarter.map({1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
        
        # Convert probability and calculate numeric values
        def convert_probability(x):
            try:
                if pd.isna(x):
                    return 0
                if isinstance(x, str):
                    x = x.rstrip('%')
                return float(x)
            except:
                return 0
        
        df['Probability_Num'] = df['Probability'].apply(convert_probability)
        
        # Pre-calculate common flags and metrics
        df['Is_Won'] = df['Sales Stage'].str.contains('Won', case=False, na=False)
        df['Amount_Lacs'] = df['Amount'].fillna(0).div(100000).round(0).astype(int)
        df['Weighted_Amount'] = (df['Amount_Lacs'] * df['Probability_Num'] / 100).round(0).astype(int)
        
        # Store the processed dataframe in session state
        st.session_state.df = df
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()  # Return empty dataframe on error

def main():
    # Check authentication
    if not st.session_state.authenticated:
        show_login_page()
        return

    # Load data if not in session state
    if st.session_state.df is None:
        st.session_state.df = load_data()

    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        selected = st.radio(
            "Select View",
            options=["Data Input", "Overview", "Sales Team", "Detailed Data"],
            key="navigation"
        )
        st.session_state.current_view = selected.lower().replace(" ", "_")
        
        # Logout button
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # Main content
    if st.session_state.current_view == "data_input":
        show_data_input_view(st.session_state.df)
    elif st.session_state.current_view == "overview":
        show_overview_view(st.session_state.df)
    elif st.session_state.current_view == "sales_team":
        show_sales_team_view(st.session_state.df)
    elif st.session_state.current_view == "detailed_data":
        show_detailed_data_view(st.session_state.df)

if __name__ == "__main__":
    main()
