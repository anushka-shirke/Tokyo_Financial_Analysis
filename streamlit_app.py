# streamlit_app.py

import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Tokyo Stock Explorer", layout="wide")

# Background Image with Black Text using Custom HTML and CSS
def add_bg_from_url():
    # Use the provided image URL
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/1440476/pexels-photo-1440476.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
             background-attachment: fixed;
             background-size: cover;
             background-position: center center;
             color: black;
         }}
         .stApp > .main {{
             background-color: rgba(255, 255, 255, 0.7);  /* Optional: Adds a semi-transparent background to text for better readability */
         }}
         h1, h2, h3, h4, h5, h6, p {{
             color: black;
         }}
         .stSidebar {{
             background-color: rgba(255, 255, 255, 0.9); /* Optional: Add semi-transparent background to sidebar */
             color: black;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# App Title
st.title("📈 Tokyo Stock Price Explorer")
st.write("Explore major Japanese companies' stock prices between April 2023 and April 2025.")

# Dates
start_date = datetime.datetime(2023, 4, 1)
end_date = datetime.datetime(2025, 4, 27)

# Load data function
@st.cache_data
def load_data():
    companies = {
        'SONY': '6758.T',
        'TOYOTA': '7203.T',
        'HONDA': '7267.T',
        'MITSUBISHI CORP': '8058.T',
        'NISSAN MOTOR CORP': '7201.T',
        'NIPPON STEEL CORP': '5401.T',
        'HITACHI': '6501.T',
        'NINTENDO': '7974.T',
        'FUJITSU': '6702.T',
        'JAPAN AIRLINES': '9201.T'
    }
    
    frames = []
    for name, ticker in companies.items():
        data = yf.download(ticker, start=start_date, end=end_date)
        data.columns = data.columns.get_level_values(0)
        data = data.reset_index()
        data['Symbol'] = name
        frames.append(data)
    
    df = pd.concat(frames, axis=0)
    df['Price_change'] = df['Close'] - df['Open']
    df['High_Low_Spread'] = df['High'] - df['Low']
    df['Close_Open_Spread'] = df['Close'] - df['Open']
    return df

# Show loading spinner
with st.spinner('Fetching stock data... Please wait...'):
    df = load_data()

# Sidebar - Stock selection
st.sidebar.header("Select Stock")
symbols = df.Symbol.unique()
selected_stock = st.sidebar.selectbox("Choose a stock to visualize:", symbols)

# Sidebar - Chart settings
st.sidebar.header("Chart Settings")
chart_type = st.sidebar.radio("Choose chart type:", ['Static (Seaborn)', 'Interactive (Plotly)'])

# Sidebar - Download data
st.sidebar.header("Download Data")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.sidebar.download_button(
    label="Download full dataset as CSV",
    data=csv,
    file_name='tokyo_index.csv',
    mime='text/csv',
)

# Filter selected stock
stk = df[df.Symbol == selected_stock]

# Main Area - Plotting
st.subheader(f"📊 Closing Price Trend for {selected_stock}")

if chart_type == 'Static (Seaborn)':
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=stk.Date, y=stk.Close, ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Close Price (JPY)")
    plt.title(f"{selected_stock} Stock Price Over Time")
    st.pyplot(fig)
else:
    fig = px.line(stk, x='Date', y='Close', title=f"{selected_stock} Stock Price Over Time (Interactive)")
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

# Checkbox - Show Full Dataset
if st.checkbox("Show Full Dataset"):
    st.dataframe(df)
