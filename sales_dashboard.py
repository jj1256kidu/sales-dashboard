import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io
from functools import lru_cache

# Format helper functions
def format_amount(x):
    try:
        if pd.isna(x) or x == 0:
            return "₹0L"
        # Convert to float first to handle string inputs, then to int
        value = float(str(x).replace('₹', '').replace('L', '').replace(',', ''))
        return f"₹{int(value)}L"
    except:
        return "₹0L"

def format_percentage(x):
    try:
        if pd.isna(x) or x == 0:
            return "0%"
        # Handle string percentage inputs
        if isinstance(x, str):
            value = float(x.rstrip('%'))
        else:
            value = float(x)
        return f"{int(value)}%"
    except:
        return "0%"

def format_number(x):
    try:
        if pd.isna(x) or x == 0:
            return "0"
        # Convert to float first to handle string inputs, then to int
        value = float(str(x).replace(',', ''))
        return f"{int(value):,}"
    except:
        return "0"

# Set page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'data_input'
if 'date_filter' not in st.session_state:
    st.session_state.date_filter = None
if 'selected_practice' not in st.session_state:
    st.session_state.selected_practice = 'All'
if 'selected_stage' not in st.session_state:
    st.session_state.selected_stage = 'All'
if 'reset_triggered' not in st.session_state:
    st.session_state.reset_triggered = False
if 'selected_team_member' not in st.session_state:
    st.session_state.selected_team_member = None

# Keep a single "sales_target" in session state
if 'sales_target' not in st.session_state:
    st.session_state.sales_target = 0.0  # Default target in Lakhs

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Modern theme colors */
    :root {
        --primary-color: #4A90E2;
        --background-color: #1E1E1E;
        --secondary-background-color: #252526;
        --text-color: #FFFFFF;
        --font-family: 'Segoe UI', sans-serif;
    }

    /* Main container styling */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: var(--font-family);
    }

    /* Card styling */
    .stCard {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 15px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Number formatting */
    .big-number {
        font-size: 2.8em;
        font-weight: 700;
        color: #2ecc71;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        letter-spacing: -1px;
    }

    .metric-value {
        font-size: 2em;
        font-weight: 600;
        color: #4A90E2;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    .metric-label {
        font-size: 1.2em;
        color: #333;
        margin-bottom: 5px;
        font-weight: 500;
    }

    /* Section headers */
    .section-header {
        font-size: 1.8em;
        font-weight: 700;
        color: #2c3e50;
        margin: 30px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Chart text styling */
    .js-plotly-plot .plotly .main-svg {
        font-size: 14px;
        font-weight: 500;
    }

    /* Table styling */
    .dataframe {
        font-size: 1.2em;
        background-color: white;
        border-radius: 8px;
        padding: 15px;
    }

    .dataframe th {
        background-color: #4A90E2;
        color: white;
        font-weight: 700;
        padding: 15px;
        font-size: 1.1em;
    }

    .dataframe td {
        padding: 12px;
        border-bottom: 1px solid #eee;
        font-weight: 500;
    }

    /* Upload container styling */
    .upload-container {
        background-color: rgba(74, 144, 226, 0.1);
        border-radius: 10px;
        padding: 30px;
        margin: 20px 0;
        border: 2px dashed rgba(74, 144, 226, 0.3);
        text-align: center;
    }

    /* Button styling */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #357ABD;
        transform: translateY(-2px);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom header */
    .custom-header {
        background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }

    /* Info box */
    .info-box {
        background-color: rgba(74, 144, 226, 0.1);
        border-left: 4px solid #4A90E2;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }

    /* Container styling */
    .container {
        margin: 30px 0;
        padding: 15px;
    }

    /* Graph container */
    .graph-container {
        margin: 30px 0;
        padding: 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Metric container */
    .metric-container {
        margin: 30px 0;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 10px;
    }

    /* Section divider */
    .section-divider {
        margin: 30px 0;
        border-top: 1px solid #eee;
    }

    /* Custom styling for number input */
    [data-testid="stNumberInput"] {
        position: relative;
        background: transparent !important;
    }
    [data-testid="stNumberInput"] > div > div > input {
        color: white !important;
        font-size: 1.8em !important;
        font-weight: 800 !important;
        text-align: center !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    /* Hide the increment/decrement buttons */
    [data-testid="stNumberInput"] > div > div > div {
        display: none !important;
    }
    /* Container styling */
    div[data-testid="column"] > div > div > div > div > div {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* Hide increment buttons */
    [data-testid="stNumberInput"] input[type="number"] {
        -moz-appearance: textfield;
    }
    [data-testid="stNumberInput"] input[type="number"]::-webkit-outer-spin-button,
    [data-testid="stNumberInput"] input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    /* Style the input field */
    [data-testid="stNumberInput"] {
        background: transparent;
    }
    
    /* Style the display value */
    .target-value {
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.5em;
        font-weight: 800;
        color: #FF6B6B;
        text-align: center;
        padding: 20px;
        margin: 10px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cache data processing functions
@st.cache_data
def process_data(df):
    """Process and prepare data for the dashboard"""
    df = df.copy()
    
    # Handle duplicate columns by keeping only the first occurrence
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Standardize column names
    column_mapping = {
        'Sales Team Member': 'Sales Owner',
        'Deal Value': 'Amount',
        'Status': 'Sales Stage',
        'Technical Lead': 'Pre-sales Technical Lead',
        'Expected Close Date': 'Expected Close Date',
        'Hunting/Farming': 'Type',
        'Hunting /farming': 'Type',
        'Sales_Stage': 'Sales Stage',
        'Month_1': 'Month',
        'Short Month': 'Month',
        'Short Year(25)': 'Year',
        'Year in FY': 'Year',
        'FY': 'Year',
        'Merge COlumn': 'Practice',
        'P & L Centre': 'Practice'
    }
    
    # Rename columns if they exist
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Convert dates and calculate time-based columns at once with explicit dayfirst parameter
    df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], format='%d-%m-%Y', dayfirst=True, errors='coerce')
    df['Month'] = df['Expected Close Date'].dt.strftime('%B')
    df['Year'] = df['Expected Close Date'].dt.year
    df['Quarter'] = df['Expected Close Date'].dt.quarter.map({1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
    
    # Convert probability and calculate numeric values at once with safe null handling
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
    
    # Pre-calculate common flags and metrics with safe null handling
    df['Is_Won'] = df['Sales Stage'].apply(lambda x: 'Won' in str(x) if pd.notna(x) else False)
    df['Amount_Lacs'] = df['Amount'].fillna(0).div(100000).round(0).astype(int)
    df['Weighted_Amount'] = (df['Amount_Lacs'] * df['Probability_Num'] / 100).round(0).astype(int)
    
    return df

@st.cache_data
def calculate_team_metrics(df):
    """Calculate all team-related metrics at once"""
    team_metrics = df.groupby('Sales Owner').agg({
        'Amount': lambda x: int(x[df['Is_Won'] & x.notna()].sum() / 100000) if len(x[df['Is_Won'] & x.notna()]) > 0 else 0,
        'Is_Won': 'sum',
        'Amount_Lacs': lambda x: int(x[~df['Is_Won'] & x.notna()].sum()) if len(x[~df['Is_Won'] & x.notna()]) > 0 else 0,
        'Weighted_Amount': lambda x: int(x[~df['Is_Won'] & x.notna()].sum()) if len(x[~df['Is_Won'] & x.notna()]) > 0 else 0
    }).reset_index()
    
    team_metrics.columns = ['Sales Owner', 'Closed Won', 'Closed Deals', 'Current Pipeline', 'Weighted Projections']
    
    team_metrics = team_metrics.fillna(0)
    
    # Calculate Pipeline Deals
    pipeline_deals = df[~df['Is_Won']].groupby('Sales Owner').size()
    team_metrics['Pipeline Deals'] = team_metrics['Sales Owner'].map(pipeline_deals).fillna(0).astype(int)
    
    # Win Rate
    total_deals = team_metrics['Closed Deals'] + team_metrics['Pipeline Deals']
    team_metrics['Win Rate'] = np.where(
        total_deals > 0,
        (team_metrics['Closed Deals'] / total_deals * 100).round(0),
        0
    ).astype(int)
    
    return team_metrics

@st.cache_data
def filter_dataframe(df, filters):
    """Apply filters to dataframe efficiently"""
    mask = pd.Series(True, index=df.index)
    
    if filters.get('selected_member') != "All Team Members":
        mask &= df['Sales Owner'] == filters['selected_member']
    
    if filters.get('search'):
        search_mask = pd.Series(False, index=df.index)
        search = filters['search'].lower()
        for col in ['Organization Name', 'Opportunity Name', 'Sales Owner', 'Sales Stage']:
            search_mask |= df[col].astype(str).str.lower().str.contains(search, na=False)
        mask &= search_mask
    
    # Practice filter
    if filters.get('practices'):
        mask &= df['Practice'].isin(filters['practices'])
            
    if filters.get('month_filter') != "All Months":
        mask &= df['Month'] == filters['month_filter']
    
    if filters.get('quarter_filter') != "All Quarters":
        mask &= df['Quarter'] == filters['quarter_filter']
    
    if filters.get('year_filter') != "All Years":
        mask &= df['Year'] == filters['year_filter']
    
    if filters.get('probability_filter') != "All Probability":
        if filters['probability_filter'] == "Custom Range":
            prob_range = filters['custom_prob_range'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
        else:
            prob_range = filters['probability_filter'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
        mask &= (df['Probability_Num'] >= min_prob) & (df['Probability_Num'] <= max_prob)
    
    if filters.get('status_filter') != "All Status":
        if filters['status_filter'] == "Committed for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask &= (df['Month'] == current_month) & (df['Probability_Num'] > 75)
        elif filters['status_filter'] == "Upsides for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask &= (df['Month'] == current_month) & (df['Probability_Num'].between(25, 75))
        else:
            mask &= df['Sales Stage'] == filters['status_filter']
    
    if filters.get('focus_filter') != "All Focus":
        mask &= df['KritiKal Focus Areas'] == filters['focus_filter']
    
    return df[mask]

def show_data_input():
    # Custom header
    st.markdown("""
        <div class="custom-header">
            <h1>Sales Performance Dashboard</h1>
            <p style="font-size: 1.2em; margin: 0;">Upload your sales data to begin analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # Main upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Sales Data",
            type=['xlsx'],
            help="Upload your sales data file in Excel format (.xlsx)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            try:
                # Read Excel file and get sheet names
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                # Display sheet selection with better UI
                st.markdown("""
                    <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
                        <h3 style='color: #2a5298; margin: 0 0 15px 0;'>Sheet Selection</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("""
                        <div style='padding: 10px; background: #e8f0fe; border-radius: 5px;'>
                            <p style='color: #2a5298; margin: 0;'>📅 Current Week Data</p>
                        </div>
                    """, unsafe_allow_html=True)
                    selected_current_sheet = st.selectbox(
                        "Select sheet containing current week's data",
                        sheet_names,
                        key="current_week",
                        help="Choose the sheet with your most recent data"
                    )
                
                with col_b:
                    st.markdown("""
                        <div style='padding: 10px; background: #e8f0fe; border-radius: 5px;'>
                            <p style='color: #2a5298; margin: 0;'>📅 Previous Week Data</p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Filter out the current sheet from previous week options
                    prev_sheet_options = [sheet for sheet in sheet_names if sheet != selected_current_sheet]
                    selected_previous_sheet = st.selectbox(
                        "Select sheet containing previous week's data",
                        prev_sheet_options,
                        key="previous_week",
                        help="Choose the sheet with your previous week's data"
                    )
                
                # Read the data with better error handling
                try:
                    df_current = pd.read_excel(uploaded_file, sheet_name=selected_current_sheet)
                    df_previous = pd.read_excel(uploaded_file, sheet_name=selected_previous_sheet)
                    
                    # Function to clean and standardize column names
                    def clean_column_names(df):
                        # Strip whitespace and convert to lowercase for comparison
                        df.columns = df.columns.str.strip()
                        
                        # Find duplicate columns
                        duplicates = df.columns[df.columns.duplicated()].tolist()
                        if duplicates:
                            st.warning(f"Found duplicate columns: {', '.join(duplicates)}")
                            
                            # Create a mapping of duplicate columns with suffixes
                            col_mapping = {}
                            seen_cols = set()
                            for col in df.columns:
                                if col in seen_cols:
                                    count = sum(1 for c in col_mapping if c.startswith(col))
                                    new_col = f"{col}_{count + 1}"
                                    col_mapping[col] = new_col
                                else:
                                    seen_cols.add(col)
                                    col_mapping[col] = col
                            
                            # Rename columns using the mapping
                            df.columns = [col_mapping[col] for col in df.columns]
                        
                        return df
                    
                    # Clean and standardize column names
                    df_current = clean_column_names(df_current)
                    df_previous = clean_column_names(df_previous)
                    
                    # Display data preview with error handling
                    st.markdown("### Data Preview")
                    
                    # Current week preview
                    st.markdown(f"""
                        <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                            <h4 style='color: #2a5298; margin: 0;'>Current Week Data ({selected_current_sheet})</h4>
                            <p style='color: #666; margin: 5px 0 0 0;'>{len(df_current)} rows × {len(df_current.columns)} columns</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        st.dataframe(
                            df_current.head(),
                            use_container_width=True
                        )
                        
                        # Show column names and types
                        with st.expander("Show Current Week Column Details"):
                            col_info = pd.DataFrame({
                                'Column Name': df_current.columns,
                                'Data Type': df_current.dtypes.astype(str),
                                'Non-Null Count': df_current.count(),
                                'Null Count': df_current.isna().sum()
                            })
                            st.dataframe(col_info, use_container_width=True)
                    
                    except Exception as e:
                        st.error(f"Error displaying current week data: {str(e)}")
                    
                    # Previous week preview
                    st.markdown(f"""
                        <div style='background: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                            <h4 style='color: #2a5298; margin: 0;'>Previous Week Data ({selected_previous_sheet})</h4>
                            <p style='color: #666; margin: 5px 0 0 0;'>{len(df_previous)} rows × {len(df_previous.columns)} columns</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        st.dataframe(
                            df_previous.head(),
                            use_container_width=True
                        )
                        
                        # Show column names and types
                        with st.expander("Show Previous Week Column Details"):
                            col_info = pd.DataFrame({
                                'Column Name': df_previous.columns,
                                'Data Type': df_previous.dtypes.astype(str),
                                'Non-Null Count': df_previous.count(),
                                'Null Count': df_previous.isna().sum()
                            })
                            st.dataframe(col_info, use_container_width=True)
                    
                    except Exception as e:
                        st.error(f"Error displaying previous week data: {str(e)}")
                    
                    # Store processed data in session state
                    st.session_state.df_current = df_current
                    st.session_state.df_previous = df_previous
                    st.session_state.df = df_current  # Keep main df as current week for compatibility
                    
                    # Success message
                    st.success(f"""
                        Successfully loaded:
                        - Current week ({selected_current_sheet}): {len(df_current):,} records
                        - Previous week ({selected_previous_sheet}): {len(df_previous):,} records
                    """)
                
                except Exception as e:
                    st.error(f"Error reading Excel sheets: {str(e)}")
                    st.error("Please make sure the selected sheets contain valid data.")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.error("Please make sure your Excel file is properly formatted and not corrupted.")
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Required Data Fields</h4>
            <ul>
                <li>Amount (or Deal Value)</li>
                <li>Sales Stage (or Status)</li>
                <li>Expected Close Date</li>
                <li>Sales Owner (or Sales Team Member)</li>
                <li>Practice/Region</li>
            </ul>
            <h4>File Format</h4>
            <ul>
                <li>Excel (.xlsx) with two sheets:</li>
                <ul>
                    <li>Current week's data</li>
                    <li>Previous week's data</li>
                </ul>
            </ul>
            <h4>Tips</h4>
            <ul>
                <li>Ensure column names are consistent across sheets</li>
                <li>Remove any empty columns</li>
                <li>Check for duplicate column names</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_overview():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Sales Performance Overview")
    df = st.session_state.df.copy()

    # Sales Target Section
    st.markdown("### Enter Your Sales Target (Optional)")
    default_target = str(int(st.session_state.get("sales_target", 0)))
    user_target_input = st.text_input("Sales Target (in Lakhs)", value=default_target)

    try:
        user_target = int(user_target_input)
    except ValueError:
        user_target = 0

    st.session_state.sales_target = float(user_target)

    # Safely handle the Sales Stage column for won deals
    def is_won_deal(stage):
        if pd.isna(stage):
            return False
        return 'won' in str(stage).lower()

    # Calculate total "Closed Won" with safe handling
    won_deals = df[df['Sales Stage'].apply(is_won_deal)]
    won_amount_lacs = won_deals['Amount'].fillna(0).sum() / 100000  # convert to Lakhs

    # Show "Target vs Closed Won" progress
    if st.session_state.sales_target > 0:
        achievement_pct = (won_amount_lacs / st.session_state.sales_target) * 100
    else:
        achievement_pct = 0

    st.markdown(
        f"""
        <div style='margin-top: 30px; padding: 20px; background: #f0f2f6; border-radius: 12px;'>
            <h3 style='margin: 0; color: #2ecc71; font-size: 1.2em; font-weight: 500;'>Closed Won</h3>
            <h2 style='margin: 5px 0; color: #2ecc71; font-size: 2.8em; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                ₹{won_amount_lacs:,.2f}L
            </h2>
            <div style='text-align: right; margin-bottom: 10px;'>
                <span style='color: #e74c3c; font-size: 1em; font-weight: 500;'>Target: ₹{st.session_state.sales_target:,.0f}L</span>
            </div>
            <div style='background: #e74c3c; height: 40px; border-radius: 20px; overflow: hidden; position: relative; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);'>
                <div style='background: #2ecc71; height: 100%; width: {min(achievement_pct, 100)}%; transition: width 0.5s ease-in-out;'></div>
                <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: 600; font-size: 1.2em; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
                    {int(achievement_pct)}% Complete
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # II. Practice
    st.markdown("""
        <div style='background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Practice</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'Practice' in df.columns:
        # Add practice filter
        practices = ['All'] + sorted(df['Practice'].dropna().unique().tolist())
        selected_practice = st.selectbox(
            "Select Practice",
            options=practices,
            key="practice_filter"
        )
        
        # Filter data based on selected practice
        df_practice = df.copy()
        if selected_practice != 'All':
            df_practice = df_practice[df_practice['Practice'] == selected_practice]
        
        # Calculate practice metrics
        practice_metrics = df_practice.groupby('Practice').agg({
            'Amount': lambda x: x[df_practice['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
            'Sales Stage': lambda x: x[df_practice['Sales Stage'].str.contains('Won', case=False, na=False)].count()
        }).reset_index()
        
        practice_metrics.columns = ['Practice', 'Closed Amount', 'Closed Deals']
        
        # Pipeline by practice
        pipeline_df = df_practice[~df_practice['Sales Stage'].str.contains('Won', case=False, na=False)]
        total_pipeline = pipeline_df.groupby('Practice')['Amount'].sum() / 100000
        practice_metrics['Total Pipeline'] = practice_metrics['Practice'].map(total_pipeline)
        
        # Pipeline deal counts
        total_deals = pipeline_df.groupby('Practice').size()
        practice_metrics['Pipeline Deals'] = practice_metrics['Practice'].map(total_deals)
        
        # Sort by pipeline
        practice_metrics = practice_metrics.sort_values('Total Pipeline', ascending=False)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pipeline = go.Figure()
            fig_pipeline.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Total Pipeline'],
                name='Pipeline',
                text=practice_metrics['Total Pipeline'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
                marker_color='#4A90E2',
                marker_line=dict(color='#357ABD', width=2),
                opacity=0.9
            ))
            fig_pipeline.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Closed Amount'],
                name='Closed Won',
                text=practice_metrics['Closed Amount'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_pipeline.update_layout(
                title=dict(
                    text="Practice-wise Pipeline vs Closed Won",
                    font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top'
                ),
                height=500,
                barmode='group',
                bargap=0.15,
                bargroupgap=0.1,
                xaxis_title=dict(
                    text="Practice",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                yaxis_title=dict(
                    text="Amount (Lakhs)",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                showlegend=True,
                legend=dict(
                    font=dict(size=14, family='Segoe UI', color='#2c3e50'),
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0.2)',
                    borderwidth=1
                ),
                font=dict(size=14, family='Segoe UI'),
                xaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                yaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=80, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_pipeline, use_container_width=True)
        
        with col2:
            fig_deals = go.Figure()
            fig_deals.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Pipeline Deals'],
                name='Pipeline Deals',
                text=practice_metrics['Pipeline Deals'],
                textposition='outside',
                textfont=dict(size=16, color='#4A90E2', family='Segoe UI', weight='bold'),
                marker_color='#4A90E2',
                marker_line=dict(color='#357ABD', width=2),
                opacity=0.9
            ))
            fig_deals.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Closed Deals'],
                name='Closed Deals',
                text=practice_metrics['Closed Deals'],
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_deals.update_layout(
                title=dict(
                    text="Practice-wise Pipeline vs Closed Deals",
                    font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                    x=0.5,
                    y=0.95,
                    xanchor='center',
                    yanchor='top'
                ),
                height=500,
                barmode='group',
                bargap=0.15,
                bargroupgap=0.1,
                xaxis_title=dict(
                    text="Practice",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                yaxis_title=dict(
                    text="Number of Deals",
                    font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                    standoff=15
                ),
                showlegend=True,
                legend=dict(
                    font=dict(size=14, family='Segoe UI', color='#2c3e50'),
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0.2)',
                    borderwidth=1
                ),
                font=dict(size=14, family='Segoe UI'),
                xaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                yaxis=dict(
                    tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                    gridcolor='rgba(0, 0, 0, 0.1)'
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=80, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_deals, use_container_width=True)
        
        # Practice summary
        st.markdown("### Practice Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pipeline_val = practice_metrics['Total Pipeline'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Pipeline</div>
                    <div class='metric-value'>₹{int(total_pipeline_val)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_deals_count = practice_metrics['Pipeline Deals'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Pipeline Deals</div>
                    <div class='metric-value'>{int(total_deals_count)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Active opportunities</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_won = practice_metrics['Closed Deals'].sum()
            win_rate = (total_won / (total_won + total_deals_count) * 100) if (total_won + total_deals_count) > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Win Rate</div>
                    <div class='metric-value'>{int(win_rate)}%</div>
                    <div style='color: #666; font-size: 0.9em;'>{int(total_won)} won</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_deal_size = practice_metrics['Closed Amount'].sum() / total_won if total_won > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Avg Deal Size</div>
                    <div class='metric-value'>₹{int(avg_deal_size)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per won deal</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Practice-wise table
        st.markdown("### Practice-wise Details")
        summary_data = practice_metrics.copy()
        summary_data['Win Rate'] = (summary_data['Closed Deals'] / (summary_data['Closed Deals'] + summary_data['Pipeline Deals']) * 100).round(1)
        summary_data['Closed Amount'] = summary_data['Closed Amount'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Total Pipeline'] = summary_data['Total Pipeline'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Win Rate'] = summary_data['Win Rate'].apply(lambda x: f"{int(x)}%")
        
        st.dataframe(
            summary_data[['Practice', 'Closed Amount', 'Total Pipeline', 'Closed Deals', 'Pipeline Deals', 'Win Rate']],
            use_container_width=True
        )
    else:
        st.error("Practice column not found in the dataset")

    # KritiKal Focus Areas
    st.markdown("""
        <div style='background: linear-gradient(90deg, #9b59b6 0%, #8e44ad 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>KritiKal Focus Areas</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'KritiKal Focus Areas' in df.columns:
        focus_metrics = df.groupby('KritiKal Focus Areas').agg({
            'Amount': 'sum',
            'Sales Stage': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].count()
        }).reset_index()
        
        focus_metrics['KritiKal Focus Areas'] = focus_metrics['KritiKal Focus Areas'].fillna('Uncategorized')
        
        focus_metrics.columns = ['Focus Area', 'Total Amount', 'Closed Deals']
        focus_metrics['Total Amount'] = focus_metrics['Total Amount'] / 100000
        
        total_deals_focus = df.groupby('KritiKal Focus Areas').size().reset_index()
        total_deals_focus.columns = ['Focus Area', 'Total Deals']
        focus_metrics = focus_metrics.merge(total_deals_focus, on='Focus Area', how='left')
        
        total_amount_focus = focus_metrics['Total Amount'].sum()
        focus_metrics['Share %'] = (focus_metrics['Total Amount'] / total_amount_focus * 100).round(1)
        
        focus_metrics = focus_metrics.sort_values('Total Amount', ascending=False)
        
        st.markdown("### Focus Areas Summary")
        summary_data = focus_metrics.copy()
        summary_data['Total Amount'] = summary_data['Total Amount'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Share %'] = summary_data['Share %'].apply(lambda x: f"{int(x)}%")
        
        summary_data = summary_data.reset_index(drop=True)
        summary_data.index = summary_data.index + 1
        
        st.dataframe(
            summary_data[['Focus Area', 'Total Amount', 'Share %', 'Total Deals', 'Closed Deals']],
            use_container_width=True
        )
        
        st.markdown("### Focus Areas Distribution")
        fig_focus = go.Figure(data=[go.Pie(
            labels=focus_metrics['Focus Area'],
            values=focus_metrics['Total Amount'],
            hole=.4,
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>' + format_amount('%{value}'),
            textfont=dict(size=14, family='Segoe UI', weight='bold')
        )])
        
        fig_focus.update_layout(
            title=dict(
                text="Focus Areas Distribution",
                font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top'
            ),
            height=500,
            showlegend=True,
            legend=dict(
                font=dict(size=14, family='Segoe UI', color='#2c3e50'),
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            ),
            annotations=[dict(
                text=f"Total: ₹{int(total_amount_focus)}L",
                font=dict(size=16, family='Segoe UI', weight='bold'),
                showarrow=False,
                x=0.5,
                y=0.5
            )]
        )
        
        st.plotly_chart(fig_focus, use_container_width=True)
    else:
        st.info("KritiKal Focus Areas column not found in the dataset")

    # Monthly Pipeline Trend
    st.markdown("""
        <div style='background: linear-gradient(90deg, #00b4db 0%, #0083b0 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Monthly Pipeline Trend</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'Expected Close Date' in df.columns and 'Amount' in df.columns and 'Sales Stage' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
        
        deal_type = st.selectbox(
            "Select Deal Type",
            ["🌊 Pipeline", "🟢 Closed Won", "📦 All Deals"],
            index=0
        )
        
        if deal_type == "🌊 Pipeline":
            filtered_df = df[~df['Sales Stage'].str.contains('Won', case=False, na=False)]
            color = '#00b4db'
        elif deal_type == "🟢 Closed Won":
            filtered_df = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
            color = '#2ecc71'
        else:
            filtered_df = df
            color = '#9b59b6'
        
        monthly_data = filtered_df.groupby(filtered_df['Expected Close Date'].dt.to_period('M')).agg({
            'Amount': 'sum',
            'Sales Stage': 'count'
        }).reset_index()
        
        monthly_data['Expected Close Date'] = monthly_data['Expected Close Date'].astype(str)
        monthly_data['Amount'] = monthly_data['Amount'] / 100000
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_data['Expected Close Date'],
            y=monthly_data['Amount'],
            mode='lines+markers',
            name=deal_type,
            line=dict(width=3, color=color),
            marker=dict(size=8, color=color),
            text=monthly_data['Amount'].apply(lambda x: f"₹{int(x)}L"),
            textposition='top center',
            textfont=dict(size=12, family='Segoe UI', weight='bold')
        ))
        
        fig_trend.update_layout(
            title=dict(
                text=f"{deal_type} Trend",
                font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top'
            ),
            height=500,
            showlegend=False,
            xaxis_title=dict(
                text="Month",
                font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                standoff=15
            ),
            yaxis_title=dict(
                text="Amount (Lakhs)",
                font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                standoff=15
            ),
            font=dict(size=14, family='Segoe UI'),
            xaxis=dict(
                tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            yaxis=dict(
                tickfont=dict(size=12, family='Segoe UI', color='#2c3e50'),
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=80, b=40, l=40, r=40)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_value = monthly_data['Amount'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Value</div>
                    <div class='metric-value'>₹{int(total_value)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Overall</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            avg_monthly = monthly_data['Amount'].mean()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Monthly Average</div>
                    <div class='metric-value'>₹{int(avg_monthly)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per month</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            total_deals = monthly_data['Sales Stage'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Deals</div>
                    <div class='metric-value'>{int(total_deals)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Number of deals</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Required columns (Expected Close Date, Amount, Sales Stage) not found in the dataset")

def show_sales_team():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Sales Team Performance")
    df = st.session_state.df.copy()  # Use only current week data
    
    # Calculate team metrics
    team_metrics = df.groupby('Sales Owner').agg({
        'Amount': 'sum',
        'Sales Stage': 'count'
    }).reset_index()
    
    # Calculate won deals based on Sales Stage
    won_deals = df[df['Sales Stage'].apply(lambda x: 'Won' in str(x) if pd.notna(x) else False)]
    won_metrics = won_deals.groupby('Sales Owner').agg({
        'Amount': 'sum',
        'Sales Stage': 'count'
    }).reset_index()
    
    # Merge won metrics with team metrics
    team_metrics = team_metrics.merge(
        won_metrics[['Sales Owner', 'Amount', 'Sales Stage']],
        on='Sales Owner',
        how='left',
        suffixes=('_total', '_won')
    ).fillna(0)
    
    team_metrics['Win Rate'] = (team_metrics['Sales Stage_won'] / team_metrics['Sales Stage_total'] * 100).round(1)
    team_metrics['Amount_total'] = team_metrics['Amount_total'].div(100000).round(0).astype(int)
    
    # Display team metrics in a table
    st.subheader("Team Performance Metrics")
    st.dataframe(
        team_metrics.rename(columns={
            'Sales Owner': 'Sales Owner',
            'Amount_total': 'Total Amount (Lakhs)',
            'Sales Stage_total': 'Total Deals',
            'Sales Stage_won': 'Won Deals',
            'Win Rate': 'Win Rate (%)'
        }),
        use_container_width=True
    )
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Team Performance")
        fig = px.bar(
            team_metrics,
            x='Sales Owner',
            y='Amount_total',
            title='Total Amount by Sales Owner',
            labels={'Amount_total': 'Amount (Lakhs)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Practice Distribution")
        practice_dist = df.groupby('Practice')['Amount'].sum().reset_index()
        practice_dist['Amount'] = practice_dist['Amount'].div(100000).round(0).astype(int)
        
        fig = px.pie(
            practice_dist,
            values='Amount',
            names='Practice',
            title='Amount Distribution by Practice'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Practice-wise performance
    st.subheader("Practice Performance")
    practice_metrics = df.groupby('Practice').agg({
        'Amount': 'sum',
        'Sales Stage': 'count'
    }).reset_index()
    
    # Calculate won deals for practices
    won_practice = won_deals.groupby('Practice').agg({
        'Amount': 'sum',
        'Sales Stage': 'count'
    }).reset_index()
    
    # Merge won metrics with practice metrics
    practice_metrics = practice_metrics.merge(
        won_practice[['Practice', 'Amount', 'Sales Stage']],
        on='Practice',
        how='left',
        suffixes=('_total', '_won')
    ).fillna(0)
    
    practice_metrics['Win Rate'] = (practice_metrics['Sales Stage_won'] / practice_metrics['Sales Stage_total'] * 100).round(1)
    practice_metrics['Amount_total'] = practice_metrics['Amount_total'].div(100000).round(0).astype(int)
    
    st.dataframe(
        practice_metrics.rename(columns={
            'Practice': 'Practice',
            'Amount_total': 'Total Amount (Lakhs)',
            'Sales Stage_total': 'Total Deals',
            'Sales Stage_won': 'Won Deals',
            'Win Rate': 'Win Rate (%)'
        }),
        use_container_width=True
    )
    
    # Practice pipeline trend
    st.subheader("Practice Pipeline Trend")
    practice_trend = df.groupby(['Practice', 'Sales Stage'])['Amount'].sum().reset_index()
    practice_trend['Amount'] = practice_trend['Amount'].div(100000).round(0).astype(int)
    
    fig = px.line(
        practice_trend,
        x='Practice',
        y='Amount',
        color='Sales Stage',
        title='Pipeline Trend by Practice',
        labels={'Amount': 'Amount (Lakhs)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed opportunities
    st.subheader("Detailed Opportunities")
    detailed_opps = df[[
        'Sales Owner',
        'Practice',
        'Sales Stage',
        'Amount',
        'Expected Close Date'
    ]].copy()
    
    detailed_opps['Amount'] = detailed_opps['Amount'].div(100000).round(0).astype(int)
    detailed_opps['Expected Close Date'] = pd.to_datetime(detailed_opps['Expected Close Date']).dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        detailed_opps.rename(columns={
            'Sales Owner': 'Sales Owner',
            'Practice': 'Practice',
            'Sales Stage': 'Sales Stage',
            'Amount': 'Amount (Lakhs)',
            'Expected Close Date': 'Expected Close Date'
        }),
        use_container_width=True
    )
    
    # Add back the original views
    st.subheader("Sales Stage Distribution")
    stage_dist = df.groupby('Sales Stage')['Amount'].sum().reset_index()
    stage_dist['Amount'] = stage_dist['Amount'].div(100000).round(0).astype(int)
    
    fig = px.pie(
        stage_dist,
        values='Amount',
        names='Sales Stage',
        title='Amount Distribution by Sales Stage'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly trend
    st.subheader("Monthly Trend")
    df['Month'] = pd.to_datetime(df['Expected Close Date']).dt.strftime('%Y-%m')
    monthly_trend = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_trend['Amount'] = monthly_trend['Amount'].div(100000).round(0).astype(int)
    
    fig = px.line(
        monthly_trend,
        x='Month',
        y='Amount',
        title='Monthly Sales Trend',
        labels={'Amount': 'Amount (Lakhs)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Win rate by practice
    st.subheader("Win Rate by Practice")
    win_rate_by_practice = practice_metrics[['Practice', 'Win Rate']].sort_values('Win Rate', ascending=False)
    
    fig = px.bar(
        win_rate_by_practice,
        x='Practice',
        y='Win Rate',
        title='Win Rate by Practice',
        labels={'Win Rate': 'Win Rate (%)'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_detailed():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view detailed information")
        return
    
    st.title("Detailed Sales Data")
    df = st.session_state.df
    search = st.text_input("Search", placeholder="Search in any field...")
    
    if search:
        mask = np.column_stack([df[col].astype(str).str.contains(search, case=False, na=False) 
                                for col in df.columns])
        df = df[mask.any(axis=1)]
    
    st.dataframe(df, use_container_width=True)

def show_quarter_summary():
    st.title("Quarter Summary Dashboard")
    
    # Check if both current and previous week data are loaded
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload both current and previous week data first!")
        return
    
    # Get current and previous week data
    df_current = st.session_state.df_current.copy()
    df_previous = st.session_state.df_previous.copy()
    
    # Filters
    col1, col2, col3 = st.columns([1.2, 1.2, 1.2])
    
    with col1:
        sales_owners = sorted(df_current['Sales Owner'].dropna().unique().tolist())
        selected_sales_owner = st.selectbox("👤 Sales Owner", ["All Sales Owners"] + sales_owners)
    
    with col2:
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        selected_quarter = st.selectbox("📊 Quarter", ["All Quarters"] + quarters)
    
    with col3:
        practices = sorted(df_current['Practice'].dropna().unique().tolist())
        selected_practice = st.selectbox("🏢 Practice", ["All Practices"] + practices)
    
    # Apply filters to both current and previous week data
    if selected_sales_owner != "All Sales Owners":
        df_current = df_current[df_current['Sales Owner'] == selected_sales_owner]
        df_previous = df_previous[df_previous['Sales Owner'] == selected_sales_owner]
    
    if selected_quarter != "All Quarters":
        df_current = df_current[df_current['Quarter'] == selected_quarter]
        df_previous = df_previous[df_previous['Quarter'] == selected_quarter]
    
    if selected_practice != "All Practices":
        df_current = df_current[df_current['Practice'] == selected_practice]
        df_previous = df_previous[df_previous['Practice'] == selected_practice]
    
    # Calculate metrics for current week
    committed_current = df_current[df_current['Sales Stage'] == "Committed for the Month"]['Amount'].sum()
    upside_current = df_current[df_current['Sales Stage'] == "Upsides for the Month"]['Amount'].sum()
    closed_won_current = df_current[df_current['Sales Stage'].apply(lambda x: 'Won' in str(x) if pd.notna(x) else False)]['Amount'].sum()
    
    # Calculate metrics for previous week
    committed_previous = df_previous[df_previous['Sales Stage'] == "Committed for the Month"]['Amount'].sum()
    upside_previous = df_previous[df_previous['Sales Stage'] == "Upsides for the Month"]['Amount'].sum()
    closed_won_previous = df_previous[df_previous['Sales Stage'].apply(lambda x: 'Won' in str(x) if pd.notna(x) else False)]['Amount'].sum()
    
    # Calculate deltas and percentages
    def calculate_delta_percentage(current, previous):
        delta = current - previous
        percentage = (delta / previous * 100) if previous != 0 else 0
        return delta, percentage
    
    committed_delta, committed_pct = calculate_delta_percentage(committed_current, committed_previous)
    upside_delta, upside_pct = calculate_delta_percentage(upside_current, upside_previous)
    closed_won_delta, closed_won_pct = calculate_delta_percentage(closed_won_current, closed_won_previous)
    
    # Calculate overall committed
    overall_committed_current = committed_current + closed_won_current
    overall_committed_previous = committed_previous + closed_won_previous
    overall_committed_delta, overall_committed_pct = calculate_delta_percentage(overall_committed_current, overall_committed_previous)
    
    # Helper function for trend indicator
    def get_trend_indicator(value):
        if value > 0:
            return "↗️"
        elif value < 0:
            return "↘️"
        return "➡️"
    
    # Display metrics using enhanced card-based layout
    def create_metric_card(title, current, previous, delta, percentage):
        trend = get_trend_indicator(delta)
        return f"""
            <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 10px 0;'>
                <h3 style='color: #2a5298; margin: 0 0 15px 0; font-size: 1.2em;'>{title}</h3>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;'>
                    <div>
                        <div style='color: #666; font-size: 0.9em;'>Current Week</div>
                        <div style='color: #2ecc71; font-size: 1.4em; font-weight: 600;'>₹{current / 100000:.0f}L</div>
                    </div>
                    <div>
                        <div style='color: #666; font-size: 0.9em;'>Previous Week</div>
                        <div style='color: #3498db; font-size: 1.4em; font-weight: 600;'>₹{previous / 100000:.0f}L</div>
                    </div>
                    <div>
                        <div style='color: #666; font-size: 0.9em;'>Change</div>
                        <div style='color: {"#2ecc71" if delta >= 0 else "#e74c3c"}; font-size: 1.4em; font-weight: 600;'>
                            {trend} ₹{abs(delta) / 100000:.0f}L
                            <div style='font-size: 0.7em;'>({percentage:.1f}%)</div>
                        </div>
                    </div>
                </div>
            </div>
        """
    
    # Create all metric cards
    metrics_html = f"""
        {create_metric_card("Committed Data", committed_current, committed_previous, committed_delta, committed_pct)}
        {create_metric_card("Upside Data", upside_current, upside_previous, upside_delta, upside_pct)}
        {create_metric_card("Closed Won", closed_won_current, closed_won_previous, closed_won_delta, closed_won_pct)}
        {create_metric_card("Overall Committed", overall_committed_current, overall_committed_previous, overall_committed_delta, overall_committed_pct)}
    """
    
    st.markdown(metrics_html, unsafe_allow_html=True)
    
    # Add summary statistics
    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
            <h4 style='color: #2a5298; margin: 0; font-size: 1.1em; font-weight: 600;'>📊 Summary Statistics</h4>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_deals_current = len(df_current)
        total_deals_previous = len(df_previous)
        deals_delta = total_deals_current - total_deals_previous
        st.metric("Total Deals", total_deals_current, deals_delta)
    
    with col2:
        avg_deal_size_current = committed_current / total_deals_current if total_deals_current > 0 else 0
        avg_deal_size_previous = committed_previous / total_deals_previous if total_deals_previous > 0 else 0
        avg_deal_delta = avg_deal_size_current - avg_deal_size_previous
        st.metric("Avg Deal Size (Lakhs)", f"₹{avg_deal_size_current/100000:.1f}L", f"₹{avg_deal_delta/100000:.1f}L")
    
    with col3:
        win_rate_current = (closed_won_current / committed_current * 100) if committed_current > 0 else 0
        win_rate_previous = (closed_won_previous / committed_previous * 100) if committed_previous > 0 else 0
        win_rate_delta = win_rate_current - win_rate_previous
        st.metric("Win Rate", f"{win_rate_current:.1f}%", f"{win_rate_delta:.1f}%")
    
    with col4:
        conversion_rate_current = (closed_won_current / upside_current * 100) if upside_current > 0 else 0
        conversion_rate_previous = (closed_won_previous / upside_previous * 100) if upside_previous > 0 else 0
        conversion_rate_delta = conversion_rate_current - conversion_rate_previous
        st.metric("Conversion Rate", f"{conversion_rate_current:.1f}%", f"{conversion_rate_delta:.1f}%")

def main():
    with st.sidebar:
        st.title("Navigation")
        selected = st.radio(
            "Select View",
            options=["Data Input", "Overview", "Sales Team", "Detailed Data", "Quarter Summary"],
            key="navigation"
        )
        st.session_state.current_view = selected.lower().replace(" ", "_")
    
    if st.session_state.current_view == "data_input":
        show_data_input()
    elif st.session_state.current_view == "overview":
        show_overview()
    elif st.session_state.current_view == "sales_team":
        show_sales_team()
    elif st.session_state.current_view == "detailed_data":
        show_detailed()
    elif st.session_state.current_view == "quarter_summary":
        show_quarter_summary()

if __name__ == "__main__":
    main()
