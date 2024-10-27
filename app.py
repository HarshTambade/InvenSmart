import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Set page layout
st.set_page_config(page_title="InvenSmart Dashboard", layout="wide")

# Utility functions for AI insights
def generate_sales_insights(df):
    insights = []
    
    # Sales trend analysis
    recent_sales = df.sort_values('Last_Restock_Date')
    sales_trend = recent_sales['Sales_Volume'].diff().mean()
    if sales_trend > 0:
        insights.append(f"📈 Sales are trending upward with an average increase of ${abs(sales_trend):.2f} per day")
    else:
        insights.append(f"📉 Sales are trending downward with an average decrease of ${abs(sales_trend):.2f} per day")
    
    # Top performing category
    top_category = df.groupby('Category')['Sales_Volume'].sum().idxmax()
    category_sales = df.groupby('Category')['Sales_Volume'].sum()[top_category]
    insights.append(f"🏆 Best performing category: {top_category} with ${category_sales:,.2f} in sales")
    
    # Stock level warnings
    low_stock = df[df['Stock_Level'] < df['Stock_Level'].mean() * 0.2]
    if not low_stock.empty:
        insights.append(f"⚠️ {len(low_stock)} products have critically low stock levels")
    
    return insights

def generate_recommendations(df):
    recommendations = []
    
    # Inventory optimization
    high_stock_low_sales = df[
        (df['Stock_Level'] > df['Stock_Level'].mean()) & 
        (df['Sales_Volume'] < df['Sales_Volume'].mean())
    ]
    if not high_stock_low_sales.empty:
        recommendations.append(f"🔄 Consider reducing stock for {len(high_stock_low_sales)} slow-moving products")
    
    # Sales opportunities
    high_demand_low_stock = df[
        (df['Stock_Level'] < df['Stock_Level'].mean()) & 
        (df['Sales_Volume'] > df['Sales_Volume'].mean())
    ]
    if not high_demand_low_stock.empty:
        recommendations.append(f"💡 Opportunity to increase stock for {len(high_demand_low_stock)} high-demand products")
    
    return recommendations

def calculate_metrics(df):
    metrics = {}
    metrics['total_sales'] = df['Sales_Volume'].sum()
    metrics['avg_daily_sales'] = df['Sales_Volume'].mean()
    metrics['stock_turnover'] = df['Sales_Volume'].sum() / df['Stock_Level'].sum()
    metrics['low_stock_items'] = len(df[df['Stock_Level'] < df['Stock_Level'].mean() * 0.2])
    return metrics

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data/hyperlocal_inventory_data_updated.csv')
    df['Last_Restock_Date'] = pd.to_datetime(df['Last_Restock_Date'], errors='coerce')
    return df

df = load_data()

# Sidebar
st.sidebar.title("InvenSmart Dashboard")
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Analytics", "AI Insights", "Recommendations"])

# Sidebar Filters
st.sidebar.markdown("### Filters")
date_range = st.sidebar.selectbox("Select Date Range", ["Last 30 Days", "Last 60 Days"], key="date_range")
selected_category = st.sidebar.selectbox("Category Filter", ["All"] + list(df['Category'].unique()))

# Apply date filter
today = pd.Timestamp.now()
if date_range == "Last 30 Days":
    df = df[df['Last_Restock_Date'] >= today - pd.DateOffset(days=30)]
else:
    df = df[df['Last_Restock_Date'] >= today - pd.DateOffset(days=60)]

# Apply category filter
if selected_category != "All":
    df = df[df['Category'] == selected_category]

# Dashboard Page
if page == "Dashboard":
    st.title("Overview Dashboard")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Enhanced KPI Metrics
        st.markdown("### Key Performance Indicators")
        metrics = calculate_metrics(df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="Total Sales",
                value=f"${metrics['total_sales']:,.2f}",
                delta=f"{((metrics['total_sales'] / df['Sales_Volume'].sum()) - 1) * 100:.1f}%"
            )
        with col2:
            st.metric(
                label="Avg Daily Sales",
                value=f"${metrics['avg_daily_sales']:,.2f}"
            )
        with col3:
            st.metric(
                label="Stock Turnover",
                value=f"{metrics['stock_turnover']:.2f}x"
            )
        with col4:
            st.metric(
                label="Low Stock Items",
                value=metrics['low_stock_items'],
                delta=metrics['low_stock_items'] - len(df) * 0.2,
                delta_color="inverse"
            )

        # Sales Visualization Section
        st.markdown("### Sales Analysis")
        
        # Enhanced Visualization Options
        viz_col1, viz_col2 = st.columns([1, 3])
        with viz_col1:
            chart_type = st.radio("Select Chart Type", ["Line Chart", "Bar Chart", "Pie Chart"])
            time_grouping = st.radio("Time Grouping", ["Daily", "Weekly", "Monthly"])
        
        with viz_col2:
            if chart_type == "Line Chart":
                # Time-based sales trend
                if time_grouping == "Daily":
                    sales_data = df.groupby('Last_Restock_Date')['Sales_Volume'].sum().reset_index()
                elif time_grouping == "Weekly":
                    df['Week'] = df['Last_Restock_Date'].dt.isocalendar().week
                    sales_data = df.groupby('Week')['Sales_Volume'].sum().reset_index()
                else:  # Monthly
                    df['Month'] = df['Last_Restock_Date'].dt.strftime('%B %Y')
                    sales_data = df.groupby('Month')['Sales_Volume'].sum().reset_index()
                
                fig = px.line(sales_data,
                             x=sales_data.columns[0],
                             y="Sales_Volume",
                             title=f"{time_grouping} Sales Trend {' - ' + selected_category if selected_category != 'All' else ''}",
                             labels={"Sales_Volume": "Sales ($)"}
                            )
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "Bar Chart":
                if time_grouping == "Daily":
                    sales_data = df.groupby('Last_Restock_Date')['Sales_Volume'].sum().reset_index()
                elif time_grouping == "Weekly":
                    df['Week'] = df['Last_Restock_Date'].dt.isocalendar().week
                    sales_data = df.groupby('Week')['Sales_Volume'].sum().reset_index()
                else:  # Monthly
                    df['Month'] = df['Last_Restock_Date'].dt.strftime('%B %Y')
                    sales_data = df.groupby('Month')['Sales_Volume'].sum().reset_index()
                
                fig = px.bar(sales_data,
                            x=sales_data.columns[0],
                            y="Sales_Volume",
                            title=f"{time_grouping} Sales Distribution {' - ' + selected_category if selected_category != 'All' else ''}",
                            labels={"Sales_Volume": "Sales ($)"}
                           )
                st.plotly_chart(fig, use_container_width=True)
            
            else:  # Pie Chart
                if selected_category == "All":
                    category_sales = df.groupby('Category')['Sales_Volume'].sum().reset_index()
                    fig = px.pie(category_sales,
                                names="Category",
                                values="Sales_Volume",
                                title="Sales Distribution by Category"
                               )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pie chart is only available when 'All' categories are selected.")

# Analytics Page
elif page == "Analytics":
    st.title("Advanced Analytics")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Sales Performance Analysis
        st.markdown("### Sales Performance Analysis")
        
        # Time Series Decomposition
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Sales Trend")
            daily_sales = df.groupby('Last_Restock_Date')['Sales_Volume'].sum().reset_index()
            fig = px.line(daily_sales,
                         x="Last_Restock_Date",
                         y="Sales_Volume",
                         title="Daily Sales Trend"
                        )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Sales Distribution")
            fig = px.histogram(df,
                             x="Sales_Volume",
                             title="Sales Distribution",
                             nbins=30
                            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Product Performance Matrix
        st.markdown("### Product Performance Matrix")
        product_metrics = df.groupby('Product_ID').agg({
            'Sales_Volume': 'sum',
            'Stock_Level': 'mean'
        }).reset_index()
        
        fig = px.scatter(product_metrics,
                        x="Stock_Level",
                        y="Sales_Volume",
                        title="Product Performance Matrix",
                        labels={"Stock_Level": "Average Stock Level", "Sales_Volume": "Total Sales"}
                       )
        st.plotly_chart(fig, use_container_width=True)

# AI Insights Page
elif page == "AI Insights":
    st.title("AI-Generated Insights")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Generate insights
        insights = generate_sales_insights(df)
        recommendations = generate_recommendations(df)
        
        # Display insights
        st.markdown("### 🤖 Key Insights")
        for insight in insights:
            st.markdown(f"- {insight}")
        
        # Sales Forecasting
        st.markdown("### 📊 Sales Patterns")
        sales_pattern = df.groupby('Last_Restock_Date')['Sales_Volume'].sum()
        trend = np.polyfit(range(len(sales_pattern)), sales_pattern.values, 1)
        trend_line = np.poly1d(trend)
        
        forecast_data = pd.DataFrame({
            'Date': sales_pattern.index,
            'Actual': sales_pattern.values,
            'Trend': trend_line(range(len(sales_pattern)))
        })
        
        fig = px.line(forecast_data,
                     x="Date",
                     y=["Actual", "Trend"],
                     title="Sales Trend Analysis",
                     labels={"value": "Sales Volume", "variable": "Type"}
                    )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category Analysis
        st.markdown("### 📈 Category Performance Insights")
        category_metrics = df.groupby('Category').agg({
            'Sales_Volume': ['sum', 'mean', 'std'],
            'Stock_Level': 'mean'
        }).round(2)
        st.dataframe(category_metrics)

# Recommendations Page
elif page == "Recommendations":
    st.title("Smart Recommendations")
    
    if df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # AI Recommendations
        st.markdown("### 🤖 AI-Powered Recommendations")
        recommendations = generate_recommendations(df)
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        # Inventory Optimization
        st.markdown("### 📦 Inventory Optimization")
        
        # Stock Level Analysis
        stock_metrics = df.groupby('Product_ID').agg({
            'Stock_Level': 'mean',
            'Sales_Volume': 'sum'
        }).reset_index()
        
        stock_metrics['turnover_ratio'] = stock_metrics['Sales_Volume'] / stock_metrics['Stock_Level']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### High Stock, Low Sales")
            high_stock = stock_metrics[stock_metrics['turnover_ratio'] < stock_metrics['turnover_ratio'].quantile(0.25)]
            st.dataframe(high_stock.sort_values('turnover_ratio').head())
        
        with col2:
            st.markdown("#### Low Stock, High Sales")
            low_stock = stock_metrics[stock_metrics['turnover_ratio'] > stock_metrics['turnover_ratio'].quantile(0.75)]
            st.dataframe(low_stock.sort_values('turnover_ratio', ascending=False).head())
        
        # Restock Recommendations
        st.markdown("### 🔄 Restock Recommendations")
        restock_needed = df[df['Stock_Level'] < df['Sales_Volume'].mean()]
        if not restock_needed.empty:
            st.dataframe(restock_needed[['Product_ID', 'Category', 'Stock_Level', 'Sales_Volume']]
                        .sort_values('Stock_Level')
                        .head(10))
        else:
            st.info("No immediate restock recommendations at this time.")

# Add feedback collection
st.sidebar.markdown("---")
st.sidebar.markdown("### Feedback")
feedback = st.sidebar.text_area("Share your feedback or suggestions:")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback! We'll use it to improve the dashboard.")