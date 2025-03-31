import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for KPI cards
st.markdown("""
    <style>
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
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Sales Dashboard")

# Data Input Section
st.header("Data Input")
input_method = st.radio("Choose data input method:", ["Excel File", "Google Sheet URL"])

df = None
if input_method == "Excel File":
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx'])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Raw_Data')
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
else:
    sheet_url = st.text_input("Paste Google Sheet URL")
    if sheet_url:
        try:
            csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            df = pd.read_csv(csv_url)
        except Exception as e:
            st.error(f"Error reading Google Sheet: {str(e)}")

if df is not None:
    # Sales Target Input
    st.header("Sales Target")
    sales_target = st.number_input("Enter Sales Target (in Lakhs)", min_value=0.0, value=100.0)

    # Filters
    st.header("Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        practices = ['All'] + sorted(df['Practice'].unique().tolist())
        selected_practice = st.selectbox("Practice", practices)
    
    with col2:
        quarters = ['All'] + sorted(df['Quarter'].unique().tolist())
        selected_quarter = st.selectbox("Quarter", quarters)
    
    with col3:
        deal_types = ['All'] + sorted(df['Hunting/Farming'].unique().tolist())
        selected_deal_type = st.selectbox("Hunting/Farming", deal_types)

    # Apply filters
    filtered_df = df.copy()
    if selected_practice != 'All':
        filtered_df = filtered_df[filtered_df['Practice'] == selected_practice]
    if selected_quarter != 'All':
        filtered_df = filtered_df[filtered_df['Quarter'] == selected_quarter]
    if selected_deal_type != 'All':
        filtered_df = filtered_df[filtered_df['Hunting/Farming'] == selected_deal_type]

    # Calculate KPIs
    current_pipeline = filtered_df['Amount'].sum()
    weighted_projection = (filtered_df['Amount'] * filtered_df['Probability'] / 100).sum()
    closed_won = filtered_df[filtered_df['Sales Stage'].isin(['Closed Won', 'Won'])]['Amount'].sum()
    achieved_percentage = (closed_won / sales_target * 100) if sales_target > 0 else 0

    # Display KPIs
    st.header("Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Sales Target</div>
                <div class="kpi-value">₹{sales_target:.2f}L</div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Current Pipeline</div>
                <div class="kpi-value">₹{current_pipeline:.2f}L</div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Weighted Projection</div>
                <div class="kpi-value">₹{weighted_projection:.2f}L</div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Closed Won</div>
                <div class="kpi-value">₹{closed_won:.2f}L</div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_col5:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Achieved %</div>
                <div class="kpi-value">{achieved_percentage:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    # Practice-wise Summary
    st.header("Practice-wise Summary")
    practice_summary = filtered_df.groupby('Practice')['Amount'].agg(['sum', 'count']).reset_index()
    practice_summary.columns = ['Practice', 'Total Amount (Lakhs)', 'Number of Deals']
    
    fig = px.bar(practice_summary, x='Practice', y='Total Amount (Lakhs)',
                 title='Practice-wise Sales Distribution')
    st.plotly_chart(fig, use_container_width=True)

    # Detailed Deals Table
    st.header("Detailed Deals")
    selected_columns = [
        'Organization Name', 'Opportunity Name', 'Geography', 'Expected Close Date',
        'Probability', 'Amount', 'Sales Owner', 'Tech Owner'
    ]
    
    # Add Weighted Revenue column
    filtered_df['Weighted Revenue'] = filtered_df['Amount'] * filtered_df['Probability'] / 100
    
    # Display table with selected columns
    st.dataframe(
        filtered_df[selected_columns + ['Weighted Revenue']].style.format({
            'Amount': '₹{:.2f}L',
            'Weighted Revenue': '₹{:.2f}L',
            'Probability': '{:.1f}%'
        }),
        use_container_width=True
    )

    # Export to CSV option
    csv = filtered_df[selected_columns + ['Weighted Revenue']].to_csv(index=False)
    st.download_button(
        label="Export to CSV",
        data=csv,
        file_name="filtered_deals.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload data to view the dashboard.") 