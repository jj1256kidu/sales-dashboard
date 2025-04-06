import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from auth import check_password, init_session_state

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

def show_overview_view(df):
    """Display the overview section with key metrics and charts"""
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
            '>📊 Overview</h3>
        </div>
    """, unsafe_allow_html=True)

    if df is None or df.empty:
        st.warning("No data available. Please upload data first.")
        return

    # Calculate key metrics
    total_amount = df['Amount'].sum()
    total_won = df[df['Is_Won']]['Amount'].sum()
    total_weighted = df['Weighted_Amount'].sum()
    win_rate = (total_won / total_amount * 100) if total_amount > 0 else 0

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Amount", f"₹{total_amount:,.0f}")
    with col2:
        st.metric("Total Won", f"₹{total_won:,.0f}")
    with col3:
        st.metric("Weighted Amount", f"₹{total_weighted:,.0f}")
    with col4:
        st.metric("Win Rate", f"{win_rate:.1f}%")

    # Create charts
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Sales by Month</h4>', unsafe_allow_html=True)
    monthly_sales = df.groupby('Month')['Amount'].sum().reset_index()
    fig = px.bar(monthly_sales, x='Month', y='Amount', title='Sales by Month')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Sales by Stage</h4>', unsafe_allow_html=True)
    stage_sales = df.groupby('Sales Stage')['Amount'].sum().reset_index()
    fig = px.pie(stage_sales, values='Amount', names='Sales Stage', title='Sales by Stage')
    st.plotly_chart(fig, use_container_width=True)

def show_sales_team_view(df):
    """Display the sales team performance section"""
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
            '>👥 Sales Team Performance</h3>
        </div>
    """, unsafe_allow_html=True)

    if df is None or df.empty:
        st.warning("No data available. Please upload data first.")
        return

    # Calculate sales team metrics
    team_metrics = df.groupby('Sales Owner').agg({
        'Amount': 'sum',
        'Weighted_Amount': 'sum',
        'Is_Won': 'sum'
    }).reset_index()

    # Display team metrics
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Sales Team Metrics</h4>', unsafe_allow_html=True)
    st.dataframe(team_metrics, use_container_width=True)

    # Create charts
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Sales by Team Member</h4>', unsafe_allow_html=True)
    fig = px.bar(team_metrics, x='Sales Owner', y='Amount', title='Sales by Team Member')
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_data_view(df):
    """Display the detailed data view with filtering options"""
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
            '>📋 Detailed Data</h3>
        </div>
    """, unsafe_allow_html=True)

    if df is None or df.empty:
        st.warning("No data available. Please upload data first.")
        return

    # Add filters
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Filters</h4>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        sales_owner = st.multiselect("Sales Owner", df['Sales Owner'].unique())
    with col2:
        sales_stage = st.multiselect("Sales Stage", df['Sales Stage'].unique())
    with col3:
        min_amount = st.number_input("Minimum Amount", min_value=0, value=0)

    # Apply filters
    filtered_df = df.copy()
    if sales_owner:
        filtered_df = filtered_df[filtered_df['Sales Owner'].isin(sales_owner)]
    if sales_stage:
        filtered_df = filtered_df[filtered_df['Sales Stage'].isin(sales_stage)]
    if min_amount > 0:
        filtered_df = filtered_df[filtered_df['Amount'] >= min_amount]

    # Display filtered data
    st.markdown('<h4 style="color: #2a5298; margin: 20px 0 10px 0;">Filtered Data</h4>', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True) 
