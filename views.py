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
    if 'df' not in st.session_state:
        st.warning("Please upload data first")
        return
    
    df = st.session_state.df
    
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
    if 'df' not in st.session_state:
        st.warning("Please upload data first")
        return
    
    df = st.session_state.df
    
    # Initialize session state for filters if not exists
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'team_members': [],
            'practices': [],
            'months': [],
            'quarters': [],
            'years': [],
            'probabilities': [],
            'statuses': [],
            'focus': [],
            'search': '',
            'date_range': None
        }
    
    # Initialize filter presets if not exists
    if 'filter_presets' not in st.session_state:
        st.session_state.filter_presets = {
            'Current Quarter': {
                'quarters': [f"Q{(pd.Timestamp.now().month-1)//3 + 1}"],
                'years': [str(pd.Timestamp.now().year)]
            },
            'Last Quarter': {
                'quarters': [f"Q{((pd.Timestamp.now().month-1)//3 - 1) % 4 + 1}"],
                'years': [str(pd.Timestamp.now().year - (1 if pd.Timestamp.now().month <= 3 else 0))]
            },
            'Current Month': {
                'months': [pd.Timestamp.now().strftime("%B")],
                'years': [str(pd.Timestamp.now().year)]
            }
        }
    
    # Export and Presets Section
    st.markdown("### 🛠️ Tools")
    tool_cols = st.columns(3)
    
    with tool_cols[0]:
        # Filter Presets
        preset = st.selectbox(
            "📋 Apply Filter Preset",
            options=["Custom"] + list(st.session_state.filter_presets.keys())
        )
        if preset != "Custom":
            st.session_state.filters.update(st.session_state.filter_presets[preset])
            st.experimental_rerun()
    
    with tool_cols[1]:
        # Save Current Filter as Preset
        new_preset_name = st.text_input("💾 Save Current Filter as Preset", placeholder="Preset name...")
        if new_preset_name and st.button("Save"):
            st.session_state.filter_presets[new_preset_name] = st.session_state.filters.copy()
            st.success(f"Preset '{new_preset_name}' saved!")
    
    with tool_cols[2]:
        # Export Options
        export_format = st.selectbox(
            "📤 Export Data",
            options=["None", "CSV", "Excel"]
        )
        if export_format != "None":
            if st.button("Export"):
                filtered_df = apply_filters(df, st.session_state.filters)
                if export_format == "CSV":
                    csv = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="sales_data.csv",
                        mime="text/csv"
                    )
                elif export_format == "Excel":
                    excel = filtered_df.to_excel(index=False)
                    st.download_button(
                        label="Download Excel",
                        data=excel,
                        file_name="sales_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    # Reset filters button
    if st.button("🔄 Reset All Filters", key="reset_filters"):
        st.session_state.filters = {
            'team_members': [],
            'practices': [],
            'months': [],
            'quarters': [],
            'years': [],
            'probabilities': [],
            'statuses': [],
            'focus': [],
            'search': '',
            'date_range': None
        }
        st.experimental_rerun()
    
    # First row of filters
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    
    with col1:
        # Sales Owner (Team Member) filter - Multi-select
        team_members = sorted(df['Sales Team Member'].unique())
        selected_team = st.multiselect(
            "👤 Sales Owner",
            options=team_members,
            default=st.session_state.filters['team_members'],
            key="team_filter"
        )
        st.session_state.filters['team_members'] = selected_team
    
    with col2:
        # Search
        search_term = st.text_input(
            "🔍 Search",
            value=st.session_state.filters['search'],
            placeholder="Search...",
            key="search_filter"
        )
        st.session_state.filters['search'] = search_term
    
    with col3:
        # Practice filter - Multi-select
        if 'Practice' in df.columns:
            practices = sorted(df['Practice'].dropna().unique())
            selected_practice = st.multiselect(
                "🏢 Practice",
                options=practices,
                default=st.session_state.filters['practices'],
                key="practice_filter"
            )
            st.session_state.filters['practices'] = selected_practice
        else:
            st.error("Practice column not found in the data")
    
    with col4:
        # Month filter - Multi-select
        months = ["April", "May", "June", "July", "August", "September",
                 "October", "November", "December", "January", "February", "March"]
        selected_month = st.multiselect(
            "📅 Month",
            options=months,
            default=st.session_state.filters['months'],
            key="month_filter"
        )
        st.session_state.filters['months'] = selected_month
    
    with col5:
        # Quarter filter - Multi-select
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        selected_quarter = st.multiselect(
            "📊 Quarter",
            options=quarters,
            default=st.session_state.filters['quarters'],
            key="quarter_filter"
        )
        st.session_state.filters['quarters'] = selected_quarter
    
    with col6:
        # Year filter - Multi-select
        years = sorted(df['Date'].dt.year.unique())
        selected_year = st.multiselect(
            "📆 Year",
            options=[str(year) for year in years],
            default=st.session_state.filters['years'],
            key="year_filter"
        )
        st.session_state.filters['years'] = selected_year
    
    with col7:
        # Probability filter - Multi-select
        probabilities = ["High", "Medium", "Low"]
        selected_probability = st.multiselect(
            "📈 Probability",
            options=probabilities,
            default=st.session_state.filters['probabilities'],
            key="probability_filter"
        )
        st.session_state.filters['probabilities'] = selected_probability
    
    with col8:
        # Status filter - Multi-select
        statuses = sorted(df['Status'].unique())
        selected_status = st.multiselect(
            "🎯 Status",
            options=statuses,
            default=st.session_state.filters['statuses'],
            key="status_filter"
        )
        st.session_state.filters['statuses'] = selected_status
    
    with col9:
        # Focus filter - Multi-select
        focus_options = ["New Business", "Existing Business"]
        selected_focus = st.multiselect(
            "🎯 Focus",
            options=focus_options,
            default=st.session_state.filters['focus'],
            key="focus_filter"
        )
        st.session_state.filters['focus'] = selected_focus
    
    # Date range picker
    st.markdown("### Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=df['Date'].min(),
            key="start_date"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=df['Date'].max(),
            key="end_date"
        )
    st.session_state.filters['date_range'] = (start_date, end_date)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply Sales Owner filter
    if st.session_state.filters['team_members']:
        filtered_df = filtered_df[filtered_df['Sales Team Member'].isin(st.session_state.filters['team_members'])]
    
    # Apply Practice filter
    if st.session_state.filters['practices']:
        filtered_df = filtered_df[filtered_df['Practice'].isin(st.session_state.filters['practices'])]
    
    # Apply Month filter
    if st.session_state.filters['months']:
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        month_numbers = [month_map[month] for month in st.session_state.filters['months']]
        filtered_df = filtered_df[filtered_df['Date'].dt.month.isin(month_numbers)]
    
    # Apply Quarter filter
    if st.session_state.filters['quarters']:
        quarter_map = {"Q1": [1, 2, 3], "Q2": [4, 5, 6], 
                      "Q3": [7, 8, 9], "Q4": [10, 11, 12]}
        quarter_months = []
        for quarter in st.session_state.filters['quarters']:
            quarter_months.extend(quarter_map[quarter])
        filtered_df = filtered_df[filtered_df['Date'].dt.month.isin(quarter_months)]
    
    # Apply Year filter
    if st.session_state.filters['years']:
        filtered_df = filtered_df[filtered_df['Date'].dt.year.astype(str).isin(st.session_state.filters['years'])]
    
    # Apply Probability filter
    if st.session_state.filters['probabilities']:
        filtered_df = filtered_df[filtered_df['Probability'].isin(st.session_state.filters['probabilities'])]
    
    # Apply Status filter
    if st.session_state.filters['statuses']:
        filtered_df = filtered_df[filtered_df['Status'].isin(st.session_state.filters['statuses'])]
    
    # Apply Focus filter
    if st.session_state.filters['focus']:
        filtered_df = filtered_df[filtered_df['Focus'].isin(st.session_state.filters['focus'])]
    
    # Apply Date Range filter
    if st.session_state.filters['date_range']:
        start_date, end_date = st.session_state.filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]
    
    # Apply Search filter
    if st.session_state.filters['search']:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(st.session_state.filters['search'], case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    if len(filtered_df) > 0:
        # Calculate common metrics once
        total_pipeline = filtered_df['Deal Value'].sum()
        total_deals = len(filtered_df)
        closed_won = len(filtered_df[filtered_df['Status'] == 'Closed Won'])
        win_rate = (closed_won / total_deals * 100) if total_deals > 0 else 0
        avg_deal_size = total_pipeline / total_deals if total_deals > 0 else 0
        
        # Calculate weighted pipeline
        probability_weights = {"High": 0.8, "Medium": 0.5, "Low": 0.2}
        filtered_df['Weighted Value'] = filtered_df.apply(
            lambda row: row['Deal Value'] * probability_weights.get(row['Probability'], 0.3),
            axis=1
        )
        weighted_pipeline = filtered_df['Weighted Value'].sum()
        
        # Calculate deal velocity
        closed_deals = filtered_df[filtered_df['Status'] == 'Closed Won']
        if not closed_deals.empty:
            closed_deals['Days to Close'] = (closed_deals['Close Date'] - closed_deals['Date']).dt.days
            avg_days_to_close = closed_deals['Days to Close'].mean()
        else:
            avg_days_to_close = 0
        
        # Calculate month-over-month growth
        current_month = filtered_df['Date'].max().to_period('M')
        prev_month = current_month - 1
        current_month_data = filtered_df[filtered_df['Date'].dt.to_period('M') == current_month]
        prev_month_data = filtered_df[filtered_df['Date'].dt.to_period('M') == prev_month]
        
        current_month_pipeline = current_month_data['Deal Value'].sum()
        prev_month_pipeline = prev_month_data['Deal Value'].sum()
        mom_growth = ((current_month_pipeline - prev_month_pipeline) / prev_month_pipeline * 100) if prev_month_pipeline > 0 else 0
        
        # Display summary metrics with enhanced styling
        st.markdown("### 📊 Summary Metrics")
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div style='font-size: 0.9em; color: #666;'>Total Pipeline</div>
                    <div style='font-size: 1.5em; font-weight: bold;'>${total_pipeline:,.2f}</div>
                    <div style='font-size: 0.8em; color: #666;'>Weighted: ${weighted_pipeline:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div style='font-size: 0.9em; color: #666;'>Win Rate</div>
                    <div style='font-size: 1.5em; font-weight: bold;'>{win_rate:.1f}%</div>
                    <div style='font-size: 0.8em; color: #666;'>{closed_won} won / {total_deals} total</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div style='font-size: 0.9em; color: #666;'>Avg Deal Size</div>
                    <div style='font-size: 1.5em; font-weight: bold;'>${avg_deal_size:,.2f}</div>
                    <div style='font-size: 0.8em; color: #666;'>Days to Close: {int(avg_days_to_close)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[3]:
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div style='font-size: 0.9em; color: #666;'>MoM Growth</div>
                    <div style='font-size: 1.5em; font-weight: bold; color: {'#2ecc71' if mom_growth >= 0 else '#e74c3c'}'>
                        {mom_growth:+.1f}%
                    </div>
                    <div style='font-size: 0.8em; color: #666;'>vs Previous Month</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Trend Analysis Section
        st.markdown("### 📈 Trend Analysis")
        trend_cols = st.columns(2)
        
        with trend_cols[0]:
            # Monthly trend
            monthly_trend = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Deal Value'].sum().reset_index()
            monthly_trend['Date'] = monthly_trend['Date'].astype(str)
            
            fig_trend = px.line(
                monthly_trend,
                x='Date',
                y='Deal Value',
                title='Monthly Pipeline Trend',
                markers=True,
                template='plotly_white'
            )
            fig_trend.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )
            fig_trend.update_layout(
                hovermode='x unified',
                showlegend=False,
                xaxis_title='Month',
                yaxis_title='Pipeline Value ($)'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with trend_cols[1]:
            # Deal size distribution
            fig_dist = px.histogram(
                filtered_df,
                x='Deal Value',
                nbins=20,
                title='Deal Size Distribution',
                template='plotly_white'
            )
            fig_dist.update_layout(
                hovermode='x unified',
                showlegend=False,
                xaxis_title='Deal Value ($)',
                yaxis_title='Number of Deals'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Team Performance Section
        st.markdown("### 👥 Team Performance")
        
        # Calculate team metrics with enhanced calculations
        team_metrics = filtered_df.groupby('Sales Team Member').agg({
            'Deal Value': ['sum', 'count', 'mean'],
            'Status': lambda x: (x == 'Closed Won').sum(),
            'Weighted Value': 'sum'
        }).reset_index()
        
        team_metrics.columns = ['Sales Team Member', 'Total Pipeline', 'Total Deals', 
                              'Avg Deal Size', 'Closed Won', 'Weighted Pipeline']
        
        # Calculate additional metrics
        team_metrics['Win Rate'] = (team_metrics['Closed Won'] / team_metrics['Total Deals'] * 100).round(1)
        team_metrics['Pipeline Share'] = (team_metrics['Total Pipeline'] / total_pipeline * 100).round(1)
        
        # Sort by weighted pipeline
        team_metrics = team_metrics.sort_values('Weighted Pipeline', ascending=False)
        
        # Display team metrics with enhanced styling
        st.dataframe(
            team_metrics.style.format({
                'Total Pipeline': '${:,.2f}',
                'Weighted Pipeline': '${:,.2f}',
                'Avg Deal Size': '${:,.2f}',
                'Win Rate': '{:.1f}%',
                'Pipeline Share': '{:.1f}%'
            }).background_gradient(subset=['Win Rate', 'Pipeline Share'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # Team performance visualization
        fig_team = px.bar(
            team_metrics,
            x='Sales Team Member',
            y=['Total Pipeline', 'Weighted Pipeline'],
            title='Pipeline vs Weighted Pipeline by Team Member',
            barmode='group',
            template='plotly_white'
        )
        fig_team.update_layout(
            hovermode='x unified',
            xaxis_title='Team Member',
            yaxis_title='Pipeline Value ($)'
        )
        st.plotly_chart(fig_team, use_container_width=True)
        
        # Practice Analysis Section
        if len(filtered_df['Practice'].unique()) > 0:
            st.markdown("### 🏢 Practice Analysis")
            
            # Calculate practice metrics with enhanced calculations
            practice_metrics = filtered_df.groupby('Practice').agg({
                'Deal Value': ['sum', 'count', 'mean'],
                'Status': lambda x: (x == 'Closed Won').sum(),
                'Weighted Value': 'sum'
            }).reset_index()
            
            practice_metrics.columns = ['Practice', 'Total Pipeline', 'Total Deals', 
                                      'Avg Deal Size', 'Closed Won', 'Weighted Pipeline']
            
            # Calculate additional metrics
            practice_metrics['Win Rate'] = (practice_metrics['Closed Won'] / practice_metrics['Total Deals'] * 100).round(1)
            practice_metrics['Pipeline Share'] = (practice_metrics['Total Pipeline'] / total_pipeline * 100).round(1)
            
            # Sort by weighted pipeline
            practice_metrics = practice_metrics.sort_values('Weighted Pipeline', ascending=False)
            
            # Display practice metrics and visualizations in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Practice Metrics")
                st.dataframe(
                    practice_metrics.style.format({
                        'Total Pipeline': '${:,.2f}',
                        'Weighted Pipeline': '${:,.2f}',
                        'Avg Deal Size': '${:,.2f}',
                        'Win Rate': '{:.1f}%',
                        'Pipeline Share': '{:.1f}%'
                    }).background_gradient(subset=['Win Rate', 'Pipeline Share'], cmap='RdYlGn'),
                    use_container_width=True
                )
            
            with col2:
                st.markdown("#### Practice Performance")
                fig_practice = px.bar(
                    practice_metrics,
                    x='Practice',
                    y=['Total Pipeline', 'Weighted Pipeline'],
                    title='Pipeline vs Weighted Pipeline by Practice',
                    barmode='group',
                    template='plotly_white'
                )
                fig_practice.update_layout(
                    hovermode='x unified',
                    xaxis_title='Practice',
                    yaxis_title='Pipeline Value ($)'
                )
                st.plotly_chart(fig_practice, use_container_width=True)
            
            # Practice distribution by team member
            st.markdown("#### Practice Distribution by Team")
            practice_dist = filtered_df.groupby(['Sales Team Member', 'Practice'])['Deal Value'].sum().reset_index()
            fig_dist = px.bar(
                practice_dist,
                x='Sales Team Member',
                y='Deal Value',
                color='Practice',
                title='Practice Distribution by Team Member',
                template='plotly_white'
            )
            fig_dist.update_layout(
                hovermode='x unified',
                xaxis_title='Team Member',
                yaxis_title='Pipeline Value ($)'
            )
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Practice heatmap
            st.markdown("#### Practice Performance Heatmap")
            practice_heatmap = filtered_df.pivot_table(
                index='Sales Team Member',
                columns='Practice',
                values='Deal Value',
                aggfunc='sum',
                fill_value=0
            )
            fig_heatmap = px.imshow(
                practice_heatmap,
                title='Practice Distribution Heatmap',
                template='plotly_white',
                color_continuous_scale='RdYlGn'
            )
            fig_heatmap.update_layout(
                xaxis_title='Practice',
                yaxis_title='Team Member'
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("No data available for the selected filters")

def show_detailed_data_view(st):
    """Display the detailed data view with search and filtering options"""
    if 'df' not in st.session_state:
        st.warning("Please upload data first")
        return
    
    df = st.session_state.df.copy()
    
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

def apply_filters(df, filters):
    """Apply all filters to the dataframe"""
    filtered_df = df.copy()
    
    # Apply Sales Owner filter
    if filters['team_members']:
        filtered_df = filtered_df[filtered_df['Sales Team Member'].isin(filters['team_members'])]
    
    # Apply Practice filter
    if filters['practices']:
        filtered_df = filtered_df[filtered_df['Practice'].isin(filters['practices'])]
    
    # Apply Month filter
    if filters['months']:
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        month_numbers = [month_map[month] for month in filters['months']]
        filtered_df = filtered_df[filtered_df['Date'].dt.month.isin(month_numbers)]
    
    # Apply Quarter filter
    if filters['quarters']:
        quarter_map = {"Q1": [1, 2, 3], "Q2": [4, 5, 6], 
                      "Q3": [7, 8, 9], "Q4": [10, 11, 12]}
        quarter_months = []
        for quarter in filters['quarters']:
            quarter_months.extend(quarter_map[quarter])
        filtered_df = filtered_df[filtered_df['Date'].dt.month.isin(quarter_months)]
    
    # Apply Year filter
    if filters['years']:
        filtered_df = filtered_df[filtered_df['Date'].dt.year.astype(str).isin(filters['years'])]
    
    # Apply Probability filter
    if filters['probabilities']:
        filtered_df = filtered_df[filtered_df['Probability'].isin(filters['probabilities'])]
    
    # Apply Status filter
    if filters['statuses']:
        filtered_df = filtered_df[filtered_df['Status'].isin(filters['statuses'])]
    
    # Apply Focus filter
    if filters['focus']:
        filtered_df = filtered_df[filtered_df['Focus'].isin(filters['focus'])]
    
    # Apply Date Range filter
    if filters['date_range']:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]
    
    # Apply Search filter
    if filters['search']:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(filters['search'], case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    return filtered_df

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
