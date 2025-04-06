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

def load_excel_data(file_path):
    """Load and process Excel data from both sheets"""
    try:
        # Read both sheets
        st.write("Loading Excel file...")
        current_df = pd.read_excel(file_path, sheet_name="Raw_Data")
        previous_df = pd.read_excel(file_path, sheet_name="Previous Data")
        
        st.write("Raw_Data columns:", current_df.columns.tolist())
        st.write("Previous Data columns:", previous_df.columns.tolist())
        
        # Select required columns
        required_columns = ['Sales Owner', 'Committed', 'Upside', 'Closed Won', 'Function']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in current_df.columns]
        if missing_columns:
            st.error(f"Missing required columns in Raw_Data: {missing_columns}")
            return None, None
            
        missing_columns = [col for col in required_columns if col not in previous_df.columns]
        if missing_columns:
            st.error(f"Missing required columns in Previous Data: {missing_columns}")
            return None, None
        
        # Process current week data
        current_df = current_df[required_columns].copy()
        current_df['Week'] = 'Current'
        
        # Process previous week data
        previous_df = previous_df[required_columns].copy()
        previous_df['Week'] = 'Previous'
        
        st.write("Data loaded successfully!")
        return current_df, previous_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error("Please make sure your Excel file has two sheets named 'Raw_Data' and 'Previous Data'")
        return None, None

def calculate_summaries(current_df, previous_df):
    """Calculate summaries for both Sales Owner and Function groups"""
    # Combine current and previous data
    combined_df = pd.concat([current_df, previous_df])
    
    # Group by Sales Owner
    sales_df = combined_df.groupby(['Sales Owner', 'Week']).agg({
        'Committed': 'sum',
        'Upside': 'sum',
        'Closed Won': 'sum'
    }).reset_index()
    
    # Group by Function
    function_df = combined_df.groupby(['Function', 'Week']).agg({
        'Committed': 'sum',
        'Upside': 'sum',
        'Closed Won': 'sum'
    }).reset_index()
    
    return sales_df, function_df

def create_comparison_df(df, group_column):
    """Create a comparison dataframe with current, previous, and delta values"""
    # Pivot the data
    pivot_df = df.pivot(index=group_column, columns='Week', values=['Committed', 'Upside', 'Closed Won'])
    
    # Calculate deltas
    for metric in ['Committed', 'Upside', 'Closed Won']:
        pivot_df[(metric, 'Delta')] = pivot_df[(metric, 'Current')] - pivot_df[(metric, 'Previous')]
    
    # Calculate total (Committed + Closed Won)
    pivot_df[('Total', 'Current')] = pivot_df[('Committed', 'Current')] + pivot_df[('Closed Won', 'Current')]
    pivot_df[('Total', 'Previous')] = pivot_df[('Committed', 'Previous')] + pivot_df[('Closed Won', 'Previous')]
    pivot_df[('Total', 'Delta')] = pivot_df[('Total', 'Current')] - pivot_df[('Total', 'Previous')]
    
    return pivot_df

def style_dataframe(df):
    """Style the dataframe with color highlights for deltas"""
    def color_delta(val):
        if isinstance(val, (int, float)):
            if val < 0:
                return 'color: red'
            elif val > 0:
                return 'color: green'
        return ''
    
    styled_df = df.style.applymap(color_delta, subset=pd.IndexSlice[:, [('Committed', 'Delta'), 
                                                                       ('Upside', 'Delta'),
                                                                       ('Closed Won', 'Delta'),
                                                                       ('Total', 'Delta')]])
    
    # Format numbers
    for col in df.columns:
        if col[1] != 'Delta':
            styled_df = styled_df.format({col: '{:,.0f}'})
        else:
            styled_df = styled_df.format({col: '{:+,.0f}'})
    
    return styled_df

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

def show_login_page():
    """Display the login page"""
    # Hide sidebar and main menu
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Override Streamlit defaults */
            .stApp {
                background: #0B0B1E !important;
            }
            
            .block-container {
                padding: 0 !important;
                max-width: 100% !important;
            }

            /* Custom styles for form elements */
            [data-testid="stTextInput"] > div > div > input {
                background-color: #000 !important;
                border: 2px solid #00F5FF !important;
                border-radius: 25px !important;
                color: #00F5FF !important;
                font-size: 1em !important;
                padding: 12px 25px !important;
                font-family: 'Orbitron', sans-serif !important;
                box-shadow: 0 0 10px rgba(0, 245, 255, 0.3) !important;
            }

            [data-testid="stTextInput"] > div > div > input:focus {
                border-color: #00F5FF !important;
                box-shadow: 0 0 20px rgba(0, 245, 255, 0.5) !important;
            }

            [data-testid="stTextInput"] > div > div > input::placeholder {
                color: rgba(0, 245, 255, 0.5) !important;
            }

            [data-testid="stButton"] > button {
                width: 100% !important;
                background: linear-gradient(90deg, #00F5FF, #FF00FF) !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 12px !important;
                font-size: 1.1em !important;
                border-radius: 25px !important;
                border: none !important;
                transition: all 0.3s ease !important;
                font-family: 'Orbitron', sans-serif !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
            }

            [data-testid="stButton"] > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 0 30px rgba(0, 245, 255, 0.5) !important;
            }

            /* Base layout */
            .main {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                font-family: 'Orbitron', sans-serif;
            }

            /* Container and login box */
            .container {
                width: 100%;
                max-width: 400px;
                margin: 0 auto;
                position: relative;
                z-index: 1;
            }

            .login-box {
                background: rgba(0, 0, 0, 0.8);
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 0 50px rgba(0, 245, 255, 0.3);
                border: 2px solid #00F5FF;
            }

            /* Title */
            .login-box h1 {
                color: #00F5FF;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5em;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
                font-family: 'Orbitron', sans-serif;
            }

            /* Remember me and Forgot password */
            .options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
                color: #00F5FF;
                font-size: 0.9em;
            }

            .remember-me {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .remember-me input[type="checkbox"] {
                accent-color: #00F5FF;
            }

            .forgot-password {
                color: #00F5FF;
                text-decoration: none;
                transition: all 0.3s ease;
            }

            .forgot-password:hover {
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
            }

            /* Particles */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                pointer-events: none;
            }

            .particle {
                position: fixed;
                width: 5px;
                height: 5px;
                border-radius: 50%;
                animation: particle-animation 20s infinite linear;
            }

            @keyframes particle-animation {
                0% {
                    transform: translateY(100vh) translateX(0) scale(0);
                    opacity: 0;
                }
                50% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100vh) translateX(100px) scale(1);
                    opacity: 0;
                }
            }

            /* Generate multiple particles with different colors */
            .particle:nth-child(3n) { background: #00F5FF; }
            .particle:nth-child(3n+1) { background: #FF00FF; }
            .particle:nth-child(3n+2) { background: #FFD700; }
        </style>
    """, unsafe_allow_html=True)

    # Generate particles HTML
    particles_html = ""
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.randint(0, 20)
        duration = random.randint(15, 25)
        particles_html += f'<div class="particle" style="left: {left}vw; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'

    # Create the main container with particles
    st.markdown(f"""
        <div class="main">
            <div class="particles">
                {particles_html}
            </div>
            <div class="container">
                <div class="login-box">
                    <h1>Welcome Back</h1>
                    <div id="login-form">
    """, unsafe_allow_html=True)

    # Create columns for centering the form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Add custom font
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        """, unsafe_allow_html=True)

        # Password input
        password = st.text_input("", value="", placeholder="Enter Password", type="password", key="login_password", label_visibility="collapsed")

        if st.button("LOGIN", key="login_button"):
            if check_password():
                st.rerun()

        # Remember me and Forgot password
        st.markdown("""
            <div class="options">
                <label class="remember-me">
                    <input type="checkbox" checked>
                    Remember me
                </label>
                <a href="#" class="forgot-password">Forgot password?</a>
            </div>
        """, unsafe_allow_html=True)

    # Close the containers
    st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
    if 'df' not in st.session_state:
        st.session_state.df = load_data()
    
    # Display selected page
    if page == "Data Input":
        show_data_input_view(st.session_state.df)
    elif page == "Overview":
        show_overview_view(st.session_state.df)
    elif page == "Sales Team":
        show_sales_team_view(st.session_state.df)
    elif page == "Quarterly Summary":
        show_quarterly_summary()
    elif page == "Previous Data":
        show_previous_data_view()

if __name__ == "__main__":
    main()
