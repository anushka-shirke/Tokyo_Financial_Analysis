# streamlit_app.py

import streamlit as st
import pandas as pd
import datetime 
import yfinance as yf
import seaborn as sb
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(page_title="Tokyo Stock Explorer", layout="wide")

st.title("Tokyo Stock Price Explorer 📈")
st.write("Explore major Japanese companies' stock data between April 2023 and April 2025.")

# Set start and end dates
s = datetime.datetime(2023, 4, 1)
e = datetime.datetime(2025, 4, 27)

# Download stock data
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
        data = yf.download(ticker, start=s, end=e)
        data.columns = data.columns.get_level_values(0)
        data = data.reset_index()
        data['Symbol'] = name
        frames.append(data)
    
    df = pd.concat(frames, axis=0)
    
    df['Price_change'] = df['Close'] - df['Open']
    df['High_Low_Spread'] = df['High'] - df['Low']
    df['Close_Open_Spread'] = df['Close'] - df['Open']
    
    return df

# Load data
df = load_data()

# Show the available companies
symbols = df.Symbol.unique()

st.sidebar.header("Select Stock")
selected_stock = st.sidebar.selectbox("Choose a stock to visualize:", symbols)

# Filter data
stk = df[df.Symbol == selected_stock]

# Plot
st.subheader(f"Closing Price Trend for {selected_stock}")
fig, ax = plt.subplots(figsize=(12,6))
sb.lineplot(x=stk.Date, y=stk.Close, ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Close Price (JPY)")
plt.title(f"{selected_stock} Stock Price Over Time")
st.pyplot(fig)

# Option to download the CSV
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

# Optional: Show full dataset if needed
if st.checkbox("Show full dataset"):
    st.dataframe(df)
