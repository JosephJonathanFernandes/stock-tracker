import streamlit as st
import pandas as pd
import utils
import charts
import news
import os

# Page Config
st.set_page_config(
    page_title="NIFTY 50 Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if os.path.exists('assets/style.css'):
    local_css('assets/style.css')

# Load Data
@st.cache_data
def get_data():
    return utils.load_data('NIFTY50_all.csv', 'stock_metadata.csv')

df = get_data()

if df is None:
    st.error("Failed to load data. Please check if the CSV files exist.")
    st.stop()

# Sidebar
st.sidebar.title("🔍 Filter Options")

# 1. Industry Filter
industry_list = ["All"] + utils.get_industry_list(df)
selected_industry = st.sidebar.selectbox("Select Industry", industry_list)

# Filter by industry first to update stock list
if selected_industry != "All":
    df_filtered_industry = df[df['Industry'] == selected_industry]
else:
    df_filtered_industry = df

# 2. Stock Search
stock_list = utils.get_stock_list(df_filtered_industry)
# Create a label that combines Symbol and Name for easier searching
stock_options = stock_list['Symbol'] + " - " + stock_list['Company Name']
selected_stock_label = st.sidebar.selectbox("Search Stock", stock_options)
selected_symbol = selected_stock_label.split(" - ")[0]

# 3. Date Range
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.sidebar.error("Error: End date must fall after start date.")

# Filter Data
filtered_data = utils.filter_data(df, stock_symbol=selected_symbol, start_date=start_date, end_date=end_date)

# Main Dashboard
st.title(f"📈 {selected_symbol} Stock Dashboard")
st.markdown(f"**Industry:** {df[df['Symbol'] == selected_symbol]['Industry'].iloc[0]}")

# Key Metrics
if not filtered_data.empty:
    latest_data = filtered_data.iloc[-1]
    prev_data = filtered_data.iloc[-2] if len(filtered_data) > 1 else latest_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Closing Price", f"₹{latest_data['Close']:.2f}", f"{latest_data['Close'] - prev_data['Close']:.2f}")
    with col2:
        st.metric("Volume", f"{latest_data['Volume']:,}", f"{latest_data['Volume'] - prev_data['Volume']:,}")
    with col3:
        st.metric("Day High", f"₹{latest_data['High']:.2f}")
    with col4:
        st.metric("Day Low", f"₹{latest_data['Low']:.2f}")

# Charts
col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    st.subheader("Price History")
    chart_type = st.radio("Chart Type", ["Line", "Candlestick"], horizontal=True)
    if chart_type == "Line":
        st.plotly_chart(charts.plot_stock_price(filtered_data, selected_symbol), use_container_width=True)
    else:
        st.plotly_chart(charts.plot_candlestick(filtered_data, selected_symbol), use_container_width=True)

with col_chart2:
    st.subheader("Volume Analysis")
    st.plotly_chart(charts.plot_volume(filtered_data, selected_symbol), use_container_width=True)

# Industry Analysis Section
st.markdown("---")
st.header("📊 Industry Analysis")
col_ind1, col_ind2 = st.columns(2)

with col_ind1:
    st.plotly_chart(charts.plot_industry_pie(df), use_container_width=True)

with col_ind2:
    st.plotly_chart(charts.plot_industry_comparison(df), use_container_width=True)

# News Section
st.markdown("---")
st.header(f"📰 Latest News for {selected_symbol}")

news_items = news.fetch_news(selected_symbol)

if news_items:
    for item in news_items:
        st.markdown(f"""
        <div class="news-card">
            <h4><a href="{item['link']}" target="_blank">{item['title']}</a></h4>
            <p class="date">{item['source']} • {item['date']}</p>
            <p>{item['snippet']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No news found.")

