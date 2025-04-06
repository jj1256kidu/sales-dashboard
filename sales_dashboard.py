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
from io import StringIO

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

            # Display the parsed data
            st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">📊 Data Preview</h4>', unsafe_allow_html=True)
            
            # Show data info
            st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
            st.write("Columns:", df.columns.tolist())

            # Add filtering options
            st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">🔍 Filter Data</h4>', unsafe_allow_html=True)
            
            # Create filter columns
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                # Column selector
                selected_columns = st.multiselect(
                    "Select columns to display",
                    options=df.columns.tolist(),
                    default=df.columns.tolist()
                )
            
            with filter_col2:
                # Row limit
                row_limit = st.number_input(
                    "Maximum rows to display",
                    min_value=1,
                    max_value=len(df),
                    value=min(100, len(df))
                )

            # Apply filters
            filtered_df = df[selected_columns].head(row_limit)

            # Display the filtered dataframe with formatting
            st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">📋 Table View</h4>', unsafe_allow_html=True)
            
            # Apply some basic formatting
            styled_df = filtered_df.style.format({
                col: '{:,.0f}' for col in filtered_df.select_dtypes(include=['int64', 'float64']).columns
            }).set_properties(**{
                'text-align': 'left',
                'padding': '5px'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#2a5298'), ('color', 'white')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#f8f9fa')]},
                {'selector': 'tr:hover', 'props': [('background-color', '#e9ecef')]}
            ])

            # Display the styled dataframe
            st.dataframe(styled_df, use_container_width=True)

            # Add download buttons
            st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">💾 Export Options</h4>', unsafe_allow_html=True)
            
            # Create two columns for export options
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Export as Excel"):
                    # Generate filename with current date
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    filename = f"previous_data_{current_date}.xlsx"
                    
                    # Save the data
                    filtered_df.to_excel(filename, index=False)
                    st.success(f"Data exported successfully as {filename}")
                    
                    # Store in session state
                    st.session_state.previous_data = filtered_df
                    st.success("Data loaded into memory")

            with col2:
                if st.button("Export as CSV"):
                    # Generate filename with current date
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    filename = f"previous_data_{current_date}.csv"
                    
                    # Save the data
                    filtered_df.to_csv(filename, index=False)
                    st.success(f"Data exported successfully as {filename}")
                    
                    # Store in session state
                    st.session_state.previous_data = filtered_df
                    st.success("Data loaded into memory")

        except Exception as e:
            st.error(f"Error parsing data: {str(e)}")
            st.info("""
                Tips for pasting Excel data:
                1. Copy the entire sheet (Ctrl+A, Ctrl+C)
                2. Make sure headers are included
                3. The system will automatically detect the format
                4. If parsing fails, try copying a smaller section first
            """)

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
    page = st.sidebar.radio("Go to", ["Data Input", "Overview", "Sales Team", "Previous Data"])

    # Initialize session state for data if not exists
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'previous_data' not in st.session_state:
        st.session_state.previous_data = None

    # Load or get data based on page
    if page in ["Overview", "Sales Team"]:
        # Try to get data from session state first
        if st.session_state.df is not None and not st.session_state.df.empty:
            df = st.session_state.df
        else:
            # Try to load from file
            df = load_data()
            if df.empty:
                st.warning("Please upload sales data in the Data Input section first.")
                # Switch to Data Input page
                page = "Data Input"
                st.experimental_rerun()

    # Show appropriate view based on selection
    if page == "Data Input":
        # Show data input view and handle file upload
        uploaded_file = show_data_input_view(None)
        if uploaded_file is not None:
            try:
                # Save the uploaded file
                with open("sales_data.xlsx", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("Data uploaded successfully!")
                
                # Load the new data
                df = load_data()
                if not df.empty:
                    st.session_state.df = df
                    st.success("Data loaded successfully!")
                else:
                    st.error("Failed to load the uploaded data. Please check the file format.")
            except Exception as e:
                st.error(f"Error saving file: {str(e)}")
    elif page == "Overview":
        show_overview_view(df)
    elif page == "Sales Team":
        show_sales_team_view(df)
    elif page == "Previous Data":
        show_previous_data_view()

if __name__ == "__main__":
    main()
