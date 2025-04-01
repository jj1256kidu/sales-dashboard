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
    
    # Date filtering
    if 'Expected Close Date' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
        current_date = pd.Timestamp.now()
        
        # Calculate MTD and YTD flags
        df['MTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month == current_date.month)
        df['YTD'] = (df['Expected Close Date'].dt.year == current_date.year) & (df['Expected Close Date'].dt.month <= current_date.month)
    
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # I. Top KPI Cards
        st.markdown("""
            <div style='background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h2 style='color: white; margin: 0; text-align: center;'>🎯 Key Performance Indicators</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate core metrics
        won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
        won_amount = won_deals['Amount'].sum() / 100000
        
        pipeline_df = df[~df['Sales Stage'].str.contains('Won|Lost', case=False, na=False)]
        total_pipeline = pipeline_df['Amount'].sum() / 100000
        
        # Calculate Committed vs Upside if Status column exists
        committed_deals = 0
        upside_deals = 0
        if 'Status' in df.columns:
            committed_deals = df[df['Status'] == 'Committed for the Month']['Amount'].sum() / 100000
            upside_deals = df[df['Status'] == 'Upside for the Month']['Amount'].sum() / 100000
        
        target = float(st.session_state.sales_target)
        achievement_pct = (won_amount / target * 100) if target > 0 else 0
        
        # Display KPIs in three columns with custom styling
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #4A90E2;'>
                    <h3 style='margin: 0; color: #4A90E2;'>🎯 Target Setting</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Target with edit option
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
            
            st.markdown(f"""
                <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #2ecc71; margin-top: 10px;'>
                    <h3 style='margin: 0; color: #2ecc71;'>✅ Closed Won</h3>
                    <h2 style='margin: 10px 0; color: #2ecc71;'>₹{won_amount:,.2f}L</h2>
                    <p style='margin: 0; color: #666;'>Achievement: {achievement_pct:.1f}% of Target</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db;'>
                    <h3 style='margin: 0; color: #3498db;'>📈 Pipeline Health</h3>
                    <h2 style='margin: 10px 0; color: #3498db;'>₹{total_pipeline:,.2f}L</h2>
                    <p style='margin: 0; color: #666;'>{(total_pipeline/target*100 if target > 0 else 0):.1f}% of Target</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #e74c3c; margin-top: 10px;'>
                    <h3 style='margin: 0; color: #e74c3c;'>📉 Target Gap</h3>
                    <h2 style='margin: 10px 0; color: #e74c3c;'>₹{(target - won_amount):,.2f}L</h2>
                    <p style='margin: 0; color: #666;'>{(100 - achievement_pct):.1f}% remaining</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if 'Status' in df.columns:
                st.markdown(f"""
                    <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #f1c40f;'>
                        <h3 style='margin: 0; color: #f1c40f;'>💼 Deal Mix</h3>
                        <h2 style='margin: 10px 0; color: #f1c40f;'>₹{committed_deals:,.2f}L</h2>
                        <p style='margin: 0; color: #666;'>Committed: {(committed_deals/total_pipeline*100 if total_pipeline > 0 else 0):.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #9b59b6; margin-top: 10px;'>
                        <h3 style='margin: 0; color: #9b59b6;'>📊 Upside Potential</h3>
                        <h2 style='margin: 10px 0; color: #9b59b6;'>₹{upside_deals:,.2f}L</h2>
                        <p style='margin: 0; color: #666;'>Upside: {(upside_deals/total_pipeline*100 if total_pipeline > 0 else 0):.1f}%</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #2ecc71;'>
                        <h3 style='margin: 0; color: #2ecc71;'>🎯 Win Rate</h3>
                        <h2 style='margin: 10px 0; color: #2ecc71;'>{(len(won_deals) / len(df) * 100):.1f}%</h2>
                        <p style='margin: 0; color: #666;'>{len(won_deals)}/{len(df)} deals</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # II. Business Mix Analysis
        st.markdown("### 📊 Business Mix Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Hunting vs Farming Split
            if 'Type' in df.columns and not df['Type'].isna().all():
                type_data = df.groupby('Type').agg({
                    'Amount': 'sum',
                    'id': 'count'
                }).reset_index()
                
                type_data['Amount'] = type_data['Amount'] / 100000
                total_amount = type_data['Amount'].sum()
                total_count = type_data['id'].sum()
                
                fig_type = go.Figure(go.Pie(
                    values=type_data['Amount'],
                    labels=type_data['Type'],
                    hole=0.6,
                    textinfo='label+percent+value',
                    text=type_data.apply(lambda x: f"{x['Type']}<br>₹{x['Amount']:,.1f}L<br>{(x['Amount']/total_amount*100):.1f}%<br>{x['id']} deals", axis=1),
                    hovertemplate="<b>%{label}</b><br>" +
                                "Amount: ₹%{value:,.1f}L<br>" +
                                "Percentage: %{percent}<br>" +
                                "Deal Count: %{text}<br>" +
                                "<extra></extra>"
                ))
                
                fig_type.update_layout(
                    title="Hunting vs Farming Split",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_type, use_container_width=True)
            else:
                st.info("Hunting vs Farming data is not available in the dataset.")
        
        with col2:
            # Geographical Split
            if 'Region' in df.columns and not df['Region'].isna().all():
                region_data = df.groupby('Region').agg({
                    'Amount': 'sum',
                    'id': 'count'
                }).reset_index()
                
                region_data['Amount'] = region_data['Amount'] / 100000
                total_amount = region_data['Amount'].sum()
                total_count = region_data['id'].sum()
                
                fig_geo = go.Figure(go.Pie(
                    values=region_data['Amount'],
                    labels=region_data['Region'],
                    hole=0.6,
                    textinfo='label+percent+value',
                    text=region_data.apply(lambda x: f"{x['Region']}<br>₹{x['Amount']:,.1f}L<br>{(x['Amount']/total_amount*100):.1f}%<br>{x['id']} deals", axis=1),
                    hovertemplate="<b>%{label}</b><br>" +
                                "Amount: ₹%{value:,.1f}L<br>" +
                                "Percentage: %{percent}<br>" +
                                "Deal Count: %{text}<br>" +
                                "<extra></extra>"
                ))
                
                fig_geo.update_layout(
                    title="Geographical Distribution",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_geo, use_container_width=True)
            else:
                st.info("Geographical data is not available in the dataset.")
        
        # III. Target vs Achievement
        st.markdown("### 🎯 Target vs Achievement")
        
        if 'Expected Close Date' in df.columns:
            # Monthly performance trend
            monthly_performance = df.groupby(df['Expected Close Date'].dt.strftime('%b %Y', na='Unknown')).agg({
                'Amount': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000
            }).reset_index()
            monthly_performance.columns = ['Month', 'Achievement']
            
            # Add target line
            monthly_target = target / 12
            
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
                barmode='group'
            )
            
            st.plotly_chart(fig_achievement, use_container_width=True)
        
        # IV. Pipeline Analysis
        st.markdown("### 🕳️ Pipeline Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Sales Funnel
            stage_data = df.groupby('Sales Stage').agg({
                'Amount': 'sum',
                'id': 'count'
            }).reset_index()
            
            stage_data['Amount'] = stage_data['Amount'] / 100000
            
            fig_funnel = go.Figure(go.Funnel(
                y=stage_data['Sales Stage'],
                x=stage_data['Amount'],
                textposition="inside",
                textinfo="value+percent initial",
                marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]}
            ))
            
            fig_funnel.update_layout(
                title="Pipeline Funnel",
                height=400
            )
            
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col2:
            # Deal Alerts
            st.markdown("#### 🚨 Deal Alerts")
            
            # High-value deals
            high_value_deals = pipeline_df.nlargest(3, 'Amount')
            for _, deal in high_value_deals.iterrows():
                st.markdown(f"""
                    💰 **High Value Deal**: ₹{deal['Amount']/100000:,.1f}L  
                    Stage: {deal['Sales Stage']}
                """)
            
            # Recent Wins
            st.markdown("#### 🏆 Recent Wins")
            recent_wins = won_deals.nlargest(3, 'Amount')
            for _, deal in recent_wins.iterrows():
                st.markdown(f"✨ ₹{deal['Amount']/100000:,.1f}L")
    
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
