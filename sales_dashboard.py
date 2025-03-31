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

# Custom CSS for modern styling
st.markdown("""
    <style>
    /* Main Layout */
    .main {
        padding: 2rem;
        background-color: #f8fafc;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Header Styling */
    .css-1v0mbdj {
        margin-bottom: 2rem;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 0 1.5rem;
        color: #64748b;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    }
    
    /* Metric Cards */
    .stMetric {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border: 1px solid #e2e8f0;
    }
    .stMetric:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease-in-out;
    }
    
    /* DataFrames */
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Selectbox Styling */
    .stSelectbox {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Number Input */
    .stNumberInput input {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Download Button */
    .stDownloadButton button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: 500;
    }
    .stDownloadButton button:hover {
        background-color: #2563eb;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e2e8f0;
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
    st.markdown("""
        <div class="section-header">
            <h3>⚙️ Settings</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0
    )
    
    # Sales Target Input
    st.markdown("""
        <div class="section-header">
            <h3>🎯 Sales Target</h3>
        </div>
    """, unsafe_allow_html=True)
    
    sales_target = st.number_input(
        "Enter Sales Target (in Lakhs)",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

# Data Input Section
st.markdown("""
    <div class="section-header">
        <h3>📁 Data Input</h3>
    </div>
""", unsafe_allow_html=True)

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
        st.markdown("""
            <div class="section-header">
                <h3>🔍 Filters</h3>
            </div>
        """, unsafe_allow_html=True)
        
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
    amount = filtered_df['Amount'].sum() / 100000
    closed_won = filtered_df[filtered_df['Sales Stage'].astype(str).isin(['Closed Won', 'Won'])]['Amount'].sum() / 100000
    achieved_percentage = (closed_won / sales_target * 100) if sales_target > 0 else 0

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Practice Analysis", "🎯 Deal Distribution", "📋 Detailed View"])

    # Overview Tab
    with tab1:
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Key Performance Indicators</h3>
            </div>
        """, unsafe_allow_html=True)
        
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
                "Amount",
                format_lakhs(amount * 100000),
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

        # Quarter-wise Breakdown
        st.markdown("""
            <div class="section-header">
                <h3>📅 Quarter-wise Breakdown</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate quarter-wise metrics
        quarter_metrics = filtered_df.groupby('Quarter').agg({
            'Amount': ['sum', 'count'],
            'Probability': 'mean'
        }).reset_index()
        
        quarter_metrics.columns = ['Quarter', 'Total Amount (Lakhs)', 'Number of Deals', 'Avg Probability']
        quarter_metrics['Total Amount (Lakhs)'] = quarter_metrics['Total Amount (Lakhs)'] / 100000
        
        # Display quarter summary table
        st.dataframe(
            quarter_metrics.style.format({
                'Total Amount (Lakhs)': '₹{:.2f}L',
                'Avg Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

        # Create quarter-wise bar chart
        fig = px.bar(
            quarter_metrics,
            x='Quarter',
            y='Total Amount (Lakhs)',
            title='Quarter-wise Pipeline Distribution',
            text='Total Amount (Lakhs)',
            labels={'Total Amount (Lakhs)': 'Amount (Lakhs)'}
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter"),
            xaxis_title="Quarter",
            yaxis_title="Amount (Lakhs)",
            showlegend=False
        )
        
        fig.update_traces(
            texttemplate='₹%{text:.2f}L',
            textposition='outside',
            marker_color='#3b82f6'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Practice Analysis Tab
    with tab2:
        st.markdown("""
            <div class="section-header">
                <h3>📈 Practice-wise Summary</h3>
            </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Hunting vs Farming Distribution</h3>
            </div>
        """, unsafe_allow_html=True)
        
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
            annotations=[dict(text='Hunting/Farming', x=0.5, y=0.5, font_size=20, showarrow=False)],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Detailed View Tab
    with tab4:
        st.markdown("""
            <div class="section-header">
                <h3>📋 Detailed Deals</h3>
            </div>
        """, unsafe_allow_html=True)
        
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
            label="📥 Export to CSV",
            data=csv,
            file_name="filtered_deals.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload data to view the dashboard.")
