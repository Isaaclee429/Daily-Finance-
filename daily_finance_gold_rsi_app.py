# daily_finance_gold_rsi_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import date
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="每日財經新聞 + 黃金 RSI 報告", layout="wide")
st.title("📊 每日財經新聞 + 黃金 RSI 報告")

# 1. 擷取財經新聞
st.header("📰 今日重要財經新聞")
@st.cache_data
def get_financial_news():
    url = "https://www.reuters.com/finance/"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h3')[:5]
        news = [h.get_text().strip() for h in headlines if h.get_text().strip()]
        return news
    except Exception as e:
        return ["無法擷取新聞，請稍後再試。"]

news_list = get_financial_news()
for idx, news in enumerate(news_list, 1):
    st.markdown(f"**{idx}.** {news}")

# 2. 黃金 RSI 報告
st.header("💰 黃金 RSI 每日分析 (GC=F)")
@st.cache_data
def get_gold_rsi():
    df = yf.download("GC=F", period="30d", interval="1d")
    if df.empty or "Close" not in df.columns:
        return pd.DataFrame()
    
    df = df.dropna(subset=["Close"])  # 確保 Close 沒有 NaN
    if df.empty:
        return pd.DataFrame()
    
    df["RSI"] = ta.momentum.RSIIndicator(close=df["Close"]).rsi()
    df = df.dropna(subset=["RSI"])
    return df


gold_df = get_gold_rsi()
if gold_df.empty:
    st.error("❌ 無法取得黃金價格資料")
else:
    today_rsi = gold_df["RSI"].iloc[-1]
    today_price = gold_df["Close"].iloc[-1]
    st.metric("最新黃金價格", f"${today_price:.2f}")
    st.metric("今日 RSI 值", f"{today_rsi:.2f}")

    st.subheader("📈 RSI 走勢圖 (30日)")
    st.line_chart(gold_df[["RSI"]])
# Daily-Finance-
