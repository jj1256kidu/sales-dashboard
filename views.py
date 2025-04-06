import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from auth import check_password, init_session_state, show_login_page

# Custom CSS for the dashboard
st.markdown("""
    <style>
        /* Custom header styles */
        .custom-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: white;
        }
        
        .custom-header h1 {
            margin: 0;
            font-size: 2em;
            font-weight: 600;
            text-align: center;
        }
        
        /* Metric styles */
        .metric-label {
            color: #2a5298;
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .metric-value {
            color: #1e3c72;
            font-size: 1.8em;
            font-weight: 700;
            margin: 5px 0;
        }
        
        /* Upload container */
        .upload-container {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        /* Info box */
        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .info-box h4 {
            color: #2a5298;
            margin-bottom: 10px;
        }
        
        .info-box ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .info-box li {
            margin-bottom: 5px;
            color: #666;
        }
    </style>
""", unsafe_allow_html=True)

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
                    manual_df.to_excel("sales_data.xlsx", index=False)
                    st.success("Manual data saved successfully!")
                    
                    # Load the data
                    st.session_state.df = load_data()
                    if not st.session_state.df.empty:
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

def show_quarterly_summary(df):
    if df is None:
        st.warning("Please upload your sales data to view quarterly summary")
        return
    
    st.title("Quarterly Sales Summary")
    
    # Add quarter selection
    quarters = sorted(df['Quarter'].unique())
    selected_quarter = st.selectbox("Select Quarter", quarters)
    
    # Filter data for selected quarter
    quarter_data = df[df['Quarter'] == selected_quarter]
    
    # Calculate metrics
    total_pipeline = quarter_data[~quarter_data['Is_Won']]['Amount_Lacs'].sum()
    total_closed = quarter_data[quarter_data['Is_Won']]['Amount_Lacs'].sum()
    total_deals = len(quarter_data)
    closed_deals = len(quarter_data[quarter_data['Is_Won']])
    win_rate = (closed_deals / total_deals * 100) if total_deals > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipeline", f"₹{int(total_pipeline)}L")
    with col2:
        st.metric("Closed Won", f"₹{int(total_closed)}L")
    with col3:
        st.metric("Total Deals", total_deals)
    with col4:
        st.metric("Win Rate", f"{int(win_rate)}%")
    
    # Practice-wise summary
    st.subheader("Practice-wise Summary")
    practice_summary = quarter_data.groupby('Practice').agg({
        'Amount_Lacs': ['sum', 'count'],
        'Is_Won': 'sum'
    }).reset_index()
    
    practice_summary.columns = ['Practice', 'Total Amount', 'Total Deals', 'Closed Deals']
    practice_summary['Win Rate'] = (practice_summary['Closed Deals'] / practice_summary['Total Deals'] * 100).round(1)
    
    st.dataframe(practice_summary, use_container_width=True)
    
    # Monthly trend
    st.subheader("Monthly Trend")
    monthly_data = quarter_data.groupby('Month').agg({
        'Amount_Lacs': 'sum',
        'Is_Won': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly_data['Month'],
        y=monthly_data['Amount_Lacs'],
        name='Total Amount',
        marker_color='#4A90E2'
    ))
    fig.add_trace(go.Bar(
        x=monthly_data['Month'],
        y=monthly_data['Is_Won'],
        name='Closed Deals',
        marker_color='#2ECC71'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Monthly Sales Performance',
        xaxis_title='Month',
        yaxis_title='Amount (Lakhs)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_previous_data_view(df):
    if df is None:
        st.warning("Please upload your sales data to view previous data")
        return
    
    st.title("Previous Data Tracking")
    
    # Add year selection
    years = sorted(df['Year'].unique())
    selected_year = st.selectbox("Select Year", years)
    
    # Filter data for selected year
    year_data = df[df['Year'] == selected_year]
    
    # Calculate metrics
    total_pipeline = year_data[~year_data['Is_Won']]['Amount_Lacs'].sum()
    total_closed = year_data[year_data['Is_Won']]['Amount_Lacs'].sum()
    total_deals = len(year_data)
    closed_deals = len(year_data[year_data['Is_Won']])
    win_rate = (closed_deals / total_deals * 100) if total_deals > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipeline", f"₹{int(total_pipeline)}L")
    with col2:
        st.metric("Closed Won", f"₹{int(total_closed)}L")
    with col3:
        st.metric("Total Deals", total_deals)
    with col4:
        st.metric("Win Rate", f"{int(win_rate)}%")
    
    # Quarterly trend
    st.subheader("Quarterly Trend")
    quarterly_data = year_data.groupby('Quarter').agg({
        'Amount_Lacs': 'sum',
        'Is_Won': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=quarterly_data['Quarter'],
        y=quarterly_data['Amount_Lacs'],
        name='Total Amount',
        marker_color='#4A90E2'
    ))
    fig.add_trace(go.Bar(
        x=quarterly_data['Quarter'],
        y=quarterly_data['Is_Won'],
        name='Closed Deals',
        marker_color='#2ECC71'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Quarterly Sales Performance',
        xaxis_title='Quarter',
        yaxis_title='Amount (Lakhs)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Practice-wise summary
    st.subheader("Practice-wise Summary")
    practice_summary = year_data.groupby('Practice').agg({
        'Amount_Lacs': ['sum', 'count'],
        'Is_Won': 'sum'
    }).reset_index()
    
    practice_summary.columns = ['Practice', 'Total Amount', 'Total Deals', 'Closed Deals']
    practice_summary['Win Rate'] = (practice_summary['Closed Deals'] / practice_summary['Total Deals'] * 100).round(1)
    
    st.dataframe(practice_summary, use_container_width=True) 
