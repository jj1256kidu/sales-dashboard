import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def show_data_input_view(df):
    st.header("Data Input")
    
    # Data Input Section
    st.subheader("Add New Sales Data")
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("Date", datetime.now())
        practice = st.selectbox("Practice", ["Consulting", "Implementation", "Support"])
        stage = st.selectbox("Stage", ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"])
        amount = st.number_input("Amount", min_value=0.0, value=0.0)
    
    with col2:
        team_member = st.selectbox("Team Member", ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams"])
        client = st.text_input("Client Name")
        description = st.text_area("Description")
    
    if st.button("Add Entry"):
        new_row = pd.DataFrame({
            'Date': [date],
            'Practice': [practice],
            'Stage': [stage],
            'Amount': [amount],
            'Team Member': [team_member],
            'Client': [client],
            'Description': [description]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        st.session_state.df = df
        st.success("Entry added successfully!")
        st.experimental_rerun()

def show_overview_view(df):
    st.header("Overview")
    
    # Date Range Filter
    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.selectbox(
            "Date Range",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 12 Months", "All Time"],
            key="date_filter"
        )
    
    with col2:
        selected_practice = st.selectbox(
            "Practice",
            ["All"] + list(df['Practice'].unique()),
            key="selected_practice"
        )
    
    with col3:
        selected_stage = st.selectbox(
            "Stage",
            ["All"] + list(df['Stage'].unique()),
            key="selected_stage"
        )
    
    # Filter data based on selections
    filtered_df = filter_dataframe(df, date_filter, selected_practice, selected_stage)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Amount'].sum()
        st.metric("Total Sales", f"${total_sales:,.2f}")
    
    with col2:
        avg_deal_size = filtered_df['Amount'].mean()
        st.metric("Average Deal Size", f"${avg_deal_size:,.2f}")
    
    with col3:
        total_deals = len(filtered_df)
        st.metric("Total Deals", f"{total_deals:,}")
    
    with col4:
        win_rate = len(filtered_df[filtered_df['Stage'] == 'Closed Won']) / len(filtered_df) * 100
        st.metric("Win Rate", f"{win_rate:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Practice
        practice_sales = filtered_df.groupby('Practice')['Amount'].sum().reset_index()
        fig_practice = px.pie(
            practice_sales,
            values='Amount',
            names='Practice',
            title='Sales Distribution by Practice'
        )
        st.plotly_chart(fig_practice, use_container_width=True)
    
    with col2:
        # Sales by Stage
        stage_sales = filtered_df.groupby('Stage')['Amount'].sum().reset_index()
        fig_stage = px.bar(
            stage_sales,
            x='Stage',
            y='Amount',
            title='Sales by Stage'
        )
        st.plotly_chart(fig_stage, use_container_width=True)
    
    # Sales Trend
    daily_sales = filtered_df.groupby('Date')['Amount'].sum().reset_index()
    fig_trend = px.line(
        daily_sales,
        x='Date',
        y='Amount',
        title='Daily Sales Trend'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

def show_sales_team_view(df):
    st.header("Sales Team")
    
    # Team Member Selection
    selected_team_member = st.selectbox(
        "Select Team Member",
        ["All"] + list(df['Team Member'].unique()),
        key="selected_team_member"
    )
    
    # Sales Target Input
    sales_target = st.number_input(
        "Set Sales Target",
        min_value=0.0,
        value=100000.0,
        key="sales_target"
    )
    
    # Filter data based on selection
    if selected_team_member != "All":
        df = df[df['Team Member'] == selected_team_member]
    
    # Team Metrics
    metrics = calculate_team_metrics(df, sales_target)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"${metrics['total_sales']:,.2f}")
    
    with col2:
        st.metric("Target Achievement", f"{metrics['target_achievement']:.1f}%")
    
    with col3:
        st.metric("Number of Deals", f"{metrics['num_deals']:,}")
    
    with col4:
        st.metric("Average Deal Size", f"${metrics['avg_deal_size']:,.2f}")
    
    # Performance Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Team Member
        team_sales = df.groupby('Team Member')['Amount'].sum().reset_index()
        fig_team = px.bar(
            team_sales,
            x='Team Member',
            y='Amount',
            title='Sales by Team Member'
        )
        st.plotly_chart(fig_team, use_container_width=True)
    
    with col2:
        # Win Rate by Team Member
        team_wins = df.groupby('Team Member').apply(
            lambda x: len(x[x['Stage'] == 'Closed Won']) / len(x) * 100
        ).reset_index()
        team_wins.columns = ['Team Member', 'Win Rate']
        
        fig_wins = px.bar(
            team_wins,
            x='Team Member',
            y='Win Rate',
            title='Win Rate by Team Member'
        )
        st.plotly_chart(fig_wins, use_container_width=True)

def show_detailed_data_view(df):
    st.header("Detailed Data")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_filter = st.selectbox(
            "Date Range",
            ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 12 Months"],
            key="date_filter_detailed"
        )
    
    with col2:
        practice_filter = st.selectbox(
            "Practice",
            ["All"] + list(df['Practice'].unique()),
            key="practice_filter_detailed"
        )
    
    with col3:
        stage_filter = st.selectbox(
            "Stage",
            ["All"] + list(df['Stage'].unique()),
            key="stage_filter_detailed"
        )
    
    # Filter data
    filtered_df = filter_dataframe(df, date_filter, practice_filter, stage_filter)
    
    # Display filtered dataframe
    st.dataframe(filtered_df, use_container_width=True)
    
    # Export button
    if st.button("Export to CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="sales_data.csv",
            mime="text/csv"
        )

def filter_dataframe(df, date_filter, practice, stage):
    """Filter dataframe based on selected criteria"""
    filtered_df = df.copy()
    
    # Apply date filter
    if date_filter != "All Time":
        today = datetime.now().date()
        if date_filter == "Last 7 Days":
            filtered_df = filtered_df[filtered_df['Date'] >= today - timedelta(days=7)]
        elif date_filter == "Last 30 Days":
            filtered_df = filtered_df[filtered_df['Date'] >= today - timedelta(days=30)]
        elif date_filter == "Last 90 Days":
            filtered_df = filtered_df[filtered_df['Date'] >= today - timedelta(days=90)]
        elif date_filter == "Last 12 Months":
            filtered_df = filtered_df[filtered_df['Date'] >= today - timedelta(days=365)]
    
    # Apply practice filter
    if practice != "All":
        filtered_df = filtered_df[filtered_df['Practice'] == practice]
    
    # Apply stage filter
    if stage != "All":
        filtered_df = filtered_df[filtered_df['Stage'] == stage]
    
    return filtered_df

def calculate_team_metrics(df, target):
    """Calculate team performance metrics"""
    total_sales = df['Amount'].sum()
    num_deals = len(df)
    avg_deal_size = df['Amount'].mean() if num_deals > 0 else 0
    target_achievement = (total_sales / target * 100) if target > 0 else 0
    
    return {
        'total_sales': total_sales,
        'num_deals': num_deals,
        'avg_deal_size': avg_deal_size,
        'target_achievement': target_achievement
    } 
