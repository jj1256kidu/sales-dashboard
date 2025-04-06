import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Quarterly Summary Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .custom-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .custom-header h1 {
        color: white;
        margin: 0;
        text-align: center;
        font-size: 2.2em;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .custom-header p {
        color: white;
        margin: 10px 0 0 0;
        text-align: center;
        font-size: 1.2em;
        opacity: 0.9;
    }
    .dataframe-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

def load_excel_data(file_path):
    """Load and process Excel data from both sheets"""
    try:
        # Read both sheets
        current_df = pd.read_excel(file_path, sheet_name="Raw_Data")
        previous_df = pd.read_excel(file_path, sheet_name="Previous Data")
        
        # Select required columns
        required_columns = ['Sales Owner', 'Committed', 'Upside', 'Closed Won', 'Function']
        
        # Process current week data
        current_df = current_df[required_columns].copy()
        current_df['Week'] = 'Current'
        
        # Process previous week data
        previous_df = previous_df[required_columns].copy()
        previous_df['Week'] = 'Previous'
        
        return current_df, previous_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def calculate_summaries(current_df, previous_df):
    """Calculate summaries for both Sales Owner and Function groups"""
    # Combine current and previous data
    combined_df = pd.concat([current_df, previous_df])
    
    # Group by Sales Owner
    sales_df = combined_df.groupby(['Sales Owner', 'Week']).agg({
        'Committed': 'sum',
        'Upside': 'sum',
        'Closed Won': 'sum'
    }).reset_index()
    
    # Group by Function
    function_df = combined_df.groupby(['Function', 'Week']).agg({
        'Committed': 'sum',
        'Upside': 'sum',
        'Closed Won': 'sum'
    }).reset_index()
    
    return sales_df, function_df

def create_comparison_df(df, group_column):
    """Create a comparison dataframe with current, previous, and delta values"""
    # Pivot the data
    pivot_df = df.pivot(index=group_column, columns='Week', values=['Committed', 'Upside', 'Closed Won'])
    
    # Calculate deltas
    for metric in ['Committed', 'Upside', 'Closed Won']:
        pivot_df[(metric, 'Delta')] = pivot_df[(metric, 'Current')] - pivot_df[(metric, 'Previous')]
    
    # Calculate total (Committed + Closed Won)
    pivot_df[('Total', 'Current')] = pivot_df[('Committed', 'Current')] + pivot_df[('Closed Won', 'Current')]
    pivot_df[('Total', 'Previous')] = pivot_df[('Committed', 'Previous')] + pivot_df[('Closed Won', 'Previous')]
    pivot_df[('Total', 'Delta')] = pivot_df[('Total', 'Current')] - pivot_df[('Total', 'Previous')]
    
    return pivot_df

def style_dataframe(df):
    """Style the dataframe with color highlights for deltas"""
    def color_delta(val):
        if isinstance(val, (int, float)):
            if val < 0:
                return 'color: red'
            elif val > 0:
                return 'color: green'
        return ''
    
    styled_df = df.style.applymap(color_delta, subset=pd.IndexSlice[:, [('Committed', 'Delta'), 
                                                                       ('Upside', 'Delta'),
                                                                       ('Closed Won', 'Delta'),
                                                                       ('Total', 'Delta')]])
    
    # Format numbers
    for col in df.columns:
        if col[1] != 'Delta':
            styled_df = styled_df.format({col: '{:,.0f}'})
        else:
            styled_df = styled_df.format({col: '{:+,.0f}'})
    
    return styled_df

def main():
    # Create header
    st.markdown("""
        <div class="custom-header">
            <h1>📊 Quarterly Summary Dashboard</h1>
            <p>Track and compare sales performance across weeks</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create sidebar for file selection
    st.sidebar.title("Data Source")
    data_source = st.sidebar.radio("Select data source:", ["File Upload", "Data Folder"])
    
    if data_source == "File Upload":
        uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=['xlsx'])
        if uploaded_file:
            current_df, previous_df = load_excel_data(uploaded_file)
    else:
        data_folder = Path("data")
        if not data_folder.exists():
            data_folder.mkdir()
        
        files = list(data_folder.glob("*.xlsx"))
        if files:
            selected_file = st.sidebar.selectbox("Select file:", files)
            if selected_file:
                current_df, previous_df = load_excel_data(selected_file)
        else:
            st.warning("No Excel files found in the data folder.")
            return
    
    if 'current_df' in locals() and current_df is not None:
        # Calculate summaries
        sales_df, function_df = calculate_summaries(current_df, previous_df)
        
        # Create comparison dataframes
        sales_comparison = create_comparison_df(sales_df, 'Sales Owner')
        function_comparison = create_comparison_df(function_df, 'Function')
        
        # Display Sales Owner Summary
        st.markdown('<h2 style="color: #2a5298;">👤 Sales Owner Summary</h2>', unsafe_allow_html=True)
        st.dataframe(style_dataframe(sales_comparison), use_container_width=True)
        
        # Display Function Overview
        st.markdown('<h2 style="color: #2a5298;">🏢 Function Overview</h2>', unsafe_allow_html=True)
        st.dataframe(style_dataframe(function_comparison), use_container_width=True)

if __name__ == "__main__":
    main() 
