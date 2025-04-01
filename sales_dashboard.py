import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import io

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
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
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
</style>
""", unsafe_allow_html=True)

def show_data_input():
    # Custom header
    st.markdown("""
        <div class="custom-header">
            <h1>📊 Sales Dashboard</h1>
            <p style="font-size: 1.2em; margin: 0;">Upload your sales data to get started</p>
        </div>
    """, unsafe_allow_html=True)

    # Main upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your Excel or CSV file here",
            type=['xlsx', 'csv'],
            help="Upload your sales data file (Excel or CSV format)"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    # Handle Excel files
                    excel_file = pd.ExcelFile(uploaded_file)
                    sheet_name = st.selectbox("Select Sheet", excel_file.sheet_names)
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                else:
                    # Handle CSV files
                    df = pd.read_csv(uploaded_file)
                
                st.session_state.df = df
                st.success(f"✅ Successfully loaded {len(df):,} rows of data!")
                
                # Preview the data
                st.subheader("Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>📋 Required Columns</h4>
            <ul>
                <li>Amount</li>
                <li>Sales Stage</li>
                <li>Expected Close Date</li>
                <li>Practice/Region</li>
            </ul>
            <h4>📁 Supported Formats</h4>
            <ul>
                <li>Excel (.xlsx)</li>
                <li>CSV (.csv)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_overview():
    if st.session_state.df is None:
        st.warning("Please upload your data first!")
        return
    
    st.title("📈 Sales Overview")
    
    df = st.session_state.df.copy()  # Create a copy to avoid modifying original data
    
    # Initialize target if not in session state
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0

    # Filters section in an expander
    with st.expander("📊 Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        # Time filter
        with col1:
            if 'Expected Close Date' in df.columns:
                df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'])
                min_date = df['Expected Close Date'].min()
                max_date = df['Expected Close Date'].max()
                
                date_filter = st.date_input(
                    "Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="date_filter"
                )
                if len(date_filter) == 2:
                    start_date, end_date = date_filter
                    df = df[
                        (df['Expected Close Date'].dt.date >= start_date) &
                        (df['Expected Close Date'].dt.date <= end_date)
                    ]
        
        # Practice filter
        with col2:
            if 'Practice' in df.columns:
                practices = ['All'] + sorted(df['Practice'].unique().tolist())
                selected_practice = st.selectbox("Practice", practices)
                if selected_practice != 'All':
                    df = df[df['Practice'] == selected_practice]
        
        # Sales Stage filter
        with col3:
            if 'Sales Stage' in df.columns:
                stages = ['All'] + sorted(df['Sales Stage'].unique().tolist())
                selected_stage = st.selectbox("Sales Stage", stages)
                if selected_stage != 'All':
                    df = df[df['Sales Stage'] == selected_stage]

    # KPI Row
    st.markdown("### 📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_amount = df['Amount'].sum() if 'Amount' in df.columns else 0
        st.metric("Total Pipeline", f"₹{total_amount:,.2f}L")
    
    with col2:
        if 'Sales Stage' in df.columns:
            won_amount = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum()
            st.metric("Won Amount", f"₹{won_amount:,.2f}L")
    
    with col3:
        if 'Sales Stage' in df.columns:
            win_rate = (df['Sales Stage'].str.contains('Won', case=False, na=False).sum() / len(df)) * 100
            st.metric("Win Rate", f"{win_rate:.1f}%")
    
    with col4:
        # Manual target input
        target = st.number_input(
            "Set Target (in Lakhs)",
            value=float(st.session_state.sales_target),
            step=1.0,
            key="target_input"
        )
        st.session_state.sales_target = target

    # Hunting vs Farming Split
    st.markdown("### 🎯 Hunting vs Farming Split")
    if 'Type' in df.columns:
        # Create mapping for cleaner labels
        df['Business Type'] = df['Type'].map({
            'Existing Business (Farming)': 'Farming',
            'New Business (Hunting)': 'Hunting'
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for deal count
            hunt_farm_count = df['Business Type'].value_counts()
            fig_count = px.pie(
                values=hunt_farm_count.values,
                names=hunt_farm_count.index,
                title="Deal Distribution (Count)",
                color_discrete_sequence=['#4A90E2', '#45B7AF'],
                hole=0.4
            )
            fig_count.update_traces(textposition='outside', textinfo='percent+label')
            st.plotly_chart(fig_count, use_container_width=True)
        
        with col2:
            # Bar chart for amount
            hunt_farm_amount = df.groupby('Business Type')['Amount'].sum().reset_index()
            fig_amount = px.bar(
                hunt_farm_amount,
                x='Business Type',
                y='Amount',
                title="Revenue Distribution",
                color='Business Type',
                color_discrete_sequence=['#4A90E2', '#45B7AF'],
                text=hunt_farm_amount['Amount'].apply(lambda x: f'₹{x:,.2f}L')
            )
            fig_amount.update_traces(textposition='outside')
            fig_amount.update_layout(showlegend=True)
            st.plotly_chart(fig_amount, use_container_width=True)
            
        # Add summary metrics
        col1, col2 = st.columns(2)
        with col1:
            farming_amount = df[df['Type'] == 'Existing Business (Farming)']['Amount'].sum()
            st.metric("Farming Revenue", f"₹{farming_amount:,.2f}L")
        with col2:
            hunting_amount = df[df['Type'] == 'New Business (Hunting)']['Amount'].sum()
            st.metric("Hunting Revenue", f"₹{hunting_amount:,.2f}L")
    else:
        st.info("Business Type classification not found in the dataset")

    # Target vs Closed Won
    st.markdown("### 💰 Target vs Achievement")
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly trend
        if 'Expected Close Date' in df.columns:
            monthly_data = df[df['Sales Stage'].str.contains('Won', case=False, na=False)].groupby(
                df['Expected Close Date'].dt.strftime('%Y-%m')
            )['Amount'].sum().reset_index()
            monthly_data['Target'] = st.session_state.sales_target / 12  # Monthly target
            
            fig_target = go.Figure()
            fig_target.add_trace(go.Bar(
                x=monthly_data['Expected Close Date'],
                y=monthly_data['Amount'],
                name='Achieved'
            ))
            fig_target.add_trace(go.Scatter(
                x=monthly_data['Expected Close Date'],
                y=monthly_data['Target'],
                name='Target',
                line=dict(color='red', dash='dash')
            ))
            fig_target.update_layout(title='Monthly Achievement vs Target')
            st.plotly_chart(fig_target, use_container_width=True)
    
    with col2:
        # Progress gauge
        total_won = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]['Amount'].sum()
        achievement_percentage = (total_won / st.session_state.sales_target * 100) if st.session_state.sales_target > 0 else 0
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=achievement_percentage,
            title={'text': "Target Achievement"},
            gauge={'axis': {'range': [None, 100]},
                  'bar': {'color': "darkblue"},
                  'steps': [
                      {'range': [0, 50], 'color': "lightgray"},
                      {'range': [50, 75], 'color': "gray"},
                      {'range': [75, 100], 'color': "darkgray"}
                  ]}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Geographical Split
    st.markdown("### 🌍 Geographical Distribution")
    if 'Region' in df.columns or 'Geography' in df.columns:
        geo_col = 'Region' if 'Region' in df.columns else 'Geography'
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Region-wise revenue
            geo_data = df.groupby(geo_col)['Amount'].sum().reset_index()
            fig_geo = px.bar(
                geo_data,
                x=geo_col,
                y='Amount',
                title=f"Revenue by {geo_col}",
                color=geo_col
            )
            st.plotly_chart(fig_geo, use_container_width=True)
        
        with col2:
            # Region-wise deal count
            geo_count = df.groupby(geo_col).size().reset_index(name='Count')
            fig_geo_count = px.pie(
                geo_count,
                values='Count',
                names=geo_col,
                title=f"Deal Distribution by {geo_col}"
            )
            st.plotly_chart(fig_geo_count, use_container_width=True)
    else:
        st.info("Geographical information not found in the dataset")

    # Committed vs Upside
    st.markdown("### 📊 Committed vs Upside")
    if 'Deal Type' in df.columns:  # Assuming 'Deal Type' contains Committed/Upside classification
        col1, col2 = st.columns(2)
        
        with col1:
            # Amount distribution
            deal_type_amount = df.groupby('Deal Type')['Amount'].sum().reset_index()
            fig_deal_type = px.bar(
                deal_type_amount,
                x='Deal Type',
                y='Amount',
                title="Revenue: Committed vs Upside",
                color='Deal Type'
            )
            st.plotly_chart(fig_deal_type, use_container_width=True)
        
        with col2:
            # Deal count distribution
            deal_type_count = df['Deal Type'].value_counts()
            fig_deal_count = px.pie(
                values=deal_type_count.values,
                names=deal_type_count.index,
                title="Distribution: Committed vs Upside"
            )
            st.plotly_chart(fig_deal_count, use_container_width=True)
    else:
        st.info("Committed/Upside classification not found in the dataset")

def show_detailed():
    if st.session_state.df is None:
        st.warning("Please upload your data first!")
        return
    
    st.title("🔍 Detailed View")
    
    df = st.session_state.df
    
    # Search and filters
    search = st.text_input("🔍 Search", placeholder="Search in any column...")
    
    # Filter the dataframe based on search
    if search:
        mask = np.column_stack([df[col].astype(str).str.contains(search, case=False, na=False) 
                              for col in df.columns])
        df = df[mask.any(axis=1)]
    
    # Display the filtered dataframe
    st.dataframe(df, use_container_width=True)

def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        selected = st.radio(
            "Select View",
            options=["Data Input", "Overview", "Detailed View"],
            key="navigation"
        )
        
        st.session_state.current_view = selected.lower().replace(" ", "_")
    
    # Display the selected view
    if st.session_state.current_view == "data_input":
        show_data_input()
    elif st.session_state.current_view == "overview":
        show_overview()
    elif st.session_state.current_view == "detailed_view":
        show_detailed()

if __name__ == "__main__":
    main() 
