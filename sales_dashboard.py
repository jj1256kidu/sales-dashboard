import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from views import show_data_input_view, show_overview_view, show_sales_team_view, show_detailed_data_view
from auth import check_password, init_session_state, show_login_page
from quarterly_dashboard import load_excel_data, calculate_summaries, create_comparison_df, style_dataframe
import os
import glob
import time
from io import StringIO
from pathlib import Path
import random

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

def show_data_input_view(df):
    """Display the data input section with both file upload and manual input options"""
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
            '>📥 Data Input</h3>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📄 File Upload", "✏️ Manual Input"])

    with tab1:
        st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Upload Excel File</h4>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx'],
            help="Upload your sales data in Excel format"
        )
        if uploaded_file is not None:
            return uploaded_file

    with tab2:
        st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Manual Data Input</h4>', unsafe_allow_html=True)
        
        # Create a form for manual data input
        with st.form("manual_data_form"):
            # Get the number of rows to input
            num_rows = st.number_input("Number of records to add", min_value=1, max_value=100, value=5)
            
            # Create input fields for each row
            manual_data = []
            for i in range(num_rows):
                st.markdown(f"### Record {i+1}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    org_name = st.text_input(f"Organization Name {i+1}", key=f"org_{i}")
                    amount = st.number_input(f"Amount {i+1}", min_value=0, key=f"amount_{i}")
                with col2:
                    sales_owner = st.text_input(f"Sales Owner {i+1}", key=f"owner_{i}")
                    probability = st.number_input(f"Probability {i+1}", min_value=0, max_value=100, key=f"prob_{i}")
                with col3:
                    close_date = st.date_input(f"Expected Close Date {i+1}", key=f"date_{i}")
                    sales_stage = st.selectbox(f"Sales Stage {i+1}", 
                                             ["Prospecting", "Qualification", "Proposal", "Negotiation", "Won", "Lost"],
                                             key=f"stage_{i}")
                
                # Store the data
                if org_name and sales_owner:  # Only add if required fields are filled
                    manual_data.append({
                        "Organization Name": org_name,
                        "Amount": amount,
                        "Sales Owner": sales_owner,
                        "Probability": probability,
                        "Expected Close Date": close_date,
                        "Sales Stage": sales_stage
                    })

            # Submit button
            submitted = st.form_submit_button("Save Manual Data")
            if submitted and manual_data:
                try:
                    # Convert to DataFrame
                    manual_df = pd.DataFrame(manual_data)
                    
                    # Save to Excel
                    manual_df.to_excel("manual_data.xlsx", index=False)
                    st.success("Manual data saved successfully!")
                    
                    # Load the data
                    df = load_data()
                    if not df.empty:
                        st.session_state.df = df
                        st.success("Data loaded successfully!")
                    else:
                        st.error("Failed to load the manual data. Please check the format.")
                except Exception as e:
                    st.error(f"Error saving manual data: {str(e)}")

    return None

def show_previous_data_view():
    """Display the previous data tracking section with copy-paste functionality"""
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
            '>📊 Previous Data Tracking</h3>
        </div>
    """, unsafe_allow_html=True)

    # Create a text area for pasting data
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">📋 Paste Your Excel Data</h4>', unsafe_allow_html=True)
    st.info("Copy and paste your entire Excel sheet data. The system will automatically detect the format.")
    
    # Text area for pasting data
    pasted_data = st.text_area(
        "Paste your Excel data here",
        height=400,
        help="Paste your entire Excel sheet data. The system will handle both tab and comma separators."
    )

    if pasted_data:
        try:
            # Clean the pasted data
            # Remove empty lines and normalize line endings
            cleaned_lines = [line.strip() for line in pasted_data.split('\n') if line.strip()]
            cleaned_data = '\n'.join(cleaned_lines)

            # Try to parse the cleaned data
            # First try with tab separator (Excel default)
            try:
                df = pd.read_csv(StringIO(cleaned_data), sep='\t', na_values=['', 'NA', 'N/A', 'NULL', 'null', 'None', 'none'])
            except:
                # If tab fails, try comma
                try:
                    df = pd.read_csv(StringIO(cleaned_data), sep=',', na_values=['', 'NA', 'N/A', 'NULL', 'null', 'None', 'none'])
                except:
                    # If both fail, try to parse with python engine
                    df = pd.read_csv(StringIO(cleaned_data), sep=None, engine='python', na_values=['', 'NA', 'N/A', 'NULL', 'null', 'None', 'none'])

            # Clean up the dataframe
            # Replace empty strings with NaN
            df = df.replace('', np.nan)
            # Convert numeric columns, keeping original values if conversion fails
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass

            # Display the dataframe
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Error parsing data: {str(e)}")
            st.info("""
                Tips for pasting Excel data:
                1. Copy the entire sheet (Ctrl+A, Ctrl+C)
                2. Make sure headers are included
                3. The system will automatically detect the format
                4. If parsing fails, try copying a smaller section first
            """)

def show_quarterly_summary():
    """Display the quarterly summary dashboard"""
    st.markdown("""
        <div class="custom-header">
            <h1>📊 Quarterly Summary Dashboard</h1>
            <p>Track and compare sales performance across weeks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create sidebar for file selection
    st.sidebar.title("Data Source")
    data_source = st.sidebar.radio("Select data source:", ["File Upload", "Data Folder"])
    
    current_df = None
    previous_df = None
    
    if data_source == "File Upload":
        uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=['xlsx'])
        if uploaded_file:
            st.write("Processing uploaded file...")
            current_df, previous_df = load_excel_data(uploaded_file)
    else:
        data_folder = Path("data")
        if not data_folder.exists():
            data_folder.mkdir()
            st.info("Created data folder. Please add your Excel files here.")
        
        files = list(data_folder.glob("*.xlsx"))
        if files:
            selected_file = st.sidebar.selectbox("Select file:", files)
            if selected_file:
                st.write(f"Processing file: {selected_file}")
                current_df, previous_df = load_excel_data(selected_file)
        else:
            st.warning("No Excel files found in the data folder. Please add your Excel files to the 'data' folder.")
            return
    
    if current_df is not None and previous_df is not None:
        try:
            # Calculate summaries
            st.write("Calculating summaries...")
            sales_df, function_df = calculate_summaries(current_df, previous_df)
            
            # Create comparison dataframes
            st.write("Creating comparison views...")
            sales_comparison = create_comparison_df(sales_df, 'Sales Owner')
            function_comparison = create_comparison_df(function_df, 'Function')
            
            # Display Sales Owner Summary
            st.markdown('<h2 style="color: #2a5298;">👤 Sales Owner Summary</h2>', unsafe_allow_html=True)
            st.dataframe(style_dataframe(sales_comparison), use_container_width=True)
            
            # Display Function Overview
            st.markdown('<h2 style="color: #2a5298;">🏢 Function Overview</h2>', unsafe_allow_html=True)
            st.dataframe(style_dataframe(function_comparison), use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.error("Please check your data format and try again.")
    else:
        st.info("Please upload or select an Excel file to view the dashboard.")

def main():
    # Initialize session state
    init_session_state()
    
    # Check if user is logged in
    if not st.session_state.get('is_logged_in', False):
        show_login_page()
        return
    
    # Create sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Data Input", "Overview", "Sales Team", "Quarterly Summary", "Previous Data"])
    
    # Load data if not in session state
    if 'df' not in st.session_state or st.session_state.df is None:
        st.session_state.df = load_data()
    
    # Display selected page
    if page == "Data Input":
        uploaded_file = show_data_input_view(st.session_state.df)
        if uploaded_file is not None:
            try:
                # Save the uploaded file
                with open("sales_data.xlsx", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("File uploaded successfully!")
                
                # Reload the data
                st.session_state.df = load_data()
                if not st.session_state.df.empty:
                    st.success("Data loaded successfully!")
                else:
                    st.error("Failed to load the uploaded data. Please check the format.")
            except Exception as e:
                st.error(f"Error processing uploaded file: {str(e)}")
    elif page == "Overview":
        if st.session_state.df is not None and not st.session_state.df.empty:
            show_overview_view(st.session_state.df)
        else:
            st.warning("No data available. Please upload data first.")
    elif page == "Sales Team":
        if st.session_state.df is not None and not st.session_state.df.empty:
            show_sales_team_view(st.session_state.df)
        else:
            st.warning("No data available. Please upload data first.")
    elif page == "Quarterly Summary":
        if st.session_state.df is not None and not st.session_state.df.empty:
            show_quarterly_summary()
        else:
            st.warning("No data available. Please upload data first.")
    elif page == "Previous Data":
        if st.session_state.df is not None and not st.session_state.df.empty:
            show_previous_data_view()
        else:
            st.warning("No data available. Please upload data first.")

if __name__ == "__main__":
    main()
