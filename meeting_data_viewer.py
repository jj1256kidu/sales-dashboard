import streamlit as st
import pandas as pd
import os
from datetime import datetime
import glob

# Set page config
st.set_page_config(
    page_title="Meeting Data Viewer",
    page_icon="📊",
    layout="wide"
)

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            color: #2a5298;
            font-size: 2.5em;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .section-header {
            color: #2a5298;
            font-size: 1.8em;
            font-weight: 500;
            margin: 20px 0 10px 0;
        }
        .info-text {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📊 Meeting Data Viewer</h1>', unsafe_allow_html=True)

# File upload section
st.markdown('<h2 class="section-header">📤 Upload New Meeting Data</h2>', unsafe_allow_html=True)
st.markdown('<p class="info-text">Upload an Excel file to add it to the data repository.</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an Excel file",
    type=['xlsx'],
    help="Upload your meeting data in Excel format"
)

if uploaded_file is not None:
    try:
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"meeting_{current_date}.xlsx"
        filepath = os.path.join("data", filename)
        
        # Save the file
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File saved successfully as {filename}")
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")

# File selection section
st.markdown('<h2 class="section-header">📂 Select Meeting Data</h2>', unsafe_allow_html=True)
st.markdown('<p class="info-text">Choose a file from the data repository to view its contents.</p>', unsafe_allow_html=True)

# Get list of files in data directory
files = glob.glob(os.path.join("data", "meeting_*.xlsx"))
files.sort(key=os.path.getmtime, reverse=True)  # Sort by most recent

if not files:
    st.warning("No meeting data files found in the data directory.")
else:
    # Create dropdown with filenames
    selected_file = st.selectbox(
        "Select a file",
        options=files,
        format_func=lambda x: os.path.basename(x)
    )

    if selected_file:
        try:
            # Read the Excel file
            df = pd.read_excel(
                selected_file,
                sheet_name="Quarter Summary Dashboard",
                skiprows=2,
                usecols="B:T"
            )
            
            # Display the data
            st.markdown('<h2 class="section-header">📋 Meeting Data</h2>', unsafe_allow_html=True)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
        except ValueError as e:
            if "Worksheet named" in str(e):
                st.error("The selected file does not contain a sheet named 'Quarter Summary Dashboard'.")
            else:
                st.error(f"Error reading file: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        Meeting Data Viewer | Last updated: {date}
    </div>
""".format(date=datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True) 
