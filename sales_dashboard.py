import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from views import show_data_input_view, show_overview_view, show_sales_team_view, show_detailed_data_view, show_login_page
from auth import check_password, init_session_state
import os
import glob
import time

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

def load_data():
    """Load and process the sales data"""
    try:
        # Check if data file exists
        if not os.path.exists("sales_data.xlsx"):
            st.warning("No data file found. Please upload data first.")
            return pd.DataFrame()  # Return empty dataframe if no file exists
        
        # Read the Excel file
        df = pd.read_excel("sales_data.xlsx")
        
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
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()  # Return empty dataframe on error

def main():
    # Check if user is locked out
    if st.session_state.locked_until > time.time():
        remaining_time = int(st.session_state.locked_until - time.time())
        st.error(f"Account locked. Please try again in {remaining_time} seconds.")
        return

    # Show login form if not authenticated
    if not st.session_state.authenticated:
        show_login_page()
        return

    # Main dashboard content
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Sales Team", "Meeting Data"])

    # Load data
    df = load_data()

    if page == "Overview":
        show_overview_view(df)
    elif page == "Sales Team":
        show_sales_team_view(df)
    elif page == "Meeting Data":
        show_meeting_data_view()

def show_meeting_data_view():
    """Display the Meeting Data Viewer section"""
    st.markdown("""
        <div style='
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 15px;
            margin: 25px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        '>
            <h3 style='
                color: #2a5298;
                margin: 0;
                font-size: 1.4em;
                font-weight: 600;
                font-family: "Segoe UI", sans-serif;
            '>📊 Meeting Data Viewer</h3>
        </div>
    """, unsafe_allow_html=True)

    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # File upload section
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">📤 Upload New Meeting Data</h4>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx'],
        help="Upload your meeting data in Excel format"
    )

    if uploaded_file is not None:
        try:
            # Generate filename with current date
            current_date = datetime.now().strftime("%Y-%m-%d")
            filename = f"meeting_{current_date}.xlsx"
            filepath = os.path.join("data", filename)
            
            # Save the file
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"File saved successfully as {filename}")
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")

    # File selection section
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">📂 Select Meeting Data</h4>', unsafe_allow_html=True)

    # Get list of files in data directory
    files = glob.glob(os.path.join("data", "meeting_*.xlsx"))
    files.sort(key=os.path.getmtime, reverse=True)  # Sort by most recent

    if not files:
        st.warning("No meeting data files found in the data directory.")
    else:
        # Create dropdown with filenames
        selected_file = st.selectbox(
            "Select a file",
            options=files,
            format_func=lambda x: os.path.basename(x)
        )

        if selected_file:
            try:
                # Read the Excel file
                df = pd.read_excel(
                    selected_file,
                    sheet_name="Quarter Summary Dashboard",
                    skiprows=2,
                    usecols="B:T"
                )
                
                # Display the data
                st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">📋 Meeting Data</h4>', unsafe_allow_html=True)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
            except ValueError as e:
                if "Worksheet named" in str(e):
                    st.error("The selected file does not contain a sheet named 'Quarter Summary Dashboard'.")
                else:
                    st.error(f"Error reading file: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
