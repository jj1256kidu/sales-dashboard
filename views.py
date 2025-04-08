import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def show_login_page(st):
    """Display the login page with neon-styled authentication and tsparticles"""
    # Custom CSS and JS for login page with particles
    st.markdown("""
        <style>
            /* Reset and base styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            /* Particle container */
            #tsparticles {
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: 0;
                background: #0a0a2e;
            }

            /* Main container */
            .container {
                position: relative;
                z-index: 1;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            /* Login box */
            .login-box {
                background: rgba(0, 0, 0, 0.8);
                border-radius: 20px;
                padding: 40px;
                width: 100%;
                max-width: 400px;
                border: 1px solid rgba(0, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
            }

            /* Form header */
            .login-header {
                text-align: center;
                margin-bottom: 30px;
            }

            .login-header h1 {
                color: #0ff;
                font-size: 2.5em;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
                margin-bottom: 10px;
            }

            /* Form inputs */
            .form-group {
                margin-bottom: 20px;
            }

            .stTextInput > div > div > input {
                width: 100% !important;
                padding: 15px !important;
                border-radius: 30px !important;
                background: rgba(0, 0, 0, 0.5) !important;
                border: 2px solid #0ff !important;
                color: #0ff !important;
                font-size: 1.1em !important;
                transition: all 0.3s ease !important;
            }

            .stTextInput > div > div > input:focus {
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.4) !important;
                border-color: #0ff !important;
            }

            .stTextInput > div > div > input::placeholder {
                color: rgba(0, 255, 255, 0.5) !important;
            }

            /* Login button */
            .stButton > button {
                width: 100% !important;
                padding: 15px !important;
                border-radius: 30px !important;
                background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
                background-size: 200% 200% !important;
                border: none !important;
                color: white !important;
                font-size: 1.2em !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                animation: buttonGlow 3s infinite !important;
            }

            .stButton > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 0 20px rgba(255, 0, 255, 0.4) !important;
            }

            /* Additional options */
            .login-options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 20px;
                color: #0ff;
                font-size: 0.9em;
            }

            .remember-me {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .remember-me input[type="checkbox"] {
                accent-color: #0ff;
            }

            .forgot-password {
                color: #0ff;
                text-decoration: none;
                transition: all 0.3s ease;
            }

            .forgot-password:hover {
                text-shadow: 0 0 10px #0ff;
            }

            /* Error message */
            .error-message {
                color: #ff0055;
                text-align: center;
                margin-top: 15px;
                font-size: 0.9em;
                text-shadow: 0 0 10px rgba(255, 0, 85, 0.5);
            }

            /* Animations */
            @keyframes buttonGlow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
        </style>

        <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"></script>
        <script>
            window.onload = function() {
                tsParticles.load("tsparticles", {
                    fullScreen: {
                        enable: true
                    },
                    particles: {
                        number: {
                            value: 80,
                            density: {
                                enable: true,
                                value_area: 800
                            }
                        },
                        color: {
                            value: ["#00ffff", "#ff00ff", "#00ff00"]
                        },
                        shape: {
                            type: "circle"
                        },
                        opacity: {
                            value: 0.5,
                            random: true,
                            animation: {
                                enable: true,
                                speed: 1,
                                minimumValue: 0.1,
                                sync: false
                            }
                        },
                        size: {
                            value: 3,
                            random: true,
                            animation: {
                                enable: true,
                                speed: 2,
                                minimumValue: 0.1,
                                sync: false
                            }
                        },
                        links: {
                            enable: true,
                            distance: 150,
                            color: "#00ffff",
                            opacity: 0.4,
                            width: 1
                        },
                        move: {
                            enable: true,
                            speed: 2,
                            direction: "none",
                            random: false,
                            straight: false,
                            outModes: {
                                default: "out"
                            },
                            attract: {
                                enable: false,
                                rotateX: 600,
                                rotateY: 1200
                            }
                        }
                    },
                    interactivity: {
                        detectsOn: "window",
                        events: {
                            onHover: {
                                enable: true,
                                mode: "repulse"
                            },
                            onClick: {
                                enable: true,
                                mode: "push"
                            },
                            resize: true
                        },
                        modes: {
                            repulse: {
                                distance: 100,
                                duration: 0.4
                            },
                            push: {
                                quantity: 4
                            }
                        }
                    },
                    background: {
                        color: "#0a0a2e"
                    }
                });
            }
        </script>

        <div id="tsparticles"></div>
    """, unsafe_allow_html=True)

    # Login container
    st.markdown("""
        <div class="container">
            <div class="login-box">
                <div class="login-header">
                    <h1>Welcome Back</h1>
                </div>
                <div class="form-group">
    """, unsafe_allow_html=True)

    # Login form
    username = st.text_input("", placeholder="Username", key="username")
    password = st.text_input("", type="password", placeholder="Password", key="password")
    
    if st.button("LOGIN"):
        if password == "admin123":  # Default password
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.markdown('<div class="error-message">Invalid credentials. Please try again.</div>', unsafe_allow_html=True)

    # Remember me and forgot password
    st.markdown("""
                </div>
                <div class="login-options">
                    <div class="remember-me">
                        <input type="checkbox" id="remember" name="remember">
                        <label for="remember">Remember me</label>
                    </div>
                    <a href="#" class="forgot-password">Forgot password?</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_data_input_view(st):
    """Display the data input view with file upload and preview"""
    st.title("Data Input")
    
    # File upload section
    st.markdown("""
        <style>
            .upload-container {
                background: rgba(0, 0, 0, 0.8);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                border: 1px solid rgba(0, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }
            
            .upload-header {
                color: #0ff;
                font-size: 1.5em;
                margin-bottom: 20px;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
            }
            
            .file-format-info {
                background: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                border: 1px solid rgba(0, 255, 255, 0.2);
            }
            
            .required-fields {
                margin-top: 20px;
                color: #0ff;
            }
        </style>
        
        <div class="upload-container">
            <div class="upload-header">Upload Sales Data</div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.session_state.df = df
            st.success("File uploaded successfully!")
            
            # Display data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Display data summary
            st.subheader("Data Summary")
            st.write(f"Total Records: {len(df)}")
            st.write(f"Columns: {', '.join(df.columns)}")
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    st.markdown("""
            <div class="file-format-info">
                <h4>Supported File Formats:</h4>
                <ul>
                    <li>Excel (.xlsx)</li>
                    <li>CSV (.csv)</li>
                </ul>
            </div>
            
            <div class="required-fields">
                <h4>Required Fields:</h4>
                <ul>
                    <li>Date</li>
                    <li>Sales Team Member</li>
                    <li>Practice</li>
                    <li>Deal Value</li>
                    <li>Status</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_overview_view(st):
    """Display the overview view with key metrics and visualizations"""
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload data first.")
        return

    dataset_choice = st.radio(
        "Select Dataset",
        ["Current Week", "Previous Week"],
        horizontal=True
    )

    df = st.session_state.df_current if dataset_choice == "Current Week" else st.session_state.df_previous
    
    # Calculate metrics
    total_closed_won = df[df['Status'] == 'Closed Won']['Deal Value'].sum()
    total_pipeline = df['Deal Value'].sum()
    win_rate = (total_closed_won / total_pipeline) * 100 if total_pipeline > 0 else 0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Closed Won", f"${total_closed_won:,.2f}")
    with col2:
        st.metric("Total Pipeline", f"${total_pipeline:,.2f}")
    with col3:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    
    # Practice-wise pipeline
    st.subheader("Practice-wise Pipeline")
    practice_pipeline = df.groupby('Practice')['Deal Value'].sum().reset_index()
    fig1 = px.bar(practice_pipeline, x='Practice', y='Deal Value',
                  color='Practice', title='Pipeline by Practice')
    st.plotly_chart(fig1)
    
    # Practice-wise closed deals
    st.subheader("Practice-wise Closed Deals")
    closed_deals = df[df['Status'] == 'Closed Won'].groupby('Practice')['Deal Value'].sum().reset_index()
    fig2 = px.pie(closed_deals, values='Deal Value', names='Practice',
                  title='Closed Deals by Practice')
    st.plotly_chart(fig2)
    
    # Monthly trend
    st.subheader("Monthly Sales Trend")
    df['Date'] = pd.to_datetime(df['Date'])
    monthly_trend = df.groupby(df['Date'].dt.to_period('M'))['Deal Value'].sum().reset_index()
    monthly_trend['Date'] = monthly_trend['Date'].astype(str)
    fig3 = px.line(monthly_trend, x='Date', y='Deal Value',
                   title='Monthly Sales Trend')
    st.plotly_chart(fig3)

def show_sales_team_view(st):
    """Display the sales team view with team performance metrics"""
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload data first.")
        return

    dataset_choice = st.radio(
        "Select Dataset",
        ["Current Week", "Previous Week"],
        horizontal=True
    )

    df = st.session_state.df_current if dataset_choice == "Current Week" else st.session_state.df_previous
    
    # First row of filters with adjusted column sizes
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1.2, 1.2, 1.2, 1, 1, 1, 1, 1.2, 1.2])
    
    with col1:
        # Sales Owner (Team Member) filter
        team_members = sorted(df['Sales Team Member'].unique())
        selected_team = st.selectbox("👤 Sales Owner", ["All Team Members"] + list(team_members))
    
    with col2:
        # Search
        search_term = st.text_input("🔍 Search", placeholder="Search...")
    
    with col3:
        try:
            # Practice filter
            if 'Practice' in df.columns:
                practices = sorted(df['Practice'].dropna().unique())
                selected_practice = st.selectbox("🏢 Practice", ["All Practices"] + list(practices))
            else:
                st.error("Practice column not found in the data")
                selected_practice = "All Practices"
        except Exception as e:
            st.error(f"Error loading practice filter: {str(e)}")
            selected_practice = "All Practices"
    
    with col4:
        # Month filter
        months = ["All Months", "April", "May", "June", "July", "August", "September",
                 "October", "November", "December", "January", "February", "March"]
        selected_month = st.selectbox("📅 Month", months)
    
    with col5:
        # Quarter filter
        quarters = ["All Quarters", "Q1", "Q2", "Q3", "Q4"]
        selected_quarter = st.selectbox("📊 Quarter", quarters)
    
    with col6:
        # Year filter
        years = sorted(df['Date'].dt.year.unique())
        selected_year = st.selectbox("📆 Year", ["All Years"] + [str(year) for year in years])
    
    with col7:
        # Probability filter
        probabilities = ["All Probability", "High", "Medium", "Low"]
        selected_probability = st.selectbox("📈 Probability", probabilities)
    
    with col8:
        # Status filter
        statuses = sorted(df['Status'].unique())
        selected_status = st.selectbox("🎯 Status", ["All Status"] + list(statuses))
    
    with col9:
        # Focus filter
        focus_options = ["All Focus", "New Business", "Existing Business"]
        selected_focus = st.selectbox("🎯 Focus", focus_options)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply Sales Owner filter
    if selected_team != "All Team Members":
        filtered_df = filtered_df[filtered_df['Sales Team Member'] == selected_team]
    
    # Apply Practice filter
    if selected_practice != "All Practices":
        filtered_df = filtered_df[filtered_df['Practice'] == selected_practice]
    
    # Apply Month filter
    if selected_month != "All Months":
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        filtered_df = filtered_df[filtered_df['Date'].dt.month == month_map[selected_month]]
    
    # Apply Quarter filter
    if selected_quarter != "All Quarters":
        quarter_map = {"Q1": [1, 2, 3], "Q2": [4, 5, 6], 
                      "Q3": [7, 8, 9], "Q4": [10, 11, 12]}
        if selected_quarter in quarter_map:
            filtered_df = filtered_df[filtered_df['Date'].dt.month.isin(quarter_map[selected_quarter])]
    
    # Apply Year filter
    if selected_year != "All Years":
        filtered_df = filtered_df[filtered_df['Date'].dt.year == int(selected_year)]
    
    # Apply Probability filter
    if selected_probability != "All Probability":
        filtered_df = filtered_df[filtered_df['Probability'] == selected_probability]
    
    # Apply Status filter
    if selected_status != "All Status":
        filtered_df = filtered_df[filtered_df['Status'] == selected_status]
    
    # Apply Focus filter
    if selected_focus != "All Focus":
        filtered_df = filtered_df[filtered_df['Focus'] == selected_focus]
    
    # Apply Search filter
    if search_term:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    if len(filtered_df) > 0:
        # Display team metrics in a single view
        st.subheader("Team Performance Metrics")
        
        # Calculate team metrics
        team_metrics = filtered_df.groupby('Sales Team Member').agg({
            'Deal Value': ['sum', 'count'],
            'Status': lambda x: (x == 'Closed Won').sum()
        }).reset_index()
        
        team_metrics.columns = ['Sales Team Member', 'Total Pipeline', 'Total Deals', 'Closed Won']
        team_metrics['Win Rate'] = (team_metrics['Closed Won'] / team_metrics['Total Deals'] * 100).round(1)
        team_metrics['Average Deal Size'] = (team_metrics['Total Pipeline'] / team_metrics['Total Deals']).round(2)
        
        # Display metrics table
        st.dataframe(team_metrics.style.format({
            'Total Pipeline': '${:,.2f}',
            'Average Deal Size': '${:,.2f}',
            'Win Rate': '{:.1f}%'
        }))
        
        # Team performance visualization
        st.subheader("Team Performance Visualization")
        fig = px.bar(team_metrics, x='Sales Team Member', y=['Total Pipeline', 'Closed Won'],
                     title='Pipeline vs Closed Won by Team Member', barmode='group')
        st.plotly_chart(fig)
        
        # Detailed Opportunities
        st.subheader("Detailed Opportunities")
        display_df = filtered_df[['Organization Name', 'Opportunity Name', 'Geography', 
                                'Date', 'Probability', 'Deal Value', 
                                'Sales Team Member', 'Technical Lead', 'Business Owner', 
                                'Type', 'Focus']].copy()
        
        display_df = display_df.rename(columns={
            'Deal Value': 'Amount (In Lacs)',
            'Technical Lead': 'Tech Owner',
            'Type': 'Hunting /farming'
        })
        
        display_df['Amount (In Lacs)'] = display_df['Amount (In Lacs)'].apply(lambda x: int(x/100000) if pd.notnull(x) else 0)
        display_df['Probability'] = display_df['Probability'].apply(lambda x: f"{x}%")
        display_df['Weighted Revenue (In Lacs)'] = display_df.apply(
            lambda row: int((row['Amount (In Lacs)']) * float(str(row['Probability']).rstrip('%'))/100) if pd.notnull(row['Amount (In Lacs)']) else 0, 
            axis=1
        )
        
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%d-%b-%Y')
        display_df = display_df.sort_values('Amount (In Lacs)', ascending=False)
        
        display_df.index = range(1, len(display_df) + 1)
        display_df.index.name = 'S.No'
        
        st.dataframe(
            display_df,
            column_config={
                'Amount (In Lacs)': st.column_config.NumberColumn(
                    'Amount (In Lacs)',
                    format="₹%d L",
                    help="Amount in Lakhs"
                ),
                'Weighted Revenue (In Lacs)': st.column_config.NumberColumn(
                    'Weighted Revenue (In Lacs)',
                    format="₹%d L",
                    help="Weighted Revenue in Lakhs"
                ),
                'Probability': st.column_config.TextColumn(
                    'Probability',
                    help="Probability of winning the deal"
                ),
                'Date': st.column_config.TextColumn(
                    'Date',
                    help="Expected closing date"
                )
            }
        )
        
        # Practice distribution
        if len(filtered_df['Practice'].unique()) > 0:
            st.subheader("Practice Distribution")
            practice_dist = filtered_df.groupby(['Sales Team Member', 'Practice'])['Deal Value'].sum().reset_index()
            fig2 = px.bar(practice_dist, x='Sales Team Member', y='Deal Value',
                         color='Practice', title='Practice Distribution by Team Member')
            st.plotly_chart(fig2)
        
        # Practice metrics
        st.subheader("Practice Performance")
        practice_metrics = filtered_df.groupby('Practice').agg({
            'Deal Value': ['sum', 'count'],
            'Status': lambda x: (x == 'Closed Won').sum()
        }).reset_index()
        
        practice_metrics.columns = ['Practice', 'Total Pipeline', 'Total Deals', 'Closed Won']
        practice_metrics['Win Rate'] = (practice_metrics['Closed Won'] / practice_metrics['Total Deals'] * 100).round(1)
        practice_metrics['Average Deal Size'] = (practice_metrics['Total Pipeline'] / practice_metrics['Total Deals']).round(2)
        
        # Display practice metrics in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(practice_metrics.style.format({
                'Total Pipeline': '${:,.2f}',
                'Average Deal Size': '${:,.2f}',
                'Win Rate': '{:.1f}%'
            }))
        
        with col2:
            fig3 = px.bar(practice_metrics, x='Practice', y='Win Rate',
                         title='Win Rate by Practice', color='Practice')
            st.plotly_chart(fig3)
        
        # Practice trend
        st.subheader("Practice Pipeline Trend")
        practice_trend = filtered_df.groupby(['Practice', filtered_df['Date'].dt.to_period('M')])['Deal Value'].sum().reset_index()
        practice_trend['Date'] = practice_trend['Date'].astype(str)
        fig4 = px.line(practice_trend, x='Date', y='Deal Value',
                       color='Practice', title='Practice-wise Pipeline Trend')
        st.plotly_chart(fig4)
    else:
        st.warning("No data available for the selected filters")

def show_detailed_data_view(st):
    """Display the detailed data view with search and filtering options"""
    if 'df_current' not in st.session_state or 'df_previous' not in st.session_state:
        st.warning("Please upload data first.")
        return

    dataset_choice = st.radio(
        "Select Dataset",
        ["Current Week", "Previous Week"],
        horizontal=True
    )

    df = st.session_state.df_current if dataset_choice == "Current Week" else st.session_state.df_previous
    
    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Search and filters
    st.sidebar.header("Search & Filters")
    
    # Text search
    search_term = st.sidebar.text_input("🔍 Search in all columns")
    
    # Practice filter
    practices = sorted(df['Practice'].unique())
    selected_practices = st.sidebar.multiselect("🏢 Select Practices", practices)
    
    # Financial Year and Month filter
    st.sidebar.subheader("📅 Financial Year & Month")
    
    # Get unique years from the data
    years = sorted(df['Date'].dt.year.unique())
    
    # Create financial year options (e.g., 2023-24)
    financial_years = [f"{year}-{str(year+1)[-2:]}" for year in years]
    selected_fy = st.sidebar.selectbox("Select Financial Year", ["All Years"] + financial_years)
    
    # Month filter
    months = [
        "April", "May", "June", "July", "August", "September",
        "October", "November", "December", "January", "February", "March"
    ]
    selected_months = st.sidebar.multiselect("Select Months", months)
    
    # Status filter
    statuses = sorted(df['Status'].unique())
    selected_statuses = st.sidebar.multiselect("🎯 Select Status", statuses)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply search filter
    if search_term:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    # Apply practice filter
    if selected_practices:
        filtered_df = filtered_df[filtered_df['Practice'].isin(selected_practices)]
    
    # Apply financial year filter
    if selected_fy != "All Years":
        start_year = int(selected_fy.split('-')[0])
        # For financial year April-March
        start_date = pd.Timestamp(f"{start_year}-04-01")
        end_date = pd.Timestamp(f"{start_year + 1}-03-31")
        filtered_df = filtered_df[
            (filtered_df['Date'] >= start_date) & 
            (filtered_df['Date'] <= end_date)
        ]
    
    # Apply month filter
    if selected_months:
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        month_numbers = [month_map[month] for month in selected_months]
        filtered_df = filtered_df[filtered_df['Date'].dt.month.isin(month_numbers)]
    
    # Apply status filter
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Status'].isin(selected_statuses)]
    
    # Display filtered data count
    total_records = len(filtered_df)
    st.subheader(f"Detailed Sales Data ({total_records} records)")
    
    if total_records > 0:
        # Display detailed data
        st.dataframe(filtered_df.style.format({
            'Deal Value': '${:,.2f}',
            'Date': lambda x: x.strftime('%Y-%m-%d')
        }))
        
        # Export options
        st.sidebar.header("📤 Export Options")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("Export to Excel"):
                try:
                    filtered_df.to_excel("sales_data_export.xlsx", index=False)
                    st.success("Data exported successfully to Excel!")
                except Exception as e:
                    st.error(f"Error exporting to Excel: {str(e)}")
        
        with col2:
            if st.button("Export to CSV"):
                try:
                    filtered_df.to_csv("sales_data_export.csv", index=False)
                    st.success("Data exported successfully to CSV!")
                except Exception as e:
                    st.error(f"Error exporting to CSV: {str(e)}")
    else:
        st.warning("No data available for the selected filters")

def main():
    """Main function to handle navigation and view selection"""
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'login'
    
    # Navigation
    if not st.session_state.authenticated:
        show_login_page(st)
    else:
        # Sidebar navigation
        st.sidebar.title("Navigation")
        view_options = {
            "Data Input": "data_input",
            "Overview": "overview",
            "Sales Team": "sales_team",
            "Detailed Data": "detailed_data"
        }
        selected_view = st.sidebar.radio("Select View", list(view_options.keys()))
        st.session_state.current_view = view_options[selected_view]
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.current_view = 'login'
            st.rerun()
        
        # Display selected view
        if st.session_state.current_view == 'data_input':
            show_data_input_view(st)
        elif st.session_state.current_view == 'overview':
            show_overview_view(st)
        elif st.session_state.current_view == 'sales_team':
            show_sales_team_view(st)
        elif st.session_state.current_view == 'detailed_data':
            show_detailed_data_view(st)

if __name__ == "__main__":
    main() 
