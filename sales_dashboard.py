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
if 'date_filter' not in st.session_state:
    st.session_state.date_filter = None
if 'selected_practice' not in st.session_state:
    st.session_state.selected_practice = 'All'
if 'selected_stage' not in st.session_state:
    st.session_state.selected_stage = 'All'
if 'reset_triggered' not in st.session_state:
    st.session_state.reset_triggered = False

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
    
    st.title("Sales Overview")
    
    df = st.session_state.df.copy()
    
    # Initialize target if not in session state
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0
    
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # I. Target Setting & Achievement
        st.markdown("""
            <div style='background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h2 style='color: white; margin: 0; text-align: center;'>🎯 Target Setting & Achievement</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Manual target input
            new_target = st.number_input(
                "Annual Target (Lakhs)",
                value=float(st.session_state.sales_target),
                step=1.0,
                format="%.2f",
                help="Enter annual target in Lakhs (1L = ₹100,000)"
            )
            if new_target != st.session_state.sales_target:
                st.session_state.sales_target = new_target
                st.rerun()
        
        with col2:
            # Current achievement
            won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
            won_amount = won_deals['Amount'].sum() / 100000
            achievement_pct = (won_amount / new_target * 100) if new_target > 0 else 0
            
            st.markdown(f"""
                <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #2ecc71;'>
                    <h3 style='margin: 0; color: #2ecc71;'>Current Achievement</h3>
                    <h2 style='margin: 10px 0; color: #2ecc71;'>₹{won_amount:,.2f}L</h2>
                    <p style='margin: 0; color: #666;'>Achievement: {achievement_pct:.1f}% of Target</p>
                </div>
            """, unsafe_allow_html=True)
        
        # II. Target vs Achievement Trend
        st.markdown("### 📈 Target vs Achievement Trend")
        
        if 'Expected Close Date' in df.columns:
            # Monthly performance trend
            monthly_performance = df.groupby(df['Expected Close Date'].dt.strftime('%b %Y', na='Unknown')).agg({
                'Amount': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000
            }).reset_index()
            monthly_performance.columns = ['Month', 'Achievement']
            
            # Sort months chronologically
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            monthly_performance['Month'] = pd.Categorical(monthly_performance['Month'], categories=month_order, ordered=True)
            monthly_performance = monthly_performance.sort_values('Month')
            
            # Add target line
            monthly_target = new_target / 12
            
            fig_achievement = go.Figure()
            
            # Add target line
            fig_achievement.add_trace(go.Scatter(
                x=monthly_performance['Month'],
                y=[monthly_target] * len(monthly_performance),
                name='Monthly Target',
                line=dict(color='red', dash='dash')
            ))
            
            # Add achievement bars
            fig_achievement.add_trace(go.Bar(
                x=monthly_performance['Month'],
                y=monthly_performance['Achievement'],
                name='Achievement',
                text=monthly_performance['Achievement'].apply(lambda x: f'₹{x:,.1f}L<br>{(x/monthly_target*100 if monthly_target > 0 else 0):.1f}%'),
                textposition='outside'
            ))
            
            fig_achievement.update_layout(
                title="Monthly Target vs Achievement",
                height=400,
                barmode='group',
                xaxis_title="Month",
                yaxis_title="Amount (Lakhs)",
                showlegend=True
            )
            
            st.plotly_chart(fig_achievement, use_container_width=True)
        
        # III. Hunting vs Farming Split
        st.markdown("### 🎯 Hunting vs Farming Split")
        
        if 'Type' in df.columns and not df['Type'].isna().all():
            type_data = df.groupby('Type').agg({
                'Amount': 'sum',
                'id': 'count'
            }).reset_index()
            
            type_data['Amount'] = type_data['Amount'] / 100000
            total_amount = type_data['Amount'].sum()
            total_count = type_data['id'].sum()
            
            # Create a bar chart for better comparison
            fig_type = go.Figure()
            
            # Add amount bars
            fig_type.add_trace(go.Bar(
                x=type_data['Type'],
                y=type_data['Amount'],
                name='Amount (Lakhs)',
                text=type_data.apply(lambda x: f"₹{x['Amount']:,.1f}L<br>{(x['Amount']/total_amount*100):.1f}%", axis=1),
                textposition='outside'
            ))
            
            # Add deal count as secondary axis
            fig_type.add_trace(go.Scatter(
                x=type_data['Type'],
                y=type_data['id'],
                name='Deal Count',
                yaxis='y2',
                text=type_data['id'],
                textposition='top center'
            ))
            
            fig_type.update_layout(
                title="Hunting vs Farming Distribution",
                height=400,
                barmode='group',
                yaxis=dict(title='Amount (Lakhs)'),
                yaxis2=dict(
                    title='Deal Count',
                    overlaying='y',
                    side='right'
                ),
                showlegend=True
            )
            
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("Hunting vs Farming data is not available in the dataset.")
        
        # IV. Geography-wise Deal Split
        st.markdown("### 🌍 Geography-wise Deal Split")
        
        if 'Region' in df.columns and not df['Region'].isna().all():
            region_data = df.groupby('Region').agg({
                'Amount': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
                'id': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].count()
            }).reset_index()
            
            region_data.columns = ['Region', 'Closed Amount', 'Closed Deals']
            
            # Create a heatmap-like bar chart
            fig_geo = go.Figure()
            
            fig_geo.add_trace(go.Bar(
                x=region_data['Region'],
                y=region_data['Closed Amount'],
                name='Closed Amount',
                text=region_data.apply(lambda x: f"₹{x['Closed Amount']:,.1f}L<br>{x['Closed Deals']} deals", axis=1),
                textposition='outside',
                marker_color='#4A90E2'
            ))
            
            fig_geo.update_layout(
                title="Regional Performance",
                height=400,
                xaxis_title="Region",
                yaxis_title="Amount (Lakhs)",
                showlegend=True
            )
            
            st.plotly_chart(fig_geo, use_container_width=True)
        else:
            st.info("Geographical data is not available in the dataset.")
        
        # V. Committed vs Upside Analysis
        st.markdown("### 💼 Committed vs Upside Analysis")
        
        if 'Status' in df.columns and 'Expected Close Date' in df.columns:
            # Monthly committed vs upside
            monthly_status = df.groupby([
                df['Expected Close Date'].dt.strftime('%b %Y', na='Unknown'),
                'Status'
            ]).agg({
                'Amount': 'sum'
            }).reset_index()
            
            monthly_status['Amount'] = monthly_status['Amount'] / 100000
            monthly_status.columns = ['Month', 'Status', 'Amount']
            
            # Sort months chronologically
            monthly_status['Month'] = pd.Categorical(monthly_status['Month'], categories=month_order, ordered=True)
            monthly_status = monthly_status.sort_values('Month')
            
            # Create stacked column chart
            fig_status = go.Figure()
            
            for status in monthly_status['Status'].unique():
                status_data = monthly_status[monthly_status['Status'] == status]
                fig_status.add_trace(go.Bar(
                    x=status_data['Month'],
                    y=status_data['Amount'],
                    name=status,
                    text=status_data['Amount'].apply(lambda x: f"₹{x:,.1f}L"),
                    textposition='inside'
                ))
            
            fig_status.update_layout(
                title="Monthly Committed vs Upside",
                height=400,
                barmode='stack',
                xaxis_title="Month",
                yaxis_title="Amount (Lakhs)",
                showlegend=True
            )
            
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Status and date data are not available in the dataset.")
    
    else:
        st.error("Required columns (Sales Stage, Amount) not found in the dataset")

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
