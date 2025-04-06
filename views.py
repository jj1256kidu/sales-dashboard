import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time
import hashlib
import secrets
import re
import logging
import json
import random
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User database (in production, use a proper database)
USERS = {
    "admin": {
        "password": "admin123",  # This will be hashed when saved
        "role": "admin",
        "last_login": None,
        "failed_attempts": 0
    }
}

def init_session_state():
    """Initialize session state variables"""
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    if 'last_attempt' not in st.session_state:
        st.session_state.last_attempt = 0
    if 'locked_until' not in st.session_state:
        st.session_state.locked_until = 0
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'role' not in st.session_state:
        st.session_state.role = None

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default admin user if file doesn't exist
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin"
            }
        }
        with open('users.json', 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

def verify_password(username: str, password: str) -> bool:
    """Verify user credentials"""
    users = load_users()
    if username in users:
        hashed_password = hash_password(password)
        return hashed_password == users[username]["password"]
    return False

def check_password():
    """Check if the password is correct"""
    # Check if account is locked
    if st.session_state.locked_until > time.time():
        remaining_time = int(st.session_state.locked_until - time.time())
        st.error(f"Account locked. Please try again in {remaining_time} seconds.")
        return False

    # Get username and password from session state
    username = st.session_state.get('login_username', '')
    password = st.session_state.get('login_password', '')

    # Check if both username and password are provided
    if not username or not password:
        st.error("Please enter both username and password")
        return False

    # Check credentials
    if verify_password(username, password):
        st.session_state.is_logged_in = True
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = load_users()[username]["role"]
        st.session_state.login_attempts = 0
        st.session_state.last_attempt = 0
        st.session_state.locked_until = 0
        logger.info(f"Successful login for user: {username}")
        return True
    else:
        # Increment login attempts
        st.session_state.login_attempts += 1
        st.session_state.last_attempt = time.time()
        
        # Check if account should be locked
        if st.session_state.login_attempts >= 3:
            st.session_state.locked_until = time.time() + 300  # Lock for 5 minutes
            st.error("Too many failed attempts. Account locked for 5 minutes.")
        else:
            st.error("Invalid username or password")
        
        logger.warning(f"Failed login attempt for user: {username}")
        return False

def show_login_page():
    """Display the login page with username and password fields"""
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
                background-color: rgba(0, 0, 0, 0.5) !important;
                border: 2px solid #00F5FF !important;
                border-radius: 25px !important;
                color: #00F5FF !important;
                font-size: 1em !important;
                padding: 12px 25px !important;
                font-family: 'Orbitron', sans-serif !important;
                box-shadow: 0 0 10px rgba(0, 245, 255, 0.3) !important;
                margin-bottom: 15px !important;
                width: 100% !important;
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
                margin-top: 20px !important;
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

            /* Title and subtitle */
            .login-box h1 {
                color: #00F5FF;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
                font-family: 'Orbitron', sans-serif;
            }

            .login-box p {
                color: rgba(0, 245, 255, 0.7);
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.1em;
            }

            /* Form elements */
            .form-group {
                margin-bottom: 20px;
            }

            .form-group label {
                display: block;
                color: #00F5FF;
                margin-bottom: 8px;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
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
                    <p>Please sign in to continue</p>
                    <div id="login-form">
    """, unsafe_allow_html=True)

    # Add custom font
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Create columns for centering the form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Username input
        st.markdown('<div class="form-group"><label>Username</label></div>', unsafe_allow_html=True)
        username = st.text_input("", value="", placeholder="Enter your username", key="login_username", label_visibility="collapsed")

        # Password input
        st.markdown('<div class="form-group"><label>Password</label></div>', unsafe_allow_html=True)
        password = st.text_input("", value="", placeholder="Enter your password", type="password", key="login_password", label_visibility="collapsed")

        if st.button("SIGN IN", key="login_button"):
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

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user():
    """Get current user's username"""
    return st.session_state.get("username") if is_authenticated() else None

def logout():
    """Logout the current user"""
    logger.info(f"User logged out: {st.session_state.username}")
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Reinitialize authentication state
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["role"] = None

def require_authentication(roles=None):
    """Decorator to require authentication for view functions with optional role-based access"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                show_login_page()
                return
            
            # Check role-based access if specified
            if roles and st.session_state.role not in roles:
                st.error("You don't have permission to access this page.")
                return
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Format helper functions
def format_amount(value):
    """Format amount in lakhs"""
    if pd.isna(value):
        return "₹0L"
    return f"₹{int(value/100000)}L"

def format_percentage(value):
    """Format percentage"""
    if pd.isna(value):
        return "0%"
    return f"{int(value)}%"

def format_number(value):
    """Format number with commas"""
    if pd.isna(value):
        return "0"
    return f"{int(value):,}"

# Custom CSS for the dashboard
st.markdown("""
    <style>
        /* Main container */
        .main {
            background-color: #f8f9fa;
            padding: 2rem;
        }
        
        /* Cards */
        .stCard {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #4A90E2;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            border: none;
            transition: background-color 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #357ABD;
        }
        
        /* Metrics */
        .metric-label {
            font-size: 1rem;
            color: #666;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .big-number {
            font-size: 3rem;
            font-weight: 700;
            color: #2c3e50;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* Tables */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        
        .stDataFrame table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .stDataFrame th {
            background-color: #4A90E2;
            color: white;
            font-weight: 500;
            padding: 0.75rem;
            text-align: left;
        }
        
        .stDataFrame td {
            padding: 0.75rem;
            border-bottom: 1px solid #eee;
        }
        
        .stDataFrame tr:hover {
            background-color: #f8f9fa;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 0.5rem;
        }
        
        /* Charts */
        .stPlotlyChart {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 1rem;
            color: #666;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            color: #4A90E2;
            font-weight: 600;
        }
        
        /* File uploader */
        .stFileUploader {
            border: 2px dashed #ddd;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
        }
        
        /* Success/Error messages */
        .stAlert {
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .element-container .stAlert {
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Cache data processing functions
@st.cache_data
def process_data(df):
    """Process and clean the data"""
    if df is None:
        return None
    
    # Make a copy of the DataFrame
    processed_df = df.copy()
    
    # Convert date columns
    if 'Expected Close Date' in processed_df.columns:
        processed_df['Expected Close Date'] = pd.to_datetime(processed_df['Expected Close Date'])
    
    # Convert amount to numeric
    if 'Amount' in processed_df.columns:
        processed_df['Amount'] = pd.to_numeric(processed_df['Amount'], errors='coerce')
    
    # Convert probability to numeric
    if 'Probability' in processed_df.columns:
        processed_df['Probability'] = pd.to_numeric(processed_df['Probability'], errors='coerce')
        processed_df['Probability'] = processed_df['Probability'].fillna(0)
    
    # Clean text columns
    text_columns = ['Practice', 'Team', 'Sales Stage', 'Notes']
    for col in text_columns:
        if col in processed_df.columns:
            processed_df[col] = processed_df[col].astype(str).str.strip()
            processed_df[col] = processed_df[col].replace('nan', '')
    
    return processed_df

@st.cache_data
def calculate_team_metrics(df):
    """Calculate team performance metrics"""
    if df is None:
        return None
    
    # Group by team and calculate metrics
    team_metrics = df.groupby('Team').agg({
        'Amount': [
            ('Total Pipeline', lambda x: x[~df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000),
            ('Closed Amount', lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000)
        ],
        'Sales Stage': [
            ('Pipeline Deals', lambda x: x[~df['Sales Stage'].str.contains('Won', case=False, na=False)].count()),
            ('Closed Deals', lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].count())
        ]
    }).reset_index()
    
    # Flatten column names
    team_metrics.columns = ['Team', 'Total Pipeline', 'Closed Amount', 'Pipeline Deals', 'Closed Deals']
    
    # Calculate additional metrics
    team_metrics['Win Rate'] = (team_metrics['Closed Deals'] / (team_metrics['Closed Deals'] + team_metrics['Pipeline Deals']) * 100).round(1)
    team_metrics['Avg Deal Size'] = (team_metrics['Closed Amount'] / team_metrics['Closed Deals']).round(1)
    
    # Replace inf and nan values
    team_metrics['Win Rate'] = team_metrics['Win Rate'].replace([np.inf, -np.inf], 0).fillna(0)
    team_metrics['Avg Deal Size'] = team_metrics['Avg Deal Size'].replace([np.inf, -np.inf], 0).fillna(0)
    
    # Sort by total pipeline
    team_metrics = team_metrics.sort_values('Total Pipeline', ascending=False)
    
    return team_metrics

@st.cache_data
def filter_dataframe(df, filters):
    """Filter the DataFrame based on the provided filters"""
    if df is None:
        return None
    
    # Make a copy of the DataFrame
    filtered_df = df.copy()
    
    # Apply filters
    for column, values in filters.items():
        if values and 'All' not in values:
            filtered_df = filtered_df[filtered_df[column].isin(values)]
    
    return filtered_df

@require_authentication()
def show_data_input_view():
    """Display the data input view"""
    # Initialize session state variables if they don't exist
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    st.title("Data Input")
    
    # File upload section
    st.subheader("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_excel(uploaded_file)
            
            # Validate required columns
            required_columns = ['Practice', 'Team', 'Sales Stage', 'Amount', 'Expected Close Date']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                # Validate data types
                try:
                    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
                    df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
                    
                    # Check for invalid data
                    invalid_amount = df['Amount'].isna().sum()
                    invalid_date = df['Expected Close Date'].isna().sum()
                    
                    if invalid_amount > 0 or invalid_date > 0:
                        st.warning(f"Found {invalid_amount} invalid amounts and {invalid_date} invalid dates. These rows will be excluded.")
                        df = df.dropna(subset=['Amount', 'Expected Close Date'])
                    
                    st.session_state.df = df
                    st.success("File uploaded successfully!")
                except Exception as e:
                    st.error(f"Error processing data: {str(e)}")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Manual input section
    st.subheader("Manual Input")
    
    if st.session_state.df is None:
        st.session_state.df = pd.DataFrame(columns=["Practice", "Team", "Sales Stage", "Amount", "Expected Close Date", "Probability", "Notes"])
    
    with st.form("manual_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            practice = st.text_input("Practice")
            team = st.text_input("Team")
            sales_stage = st.selectbox("Sales Stage", ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"])
            amount = st.number_input("Amount", min_value=0.0, step=1000.0)
        
        with col2:
            expected_close_date = st.date_input("Expected Close Date")
            probability = st.slider("Probability (%)", 0, 100, 50)
            notes = st.text_area("Notes")
        
        submit = st.form_submit_button("Add Data")
        
        if submit:
            try:
                # Validate input
                if not practice or not team or not sales_stage or amount <= 0:
                    st.error("Please fill in all required fields with valid values.")
                    return
                
                # Create new row
                new_row = pd.DataFrame([{
                    "Practice": practice,
                    "Team": team,
                    "Sales Stage": sales_stage,
                    "Amount": amount,
                    "Expected Close Date": pd.Timestamp(expected_close_date),
                    "Probability": probability,
                    "Notes": notes
                }])
                
                # Add to DataFrame
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                st.success("Data added successfully!")
            except Exception as e:
                st.error(f"Error adding data: {str(e)}")
    
    # Display current data
    if st.session_state.df is not None and not st.session_state.df.empty:
        st.subheader("Current Data")
        st.dataframe(st.session_state.df)
        
        # Download button
        csv = st.session_state.df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="sales_data.csv",
            mime="text/csv"
        )

def show_overview_view():
    """Display the overview section with key metrics and charts"""
    if st.session_state.df is None:
        st.warning("Please upload data to view the dashboard.")
        return
    
    st.title("Sales Performance Overview")
    
    # Process data
    df = process_data(st.session_state.df)
    
    # Sales target input
    target = st.number_input("Enter Sales Target (in lakhs)", min_value=0, value=1000)
    
    # Calculate metrics
    total_pipeline = df["Amount"].sum() / 100000
    closed_won = df[df["Sales Stage"] == "Closed Won"]["Amount"].sum() / 100000
    achievement_percentage = (closed_won / target) * 100 if target > 0 else 0
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipeline", f"₹{format_number(total_pipeline)}L")
    with col2:
        st.metric("Closed Won", f"₹{format_number(closed_won)}L")
    with col3:
        st.metric("Target", f"₹{format_number(target)}L")
    with col4:
        st.metric("Achievement", f"{format_percentage(achievement_percentage)}")
    
    # Practice metrics
    st.subheader("Practice Metrics")
    practice = st.selectbox("Select Practice", ["All"] + list(df["Practice"].unique()))
    
    if practice != "All":
        df = df[df["Practice"] == practice]
    
    # Practice summary
    practice_metrics = df.groupby("Practice").agg({
        "Amount": ["sum", "count"],
        "Sales Stage": lambda x: (x == "Closed Won").sum()
    }).reset_index()
    
    practice_metrics.columns = ["Practice", "Total Pipeline", "Pipeline Deals", "Closed Deals"]
    practice_metrics["Win Rate"] = (practice_metrics["Closed Deals"] / practice_metrics["Pipeline Deals"] * 100).round(1)
    practice_metrics["Average Deal Size"] = (practice_metrics["Total Pipeline"] / practice_metrics["Pipeline Deals"] / 100000).round(1)
    
    st.dataframe(practice_metrics)
    
    # KritiKal Focus Areas
    st.subheader("KritiKal Focus Areas")
    focus_areas = df.groupby("Practice")["Amount"].sum().sort_values(ascending=False)
    
    fig = go.Figure(data=[go.Pie(
        labels=focus_areas.index,
        values=focus_areas.values,
        hole=0.3
    )])
    
    fig.update_layout(
        title="Focus Areas Distribution",
        showlegend=True
    )
    
    st.plotly_chart(fig)
    
    # Monthly pipeline trend
    st.subheader("Monthly Pipeline Trend")
    deal_type = st.selectbox("Select Deal Type", ["All", "Closed Won", "Pipeline"])
    
    if deal_type != "All":
        df = df[df["Sales Stage"] == deal_type]
    
    monthly_trend = df.groupby(pd.Grouper(key="Expected Close Date", freq="M"))["Amount"].sum().reset_index()
    monthly_trend["Amount"] = monthly_trend["Amount"] / 100000
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly_trend["Expected Close Date"],
        y=monthly_trend["Amount"],
        name="Amount"
    ))
    
    fig.update_layout(
        title="Monthly Pipeline Trend",
        xaxis_title="Month",
        yaxis_title="Amount (in lakhs)",
        showlegend=True
    )
    
    st.plotly_chart(fig)
    
    # Monthly metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Value", f"₹{format_number(monthly_trend['Amount'].sum())}L")
    with col2:
        st.metric("Monthly Average", f"₹{format_number(monthly_trend['Amount'].mean())}L")
    with col3:
        st.metric("Total Deals", format_number(len(monthly_trend)))

def show_sales_team_view():
    """Display the sales team performance section"""
    if st.session_state.df is None:
        st.warning("Please upload data to view the dashboard.")
        return
    
    st.title("Sales Team Performance")
    
    # Process data
    df = process_data(st.session_state.df)
    
    # Calculate team metrics
    team_metrics = calculate_team_metrics(df)
    
    # Team selection
    team = st.selectbox("Select Team", ["All"] + list(df["Team"].unique()))
    
    if team != "All":
        df = df[df["Team"] == team]
        team_metrics = team_metrics[team_metrics.index == team]
    
    # Display team metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipeline", f"₹{format_number(team_metrics['Total Pipeline'].iloc[0] / 100000)}L")
    with col2:
        st.metric("Total Deals", format_number(team_metrics['Pipeline Deals'].iloc[0]))
    with col3:
        st.metric("Win Rate", format_percentage(team_metrics['Win Rate'].iloc[0]))
    with col4:
        st.metric("Average Deal Size", f"₹{format_number(team_metrics['Average Deal Size'].iloc[0])}L")
    
    # Team-wise charts
    st.subheader("Team Performance")
    
    # Pipeline vs Closed Won
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=team_metrics.index,
        y=team_metrics["Total Pipeline"] / 100000,
        name="Pipeline"
    ))
    fig.add_trace(go.Bar(
        x=team_metrics.index,
        y=team_metrics["Closed Amount"] / 100000,
        name="Closed Won"
    ))
    
    fig.update_layout(
        title="Pipeline vs Closed Won",
        xaxis_title="Team",
        yaxis_title="Amount (in lakhs)",
        barmode="group"
    )
    
    st.plotly_chart(fig)
    
    # Pipeline vs Closed Deals
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=team_metrics.index,
        y=team_metrics["Pipeline Deals"],
        name="Pipeline"
    ))
    fig.add_trace(go.Bar(
        x=team_metrics.index,
        y=team_metrics["Closed Deals"],
        name="Closed Won"
    ))
    
    fig.update_layout(
        title="Pipeline vs Closed Deals",
        xaxis_title="Team",
        yaxis_title="Number of Deals",
        barmode="group"
    )
    
    st.plotly_chart(fig)
    
    # Team-wise summary
    st.subheader("Team-wise Summary")
    team_summary = team_metrics.copy()
    team_summary["Total Pipeline"] = team_summary["Total Pipeline"] / 100000
    team_summary["Closed Amount"] = team_summary["Closed Amount"] / 100000
    
    st.dataframe(team_summary)

def show_detailed_data_view():
    """Display the detailed data view with filters and data table"""
    if st.session_state.df is None:
        st.warning("Please upload data to view the dashboard.")
        return
    
    st.title("Detailed Data View")
    
    # Process data
    df = process_data(st.session_state.df)
    
    # Filters
    st.subheader("Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        practice = st.multiselect("Practice", ["All"] + list(df["Practice"].unique()), default=["All"])
    with col2:
        team = st.multiselect("Team", ["All"] + list(df["Team"].unique()), default=["All"])
    with col3:
        sales_stage = st.multiselect("Sales Stage", ["All"] + list(df["Sales Stage"].unique()), default=["All"])
    
    # Apply filters
    filters = {
        "Practice": practice,
        "Team": team,
        "Sales Stage": sales_stage
    }
    
    filtered_df = filter_dataframe(df, filters)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipeline", f"₹{format_number(filtered_df['Amount'].sum() / 100000)}L")
    with col2:
        st.metric("Total Deals", format_number(len(filtered_df)))
    with col3:
        win_rate = (filtered_df[filtered_df["Sales Stage"] == "Closed Won"]["Amount"].sum() / filtered_df["Amount"].sum() * 100) if len(filtered_df) > 0 else 0
        st.metric("Win Rate", format_percentage(win_rate))
    with col4:
        avg_deal_size = (filtered_df["Amount"].sum() / len(filtered_df) / 100000) if len(filtered_df) > 0 else 0
        st.metric("Average Deal Size", f"₹{format_number(avg_deal_size)}L")
    
    # Display data table
    st.subheader("Data Table")
    st.dataframe(filtered_df)

def show_quarterly_summary():
    """Display the quarterly summary view"""
    # Initialize session state variables if they don't exist
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    if st.session_state.df is None:
        st.warning("Please upload data to view the dashboard.")
        return
    
    try:
        # Process data with error handling
        df = process_data(st.session_state.df)
        if df is None or df.empty:
            st.error("No valid data available for analysis.")
            return
            
        # Validate required columns
        required_columns = ['Amount', 'Sales Stage', 'Expected Close Date', 'Practice']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return
            
        st.title("Quarterly Summary")
        
        # Quarter selection with validation
        current_year = pd.Timestamp.now().year
        quarters = [f"Q{i} {current_year}" for i in range(1, 5)]
        quarter = st.selectbox("Select Quarter", quarters)
        
        # Filter data for selected quarter with error handling
        try:
            q = int(quarter.split()[0][1])
            start_date = pd.Timestamp(f"{current_year}-{3*q-2}-01")
            end_date = pd.Timestamp(f"{current_year}-{3*q}-30")
            
            df = df[(df["Expected Close Date"] >= start_date) & (df["Expected Close Date"] <= end_date)]
            
            if df.empty:
                st.warning(f"No data available for {quarter}")
                return
                
            # Calculate metrics with error handling
            total_pipeline = df["Amount"].sum() / 100000
            closed_won = df[df["Sales Stage"] == "Closed Won"]["Amount"].sum() / 100000
            total_deals = len(df)
            win_rate = (closed_won / total_pipeline * 100) if total_pipeline > 0 else 0
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Pipeline", f"₹{format_number(total_pipeline)}L")
            with col2:
                st.metric("Closed Won", f"₹{format_number(closed_won)}L")
            with col3:
                st.metric("Total Deals", format_number(total_deals))
            with col4:
                st.metric("Win Rate", format_percentage(win_rate))
            
            # Practice-wise summary with error handling
            st.subheader("Practice-wise Summary")
            try:
                practice_summary = df.groupby("Practice").agg({
                    "Amount": ["sum", "count"],
                    "Sales Stage": lambda x: (x == "Closed Won").sum()
                }).reset_index()
                
                practice_summary.columns = ["Practice", "Total Pipeline", "Pipeline Deals", "Closed Deals"]
                practice_summary["Win Rate"] = (practice_summary["Closed Deals"] / practice_summary["Pipeline Deals"] * 100).round(1)
                practice_summary["Closed Amount"] = practice_summary["Total Pipeline"] / 100000
                
                st.dataframe(practice_summary)
            except Exception as e:
                st.error(f"Error generating practice summary: {str(e)}")
            
            # Monthly trend with error handling
            st.subheader("Monthly Trend")
            try:
                monthly_trend = df.groupby(pd.Grouper(key="Expected Close Date", freq="M"))["Amount"].sum().reset_index()
                monthly_trend["Amount"] = monthly_trend["Amount"] / 100000
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=monthly_trend["Expected Close Date"],
                    y=monthly_trend["Amount"],
                    name="Amount"
                ))
                
                fig.update_layout(
                    title="Monthly Pipeline Trend",
                    xaxis_title="Month",
                    yaxis_title="Amount (in lakhs)",
                    showlegend=True
                )
                
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error generating monthly trend: {str(e)}")
                
        except Exception as e:
            st.error(f"Error processing quarter data: {str(e)}")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def show_previous_data_view():
    """Display the previous data view"""
    # Initialize session state variables if they don't exist
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    if st.session_state.df is None:
        st.warning("Please upload data to view the dashboard.")
        return
    
    try:
        # Process data with error handling
        df = process_data(st.session_state.df)
        if df is None or df.empty:
            st.error("No valid data available for analysis.")
            return
            
        # Validate required columns
        required_columns = ['Amount', 'Sales Stage', 'Expected Close Date', 'Practice']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return
            
        st.title("Previous Data View")
        
        # Year selection with validation
        current_year = pd.Timestamp.now().year
        years = [str(year) for year in range(current_year - 4, current_year + 1)]
        selected_year = st.selectbox("Select Year", years)
        
        # Filter data for selected year with error handling
        try:
            start_date = pd.Timestamp(f"{selected_year}-01-01")
            end_date = pd.Timestamp(f"{selected_year}-12-31")
            
            df = df[(df["Expected Close Date"] >= start_date) & (df["Expected Close Date"] <= end_date)]
            
            if df.empty:
                st.warning(f"No data available for {selected_year}")
                return
                
            # Calculate metrics with error handling
            total_pipeline = df["Amount"].sum() / 100000
            closed_won = df[df["Sales Stage"] == "Closed Won"]["Amount"].sum() / 100000
            total_deals = len(df)
            win_rate = (closed_won / total_pipeline * 100) if total_pipeline > 0 else 0
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Pipeline", f"₹{format_number(total_pipeline)}L")
            with col2:
                st.metric("Closed Won", f"₹{format_number(closed_won)}L")
            with col3:
                st.metric("Total Deals", format_number(total_deals))
            with col4:
                st.metric("Win Rate", format_percentage(win_rate))
            
            # Quarterly trend with error handling
            st.subheader("Quarterly Trend")
            try:
                df['Quarter'] = df['Expected Close Date'].dt.quarter
                quarterly_trend = df.groupby('Quarter').agg({
                    'Amount': 'sum',
                    'Sales Stage': lambda x: (x == 'Closed Won').sum()
                }).reset_index()
                
                quarterly_trend['Amount'] = quarterly_trend['Amount'] / 100000
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=quarterly_trend['Quarter'],
                    y=quarterly_trend['Amount'],
                    name='Amount'
                ))
                fig.add_trace(go.Scatter(
                    x=quarterly_trend['Quarter'],
                    y=quarterly_trend['Sales Stage'],
                    name='Closed Deals',
                    mode='lines+markers'
                ))
                
                fig.update_layout(
                    title=f"Quarterly Performance - {selected_year}",
                    xaxis_title="Quarter",
                    yaxis_title="Amount (in lakhs) / Number of Deals",
                    showlegend=True
                )
                
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error generating quarterly trend: {str(e)}")
            
            # Practice-wise summary with error handling
            st.subheader("Practice-wise Summary")
            try:
                practice_summary = df.groupby("Practice").agg({
                    "Amount": ["sum", "count"],
                    "Sales Stage": lambda x: (x == "Closed Won").sum()
                }).reset_index()
                
                practice_summary.columns = ["Practice", "Total Pipeline", "Pipeline Deals", "Closed Deals"]
                practice_summary["Win Rate"] = (practice_summary["Closed Deals"] / practice_summary["Pipeline Deals"] * 100).round(1)
                practice_summary["Closed Amount"] = practice_summary["Total Pipeline"] / 100000
                
                st.dataframe(practice_summary)
            except Exception as e:
                st.error(f"Error generating practice summary: {str(e)}")
                
        except Exception as e:
            st.error(f"Error processing year data: {str(e)}")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
