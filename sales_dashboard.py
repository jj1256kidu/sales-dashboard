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
        margin: 20px 0 15px;
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
</style>
""", unsafe_allow_html=True)

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
            type=['xlsx', 'csv'],
            help="Upload your sales data file in Excel or CSV format"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    # Handle Excel files
                    excel_file = pd.ExcelFile(uploaded_file)
                    sheet_name = st.selectbox("Select Worksheet", excel_file.sheet_names)
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                else:
                    # Handle CSV files
                    df = pd.read_csv(uploaded_file)
                
                st.session_state.df = df
                st.success(f"Successfully loaded {len(df):,} records")
                
                # Preview the data
                st.subheader("Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>Required Data Fields</h4>
            <ul>
                <li>Amount</li>
                <li>Sales Stage</li>
                <li>Expected Close Date</li>
                <li>Practice/Region</li>
            </ul>
            <h4>File Formats</h4>
            <ul>
                <li>Excel (.xlsx)</li>
                <li>CSV (.csv)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_overview():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Sales Performance Overview")
    
    df = st.session_state.df.copy()
    
    # Initialize target if not in session state
    if 'sales_target' not in st.session_state:
        st.session_state.sales_target = 0
    
    if 'Sales Stage' in df.columns and 'Amount' in df.columns:
        # I. Target vs Closed Won
        st.markdown("""
            <div style='background: linear-gradient(90deg, #2ecc71 0%, #27ae60 100%); padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Target vs Closed Won</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Calculate achievement
        won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
        won_amount = won_deals['Amount'].sum() / 100000
        achievement_pct = (won_amount / st.session_state.sales_target * 100) if st.session_state.sales_target > 0 else 0
        
        # Manual target input
        new_target = st.number_input(
            "Annual Sales Target (Lakhs)",
            value=float(st.session_state.sales_target),
            step=1.0,
            format="%.2f",
            help="Enter the annual sales target in Lakhs (1L = ₹100,000)"
        )
        if new_target != st.session_state.sales_target:
            st.session_state.sales_target = new_target
            st.rerun()
        
        # Enhanced horizontal progress bar with metrics
        st.markdown(f"""
            <div style='background: #f0f2f6; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                    <div>
                        <h3 style='margin: 0; color: #2ecc71; font-size: 1.2em; font-weight: 500;'>Closed Won</h3>
                        <h2 style='margin: 8px 0; color: #2ecc71; font-size: 2.8em; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>₹{won_amount:,.2f}L</h2>
                    </div>
                    <div style='text-align: right;'>
                        <h3 style='margin: 0; color: #e74c3c; font-size: 1.2em; font-weight: 500;'>Target</h3>
                        <h2 style='margin: 8px 0; color: #e74c3c; font-size: 2.8em; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>₹{new_target:,.2f}L</h2>
                    </div>
                </div>
                <div style='background: #e74c3c; height: 40px; border-radius: 20px; overflow: hidden; position: relative; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);'>
                    <div style='background: #2ecc71; height: 100%; width: {min(100, achievement_pct)}%; transition: width 0.5s ease-in-out;'></div>
                    <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: 600; font-size: 1.2em; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
                        {achievement_pct:.1f}% Complete
                    </div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 10px; color: #666; font-size: 1.1em; font-weight: 400;'>
                    <span>₹0L</span>
                    <span>₹{new_target:,.1f}L</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # II. Practice
        st.markdown("""
            <div style='background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%); padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
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
            if selected_practice != 'All':
                df = df[df['Practice'] == selected_practice]
            
            # Calculate practice metrics
            practice_metrics = df.groupby('Practice').agg({
                'Amount': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
                'Sales Stage': lambda x: x[df['Sales Stage'].str.contains('Won', case=False, na=False)].count()
            }).reset_index()
            
            practice_metrics.columns = ['Practice', 'Closed Amount', 'Closed Deals']
            
            # Calculate total pipeline amount by practice
            total_pipeline = df.groupby('Practice')['Amount'].sum() / 100000
            practice_metrics['Total Pipeline'] = practice_metrics['Practice'].map(total_pipeline)
            
            # Calculate total deals by practice
            total_deals = df.groupby('Practice').size()
            practice_metrics['Pipeline Deals'] = practice_metrics['Practice'].map(total_deals) - practice_metrics['Closed Deals']
            
            # Sort practice metrics by Total Pipeline in descending order
            practice_metrics = practice_metrics.sort_values('Total Pipeline', ascending=False)
            
            # Create a comprehensive view
            col1, col2 = st.columns(2)
            
            with col1:
                # Practice-wise Pipeline Amount
                fig_pipeline = go.Figure()
                
                fig_pipeline.add_trace(go.Bar(
                    x=practice_metrics['Practice'],
                    y=practice_metrics['Total Pipeline'],
                    name='Total Pipeline',
                    text=practice_metrics['Total Pipeline'].apply(lambda x: f"₹{x:,.1f}L"),
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
                    text=practice_metrics['Closed Amount'].apply(lambda x: f"₹{x:,.1f}L"),
                    textposition='outside',
                    textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                    marker_color='#2ecc71',
                    marker_line=dict(color='#27ae60', width=2),
                    opacity=0.9
                ))
                
                fig_pipeline.update_layout(
                    title=dict(
                        text="Practice-wise Pipeline Amount",
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
                # Practice-wise Deal Count
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
                        text="Practice-wise Deal Count",
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
            
            # Add practice summary metrics
            st.markdown("### Practice Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_pipeline = practice_metrics['Total Pipeline'].sum()
                st.markdown(f"""
                    <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                        <div class='metric-label'>Total Pipeline</div>
                        <div class='metric-value'>₹{total_pipeline:,.1f}L</div>
                        <div style='color: #666; font-size: 0.9em;'>{practice_metrics['Total Pipeline'].sum() - practice_metrics['Closed Amount'].sum():,.1f}L remaining</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_deals = practice_metrics['Pipeline Deals'].sum() + practice_metrics['Closed Deals'].sum()
                st.markdown(f"""
                    <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                        <div class='metric-label'>Total Deals</div>
                        <div class='metric-value'>{total_deals:,}</div>
                        <div style='color: #666; font-size: 0.9em;'>{practice_metrics['Pipeline Deals'].sum():,} in pipeline</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_won = practice_metrics['Closed Deals'].sum()
                win_rate = (total_won / total_deals * 100) if total_deals > 0 else 0
                st.markdown(f"""
                    <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                        <div class='metric-label'>Win Rate</div>
                        <div class='metric-value'>{win_rate:.1f}%</div>
                        <div style='color: #666; font-size: 0.9em;'>{total_won:,} won</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col4:
                avg_deal_size = practice_metrics['Closed Amount'].sum() / total_won if total_won > 0 else 0
                st.markdown(f"""
                    <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                        <div class='metric-label'>Avg Deal Size</div>
                        <div class='metric-value'>₹{avg_deal_size:,.1f}L</div>
                        <div style='color: #666; font-size: 0.9em;'>Per won deal</div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Add practice-wise summary table
            st.markdown("### Practice-wise Details")
            summary_data = practice_metrics.copy()
            summary_data['Win Rate'] = (summary_data['Closed Deals'] / (summary_data['Closed Deals'] + summary_data['Pipeline Deals']) * 100).round(1)
            summary_data['Pipeline Value'] = summary_data['Total Pipeline'] - summary_data['Closed Amount']
            
            # Format the summary table
            summary_data['Closed Amount'] = summary_data['Closed Amount'].apply(lambda x: f"₹{x:,.1f}L")
            summary_data['Total Pipeline'] = summary_data['Total Pipeline'].apply(lambda x: f"₹{x:,.1f}L")
            summary_data['Pipeline Value'] = summary_data['Pipeline Value'].apply(lambda x: f"₹{x:,.1f}L")
            summary_data['Win Rate'] = summary_data['Win Rate'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(
                summary_data[['Practice', 'Closed Amount', 'Pipeline Value', 'Total Pipeline', 'Closed Deals', 'Pipeline Deals', 'Win Rate']],
                use_container_width=True
            )
        else:
            st.error("Practice column not found in the dataset")
    
    else:
        st.error("Required data fields (Sales Stage, Amount) not found in the dataset")

def show_detailed():
    if st.session_state.df is None:
        st.warning("Please upload your sales data to view detailed information")
        return
    
    st.title("Detailed Sales Data")
    
    df = st.session_state.df
    
    # Search and filters
    search = st.text_input("Search", placeholder="Search in any field...")
    
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
            options=["Data Input", "Overview", "Detailed Data"],
            key="navigation"
        )
        
        st.session_state.current_view = selected.lower().replace(" ", "_")
    
    # Display the selected view
    if st.session_state.current_view == "data_input":
        show_data_input()
    elif st.session_state.current_view == "overview":
        show_overview()
    elif st.session_state.current_view == "detailed_data":
        show_detailed()

if __name__ == "__main__":
    main() 
