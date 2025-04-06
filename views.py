import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def show_login_page():
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

def show_data_input_view(df):
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
                    excel_file = pd.ExcelFile(uploaded_file)
                    sheet_name = st.selectbox("Select Worksheet", excel_file.sheet_names)
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                else:
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

def show_overview_view(df):
    if df is None:
        st.warning("Please upload your sales data to view the dashboard")
        return
    
    st.title("Sales Performance Overview")
    df = df.copy()

    # Sales Target Input
    st.markdown("### Enter Your Sales Target (Optional)")
    default_target = str(int(st.session_state.get("sales_target", 0)))
    user_target_input = st.text_input("Sales Target (in Lakhs)", value=default_target)
    
    try:
        user_target = int(user_target_input)
    except ValueError:
        user_target = 0
    
    st.session_state.sales_target = float(user_target)

    # Calculate total "Closed Won"
    won_deals = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
    won_amount_lacs = won_deals['Amount'].sum() / 100000

    # Show "Target vs Closed Won" progress
    if st.session_state.sales_target > 0:
        achievement_pct = (won_amount_lacs / st.session_state.sales_target) * 100
    else:
        achievement_pct = 0

    st.markdown(
        f"""
        <div style='margin-top: 30px; padding: 20px; background: #f0f2f6; border-radius: 12px;'>
            <h3 style='margin: 0; color: #2ecc71; font-size: 1.2em; font-weight: 500;'>Closed Won</h3>
            <h2 style='margin: 5px 0; color: #2ecc71; font-size: 2.8em; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>
                ₹{won_amount_lacs:,.2f}L
            </h2>
            <div style='text-align: right; margin-bottom: 10px;'>
                <span style='color: #e74c3c; font-size: 1em; font-weight: 500;'>Target: ₹{st.session_state.sales_target:,.0f}L</span>
            </div>
            <div style='background: #e74c3c; height: 40px; border-radius: 20px; overflow: hidden; position: relative; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);'>
                <div style='background: #2ecc71; height: 100%; width: {min(achievement_pct, 100)}%; transition: width 0.5s ease-in-out;'></div>
                <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: 600; font-size: 1.2em; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);'>
                    {int(achievement_pct)}% Complete
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Practice Section
    st.markdown("""
        <div style='background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Practice</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'Practice' in df.columns:
        practices = ['All'] + sorted(df['Practice'].dropna().unique().tolist())
        selected_practice = st.selectbox(
            "Select Practice",
            options=practices,
            key="practice_filter"
        )
        
        df_practice = df.copy()
        if selected_practice != 'All':
            df_practice = df_practice[df_practice['Practice'] == selected_practice]
        
        # Calculate practice metrics
        practice_metrics = df_practice.groupby('Practice').agg({
            'Amount': lambda x: x[df_practice['Sales Stage'].str.contains('Won', case=False, na=False)].sum() / 100000,
            'Sales Stage': lambda x: x[df_practice['Sales Stage'].str.contains('Won', case=False, na=False)].count()
        }).reset_index()
        
        practice_metrics.columns = ['Practice', 'Closed Amount', 'Closed Deals']
        
        # Pipeline by practice
        pipeline_df = df_practice[~df_practice['Sales Stage'].str.contains('Won', case=False, na=False)]
        total_pipeline = pipeline_df.groupby('Practice')['Amount'].sum() / 100000
        practice_metrics['Total Pipeline'] = practice_metrics['Practice'].map(total_pipeline)
        
        # Pipeline deal counts
        total_deals = pipeline_df.groupby('Practice').size()
        practice_metrics['Pipeline Deals'] = practice_metrics['Practice'].map(total_deals)
        
        # Sort by pipeline
        practice_metrics = practice_metrics.sort_values('Total Pipeline', ascending=False)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pipeline = go.Figure()
            fig_pipeline.add_trace(go.Bar(
                x=practice_metrics['Practice'],
                y=practice_metrics['Total Pipeline'],
                name='Pipeline',
                text=practice_metrics['Total Pipeline'].apply(lambda x: f"₹{int(x)}L"),
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
                text=practice_metrics['Closed Amount'].apply(lambda x: f"₹{int(x)}L"),
                textposition='outside',
                textfont=dict(size=16, color='#2ecc71', family='Segoe UI', weight='bold'),
                marker_color='#2ecc71',
                marker_line=dict(color='#27ae60', width=2),
                opacity=0.9
            ))
            fig_pipeline.update_layout(
                title=dict(
                    text="Practice-wise Pipeline vs Closed Won",
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
                    text="Practice-wise Pipeline vs Closed Deals",
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
        
        # Practice summary
        st.markdown("### Practice Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pipeline_val = practice_metrics['Total Pipeline'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Pipeline</div>
                    <div class='metric-value'>₹{int(total_pipeline_val)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Active pipeline value</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_deals_count = practice_metrics['Pipeline Deals'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Pipeline Deals</div>
                    <div class='metric-value'>{int(total_deals_count)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Active opportunities</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_won = practice_metrics['Closed Deals'].sum()
            win_rate = (total_won / (total_won + total_deals_count) * 100) if (total_won + total_deals_count) > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Win Rate</div>
                    <div class='metric-value'>{int(win_rate)}%</div>
                    <div style='color: #666; font-size: 0.9em;'>{int(total_won)} won</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_deal_size = practice_metrics['Closed Amount'].sum() / total_won if total_won > 0 else 0
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Avg Deal Size</div>
                    <div class='metric-value'>₹{int(avg_deal_size)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per won deal</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Practice-wise table
        st.markdown("### Practice-wise Details")
        summary_data = practice_metrics.copy()
        summary_data['Win Rate'] = (summary_data['Closed Deals'] / (summary_data['Closed Deals'] + summary_data['Pipeline Deals']) * 100).round(1)
        summary_data['Closed Amount'] = summary_data['Closed Amount'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Total Pipeline'] = summary_data['Total Pipeline'].apply(lambda x: f"₹{int(x)}L")
        summary_data['Win Rate'] = summary_data['Win Rate'].apply(lambda x: f"{int(x)}%")
        
        st.dataframe(
            summary_data[['Practice', 'Closed Amount', 'Total Pipeline', 'Closed Deals', 'Pipeline Deals', 'Win Rate']],
            use_container_width=True
        )
    else:
        st.error("Practice column not found in the dataset")

    # Monthly Pipeline Trend
    st.markdown("""
        <div style='background: linear-gradient(90deg, #00b4db 0%, #0083b0 100%); padding: 15px; border-radius: 10px; margin-bottom: 30px;'>
            <h3 style='color: white; margin: 0; text-align: center; font-size: 1.8em; font-weight: 600;'>Monthly Pipeline Trend</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if 'Expected Close Date' in df.columns and 'Amount' in df.columns and 'Sales Stage' in df.columns:
        df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
        
        deal_type = st.selectbox(
            "Select Deal Type",
            ["🌊 Pipeline", "🟢 Closed Won", "📦 All Deals"],
            index=0
        )
        
        if deal_type == "🌊 Pipeline":
            filtered_df = df[~df['Sales Stage'].str.contains('Won', case=False, na=False)]
            color = '#00b4db'
        elif deal_type == "🟢 Closed Won":
            filtered_df = df[df['Sales Stage'].str.contains('Won', case=False, na=False)]
            color = '#2ecc71'
        else:
            filtered_df = df
            color = '#9b59b6'
        
        monthly_data = filtered_df.groupby(filtered_df['Expected Close Date'].dt.to_period('M')).agg({
            'Amount': 'sum',
            'Sales Stage': 'count'
        }).reset_index()
        
        monthly_data['Expected Close Date'] = monthly_data['Expected Close Date'].astype(str)
        monthly_data['Amount'] = monthly_data['Amount'] / 100000
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_data['Expected Close Date'],
            y=monthly_data['Amount'],
            mode='lines+markers',
            name=deal_type,
            line=dict(width=3, color=color),
            marker=dict(size=8, color=color),
            text=monthly_data['Amount'].apply(lambda x: f"₹{int(x)}L"),
            textposition='top center',
            textfont=dict(size=12, family='Segoe UI', weight='bold')
        ))
        
        fig_trend.update_layout(
            title=dict(
                text=f"{deal_type} Trend",
                font=dict(size=22, family='Segoe UI', color='#2c3e50', weight='bold'),
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top'
            ),
            height=500,
            showlegend=False,
            xaxis_title=dict(
                text="Month",
                font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                standoff=15
            ),
            yaxis_title=dict(
                text="Amount (Lakhs)",
                font=dict(size=16, family='Segoe UI', color='#2c3e50', weight='bold'),
                standoff=15
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
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_value = monthly_data['Amount'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Value</div>
                    <div class='metric-value'>₹{int(total_value)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Overall</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            avg_monthly = monthly_data['Amount'].mean()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Monthly Average</div>
                    <div class='metric-value'>₹{int(avg_monthly)}L</div>
                    <div style='color: #666; font-size: 0.9em;'>Per month</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            total_deals = monthly_data['Sales Stage'].sum()
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <div class='metric-label'>Total Deals</div>
                    <div class='metric-value'>{int(total_deals)}</div>
                    <div style='color: #666; font-size: 0.9em;'>Number of deals</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Required columns (Expected Close Date, Amount, Sales Stage) not found in the dataset")

def show_sales_team_view(df):
    if df is None:
        st.warning("Please upload your sales data to view team information")
        return
    
    # Process data once with caching
    df = process_data(df)
    
    # Team members
    team_members = sorted(df['Sales Owner'].dropna().unique().tolist())
    
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        '>
            <h2 style='
                color: white;
                margin: 0;
                text-align: center;
                font-size: 2em;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            '>Sales Team Data</h2>
        </div>
    """, unsafe_allow_html=True)

    metrics = calculate_team_metrics(df)
    
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    metric_style = """
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, {gradient});
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 10px 5px;
    """
    metric_text_style = """
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.6em;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        margin: 15px 0;
        letter-spacing: 0.5px;
        -webkit-font-smoothing: antialiased;
    """
    label_style = """
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.5em;
        font-weight: 800;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        -webkit-font-smoothing: antialiased;
    """
    sublabel_style = """
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.2em;
        font-weight: 700;
        margin-top: 8px;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        -webkit-font-smoothing: antialiased;
    """
    
    total_pipeline = metrics['Current Pipeline'].sum()
    total_closed = metrics['Closed Won'].sum()
    total_closed_deals = metrics['Closed Deals'].sum()
    total_pipeline_deals = metrics['Pipeline Deals'].sum()
    
    with col1:
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#2193b0 0%, #6dd5ed 100%")}'>
                <div style='{label_style}'>Pipeline Value</div>
                <div style='{metric_text_style}'>₹{int(total_pipeline)}L</div>
                <div style='{sublabel_style}'>Active opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#11998e 0%, #38ef7d 100%")}'>
                <div style='{label_style}'>Closed Won</div>
                <div style='{metric_text_style}'>₹{int(total_closed)}L</div>
                <div style='{sublabel_style}'>Won opportunities</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        win_rate = round((total_closed_deals / (total_closed_deals + total_pipeline_deals) * 100), 1) if (total_closed_deals + total_pipeline_deals) > 0 else 0
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#4e54c8 0%, #8f94fb 100%")}'>
                <div style='{label_style}'>Win Rate</div>
                <div style='{metric_text_style}'>{int(win_rate)}%</div>
                <div style='{sublabel_style}'>{int(total_closed_deals)} won</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_deal_size = round(total_closed / total_closed_deals, 1) if total_closed_deals > 0 else 0
        st.markdown(f"""
            <div style='{metric_style.format(gradient="#f12711 0%, #f5af19 100%")}'>
                <div style='{label_style}'>Avg Deal Size</div>
                <div style='{metric_text_style}'>₹{int(avg_deal_size)}L</div>
                <div style='{sublabel_style}'>Per won deal</div>
            </div>
        """, unsafe_allow_html=True)

    # Filters
    st.markdown("""
        <div style='padding: 15px; background: linear-gradient(to right, #f8f9fa, #e9ecef); border-radius: 10px; margin: 15px 0;'>
            <h4 style='color: #2a5298; margin: 0; font-size: 1.1em; font-weight: 600;'>🔍 Filters</h4>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col1:
        filters = {
            'selected_member': st.selectbox(
                "👤 Sales Owner",
                options=["All Team Members"] + team_members,
                key="team_member_filter"
            )
        }
    with col2:
        filters['search'] = st.text_input("🔍 Search", placeholder="Search...")
    with col3:
        fiscal_order = ['April', 'May', 'June', 'July', 'August', 'September', 
                       'October', 'November', 'December', 'January', 'February', 'March']
        available_months = df['Month'].dropna().unique().tolist()
        available_months.sort(key=lambda x: fiscal_order.index(x) if x in fiscal_order else len(fiscal_order))
        filters['month_filter'] = st.selectbox("📅 Month", options=["All Months"] + available_months)
    with col4:
        filters['quarter_filter'] = st.selectbox("📊 Quarter", options=["All Quarters", "Q1", "Q2", "Q3", "Q4"])
    with col5:
        filters['year_filter'] = st.selectbox("📅 Year", options=["All Years"] + sorted(df['Expected Close Date'].dt.year.unique().tolist()))
    with col6:
        probability_options = ["All Probability", "0-25%", "26-50%", "51-75%", "76-100%", "Custom Range"]
        filters['probability_filter'] = st.selectbox("📈 Probability", options=probability_options)
        if filters.get('probability_filter') == "Custom Range":
            col6a, col6b = st.columns(2)
            with col6a:
                min_prob_input = st.text_input("Min %", value="0", key="custom_min_prob_input")
            with col6b:
                max_prob_input = st.text_input("Max %", value="100", key="custom_max_prob_input")
            try:
                min_prob = int(min_prob_input)
            except ValueError:
                min_prob = 0
            try:
                max_prob = int(max_prob_input)
            except ValueError:
                max_prob = 100
            filters['min_prob'] = min_prob
            filters['max_prob'] = max_prob
            filters['custom_prob_range'] = f"{min_prob}-{max_prob}%"
    with col7:
        status_options = ["All Status", "Committed for the Month", "Upsides for the Month"]
        filters['status_filter'] = st.selectbox("🎯 Status", options=status_options)
    with col8:
        filters['focus_filter'] = st.selectbox("🎯 Focus", options=["All Focus"] + sorted(df['KritiKal Focus Areas'].dropna().unique().tolist()))
    with col9:
        practices = ["All Practices"] + sorted(df['Practice'].dropna().unique().tolist())
        filters['practice_filter'] = st.selectbox("🏢 Practice", options=practices)

    filtered_df = filter_dataframe(df, filters)
    
    # Performance Metrics
    st.markdown("""
        <div style='margin-bottom: 20px;'>
            <h3 style='color: #2a5298; margin: 0; font-size: 1.4em; font-weight: 600;'>Performance Metrics</h3>
        </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    current_pipeline = filtered_df[~filtered_df['Is_Won']]['Amount_Lacs'].sum()
    weighted_projections = filtered_df[~filtered_df['Is_Won']]['Weighted_Amount'].sum()
    closed_won = filtered_df[filtered_df['Is_Won']]['Amount_Lacs'].sum()

    with m1:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
                height: 100%;
            '>
                <div style='color: white; font-size: 1.1em; font-weight: 600; margin-bottom: 8px;'>
                    🌊 Current Pipeline
                </div>
                <div style='color: white; font-size: 1.8em; font-weight: 800;'>
                    ₹{int(current_pipeline)}L
                </div>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #6B5B95 0%, #846EA9 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            '>
                <div style='color: white; font-size: 1.1em; font-weight: 600; margin-bottom: 8px;'>
                    ⚖️ Weighted Projections
                </div>
                <div style='color: white; font-size: 1.8em; font-weight: 800;'>
                    ₹{int(weighted_projections)}L
                </div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            '>
                <div style='color: white; font-size: 1.1em; font-weight: 600; margin-bottom: 8px;'>
                    💰 Closed Won
                </div>
                <div style='color: white; font-size: 1.8em; font-weight: 800;'>
                    ₹{int(closed_won)}L
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Team Member Performance Table
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)
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
            '>Team Member Performance</h3>
        </div>
    """, unsafe_allow_html=True)
    
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.index = filtered_df.index + 1
    
    display_df = filtered_df[['Organization Name', 'Opportunity Name', 'Geography', 
                            'Expected Close Date', 'Probability', 'Amount', 
                            'Sales Owner', 'Pre-sales Technical Lead', 'Business Owner', 
                            'Type', 'KritiKal Focus Areas', 'Practice']].copy()
    
    display_df = display_df.rename(columns={
        'Amount': 'Amount (In Lacs)',
        'Pre-sales Technical Lead': 'Tech Owner',
        'Type': 'Hunting /farming'
    })
    
    display_df['Amount (In Lacs)'] = display_df['Amount (In Lacs)'].apply(lambda x: int(x/100000) if pd.notnull(x) else 0)
    display_df['Probability'] = display_df['Probability'].apply(format_percentage)
    display_df['Weighted Revenue (In Lacs)'] = display_df.apply(
        lambda row: int((row['Amount (In Lacs)']) * float(str(row['Probability']).rstrip('%'))/100) if pd.notnull(row['Amount (In Lacs)']) else 0, 
        axis=1
    )
    
    display_df['Expected Close Date'] = pd.to_datetime(display_df['Expected Close Date']).dt.strftime('%d-%b-%Y')
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
            'Expected Close Date': st.column_config.TextColumn(
                'Expected Close Date',
                help="Expected closing date"
            ),
            'Practice': st.column_config.TextColumn(
                'Practice',
                help="Practice area"
            )
        }
    )

def show_detailed_data_view(df):
    if df is None:
        st.warning("Please upload your sales data to view detailed information")
        return
    
    st.title("Detailed Sales Data")
    search = st.text_input("Search", placeholder="Search in any field...")
    
    if search:
        mask = np.column_stack([df[col].astype(str).str.contains(search, case=False, na=False) 
                                for col in df.columns])
        df = df[mask.any(axis=1)]
    
    st.dataframe(df, use_container_width=True)

def process_data(df):
    """Process and prepare data for the dashboard"""
    df = df.copy()
    
    # Convert dates and calculate time-based columns at once
    df['Expected Close Date'] = pd.to_datetime(df['Expected Close Date'], errors='coerce')
    df['Month'] = df['Expected Close Date'].dt.strftime('%B')
    df['Year'] = df['Expected Close Date'].dt.year
    df['Quarter'] = df['Expected Close Date'].dt.quarter.map({1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
    
    # Convert probability and calculate numeric values at once with safe null handling
    def convert_probability(x):
        try:
            if pd.isna(x):
                return 0
            if isinstance(x, str):
                x = x.rstrip('%')
            return float(x)
        except:
            return 0
    
    df['Probability_Num'] = df['Probability'].apply(convert_probability)
    
    # Pre-calculate common flags and metrics with safe null handling
    df['Is_Won'] = df['Sales Stage'].str.contains('Won', case=False, na=False)
    df['Amount_Lacs'] = df['Amount'].fillna(0).div(100000).round(0).astype(int)
    df['Weighted_Amount'] = (df['Amount_Lacs'] * df['Probability_Num'] / 100).round(0).astype(int)
    
    return df

def format_percentage(value):
    """Format probability as percentage"""
    if pd.isna(value):
        return "0%"
    try:
        return f"{int(float(str(value).rstrip('%')))}%"
    except:
        return "0%"

def filter_dataframe(df, filters):
    """Apply filters to dataframe efficiently"""
    mask = pd.Series(True, index=df.index)
    
    if filters.get('selected_member') != "All Team Members":
        mask &= df['Sales Owner'] == filters['selected_member']
    
    if filters.get('search'):
        search_mask = pd.Series(False, index=df.index)
        search = filters['search'].lower()
        for col in ['Organization Name', 'Opportunity Name', 'Sales Owner', 'Sales Stage']:
            search_mask |= df[col].astype(str).str.lower().str.contains(search, na=False)
        mask &= search_mask
    
    if filters.get('month_filter') != "All Months":
        mask &= df['Month'] == filters['month_filter']
    
    if filters.get('quarter_filter') != "All Quarters":
        mask &= df['Quarter'] == filters['quarter_filter']
    
    if filters.get('year_filter') != "All Years":
        mask &= df['Year'] == filters['year_filter']
    
    if filters.get('probability_filter') != "All Probability":
        if filters['probability_filter'] == "Custom Range":
            prob_range = filters['custom_prob_range'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
        else:
            prob_range = filters['probability_filter'].split("-")
            min_prob = float(prob_range[0])
            max_prob = float(prob_range[1].rstrip("%"))
        mask &= (df['Probability_Num'] >= min_prob) & (df['Probability_Num'] <= max_prob)
    
    if filters.get('status_filter') != "All Status":
        if filters['status_filter'] == "Committed for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask &= (df['Month'] == current_month) & (df['Probability_Num'] > 75)
        elif filters['status_filter'] == "Upsides for the Month":
            current_month = pd.Timestamp.now().strftime('%B')
            mask &= (df['Month'] == current_month) & (df['Probability_Num'].between(25, 75))
        else:
            mask &= df['Sales Stage'] == filters['status_filter']
    
    if filters.get('focus_filter') != "All Focus":
        mask &= df['KritiKal Focus Areas'] == filters['focus_filter']
    
    # Add practice filter
    if filters.get('practice_filter') != "All Practices":
        mask &= df['Practice'] == filters['practice_filter']
    
    return df[mask]

def calculate_team_metrics(df):
    """Calculate all team-related metrics at once"""
    team_metrics = df.groupby('Sales Owner').agg({
        'Amount': lambda x: int(x[df['Is_Won'] & x.notna()].sum() / 100000) if len(x[df['Is_Won'] & x.notna()]) > 0 else 0,
        'Is_Won': 'sum',
        'Amount_Lacs': lambda x: int(x[~df['Is_Won'] & x.notna()].sum()) if len(x[~df['Is_Won'] & x.notna()]) > 0 else 0,
        'Weighted_Amount': lambda x: int(x[~df['Is_Won'] & x.notna()].sum()) if len(x[~df['Is_Won'] & x.notna()]) > 0 else 0
    }).reset_index()
    
    team_metrics.columns = ['Sales Owner', 'Closed Won', 'Closed Deals', 'Current Pipeline', 'Weighted Projections']
    
    team_metrics = team_metrics.fillna(0)
    
    # Calculate Pipeline Deals
    pipeline_deals = df[~df['Is_Won']].groupby('Sales Owner').size()
    team_metrics['Pipeline Deals'] = team_metrics['Sales Owner'].map(pipeline_deals).fillna(0).astype(int)
    
    # Win Rate
    total_deals = team_metrics['Closed Deals'] + team_metrics['Pipeline Deals']
    team_metrics['Win Rate'] = np.where(
        total_deals > 0,
        (team_metrics['Closed Deals'] / total_deals * 100).round(0),
        0
    ).astype(int)
    
    return team_metrics 
