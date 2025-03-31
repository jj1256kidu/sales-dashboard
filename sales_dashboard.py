import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 5px 0;
    }
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def format_lakhs(value):
    try:
        return f"₹{float(value)/100000:,.2f}L"
    except (ValueError, TypeError):
        return "₹0.00L"

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# Title and Header
st.title("📊 Sales Dashboard")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    # Theme toggle
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0
    )
    
    # Sales Target Input
    st.header("Sales Target")
    sales_target = st.number_input(
        "Enter Sales Target (in Lakhs)",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

# Data Input Section
st.header("Data Input")
input_method = st.radio("Choose data input method:", ["Excel File", "Google Sheet URL"])

df = None
if input_method == "Excel File":
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Raw_Data')
            if 'Amount' in df.columns:
                df['Amount'] = df['Amount'].apply(safe_float)
            if 'Probability' in df.columns:
                df['Probability'] = df['Probability'].apply(safe_float)
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
else:
    sheet_url = st.text_input("Paste Google Sheet URL")
    if sheet_url:
        try:
            csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            df = pd.read_csv(csv_url)
            if 'Amount' in df.columns:
                df['Amount'] = df['Amount'].apply(safe_float)
            if 'Probability' in df.columns:
                df['Probability'] = df['Probability'].apply(safe_float)
        except Exception as e:
            st.error(f"Error reading Google Sheet: {str(e)}")

if df is not None:
    # Sidebar Filters
    with st.sidebar:
        st.header("Filters")
        
        # Practice filter
        practices = ['All'] + sorted(df['Practice'].astype(str).unique().tolist())
        selected_practice = st.selectbox("Practice", practices)
        
        # Quarter filter
        quarters = ['All'] + sorted(df['Quarter'].astype(str).unique().tolist())
        selected_quarter = st.selectbox("Quarter", quarters)
        
        # Hunting/Farming filter
        deal_types = ['All'] + sorted(df['Hunting/Farming'].astype(str).unique().tolist())
        selected_deal_type = st.selectbox("Hunting/Farming", deal_types)
        
        # Sales Owner filter (if available)
        if 'Sales Owner' in df.columns:
            sales_owners = ['All'] + sorted(df['Sales Owner'].astype(str).unique().tolist())
            selected_sales_owner = st.selectbox("Sales Owner", sales_owners)
        
        # Tech Owner filter (if available)
        if 'Tech Owner' in df.columns:
            tech_owners = ['All'] + sorted(df['Tech Owner'].astype(str).unique().tolist())
            selected_tech_owner = st.selectbox("Tech Owner", tech_owners)

    # Apply filters
    filtered_df = df.copy()
    if selected_practice != 'All':
        filtered_df = filtered_df[filtered_df['Practice'].astype(str) == selected_practice]
    if selected_quarter != 'All':
        filtered_df = filtered_df[filtered_df['Quarter'].astype(str) == selected_quarter]
    if selected_deal_type != 'All':
        filtered_df = filtered_df[filtered_df['Hunting/Farming'].astype(str) == selected_deal_type]
    if 'Sales Owner' in df.columns and selected_sales_owner != 'All':
        filtered_df = filtered_df[filtered_df['Sales Owner'].astype(str) == selected_sales_owner]
    if 'Tech Owner' in df.columns and selected_tech_owner != 'All':
        filtered_df = filtered_df[filtered_df['Tech Owner'].astype(str) == selected_tech_owner]

    # Calculate KPIs (in Lakhs)
    current_pipeline = filtered_df['Amount'].sum() / 100000
    weighted_projection = (filtered_df['Amount'] * filtered_df['Probability'] / 100).sum() / 100000
    closed_won = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
    achieved_percentage = (closed_won / sales_target * 100) if sales_target > 0 else 0

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Practice Analysis", "Deal Distribution", "Detailed View"])

    # Overview Tab
    with tab1:
        st.header("Key Performance Indicators")
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric(
                "Sales Target",
                format_lakhs(sales_target * 100000),
                delta=None,
                delta_color="normal"
            )
            st.metric(
                "Current Pipeline",
                format_lakhs(current_pipeline * 100000),
                delta=None,
                delta_color="normal"
            )
        
        with kpi_col2:
            st.metric(
                "Weighted Projection",
                format_lakhs(weighted_projection * 100000),
                delta=None,
                delta_color="normal"
            )
            st.metric(
                "Closed Won",
                format_lakhs(closed_won * 100000),
                delta=None,
                delta_color="normal"
            )
        
        with kpi_col3:
            st.metric(
                "Achieved %",
                f"{achieved_percentage:.1f}%",
                delta=None,
                delta_color="normal"
            )

    # Practice Analysis Tab
    with tab2:
        st.header("Practice-wise Summary")
        practice_summary = filtered_df.groupby('Practice').agg({
            'Amount': ['sum', 'count'],
            'Probability': 'mean'
        }).reset_index()
        
        practice_summary.columns = ['Practice', 'Total Amount (Lakhs)', 'Number of Deals', 'Avg Probability']
        practice_summary['Total Amount (Lakhs)'] = practice_summary['Total Amount (Lakhs)'] / 100000
        
        # Display practice summary table
        st.dataframe(
            practice_summary.style.format({
                'Total Amount (Lakhs)': '₹{:.2f}L',
                'Avg Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

    # Deal Distribution Tab
    with tab3:
        st.header("Hunting vs Farming Distribution")
        
        # Calculate percentages
        hunting_farming = filtered_df.groupby('Hunting/Farming')['Amount'].sum().reset_index()
        total_amount = hunting_farming['Amount'].sum()
        hunting_farming['Percentage'] = (hunting_farming['Amount'] / total_amount * 100).round(1)
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=hunting_farming['Hunting/Farming'],
            values=hunting_farming['Amount'] / 100000,  # Convert to Lakhs
            hole=.4,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Distribution of Hunting vs Farming (in Lakhs)",
            showlegend=True,
            annotations=[dict(text='Hunting/Farming', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Detailed View Tab
    with tab4:
        st.header("Detailed Deals")
        
        # Add Weighted Revenue column
        filtered_df['Weighted Revenue'] = filtered_df['Amount'] * filtered_df['Probability'] / 100
        
        # Define columns for display
        columns_to_show = [
            'Opportunity Number',
            'Organization Name',
            'Amount',
            'Probability',
            'Weighted Revenue',
            'Quarter',
            'Practice',
            'Sales Stage',
            'Tech Owner',
            'Sales Owner',
            'Expected Close Date'
        ]
        
        # Filter columns that exist in the dataframe
        available_columns = [col for col in columns_to_show if col in filtered_df.columns]
        
        # Display table with formatting
        st.dataframe(
            filtered_df[available_columns].style.format({
                'Amount': '₹{:.2f}L',
                'Weighted Revenue': '₹{:.2f}L',
                'Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

        # Export to CSV option
        csv = filtered_df[available_columns].to_csv(index=False)
        st.download_button(
            label="Export to CSV",
            data=csv,
            file_name="filtered_deals.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload data to view the dashboard.")
