# daily_finance_news_app.py（多來源新聞擴充版）
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="每日財經新聞快報", layout="wide")
st.title("📊 每日財經新聞快報")

# 📰 擷取 Reuters 財經新聞
@st.cache_data
def get_reuters_news():
    try:
        url = "https://www.reuters.com/finance/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h3')[:5]
        return [h.get_text().strip() for h in headlines if h.get_text().strip()]
    except:
        return ["無法擷取 Reuters 新聞"]

# 📰 擷取 Bloomberg 財經新聞（首頁標題）
@st.cache_data
def get_bloomberg_news():
    try:
        url = "https://www.bloomberg.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h3')[:5]
        return [h.get_text().strip() for h in headlines if h.get_text().strip()]
    except:
        return ["無法擷取 Bloomberg 新聞"]

# 📰 擷取 Yahoo Finance 頭條新聞
@st.cache_data
def get_yahoo_news():
    try:
        url = "https://finance.yahoo.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h3')[:5]
        return [h.get_text().strip() for h in headlines if h.get_text().strip()]
    except:
        return ["無法擷取 Yahoo Finance 新聞"]

# 顯示區塊
st.header("📰 Reuters 財經新聞")
for i, news in enumerate(get_reuters_news(), 1):
    st.markdown(f"**{i}.** {news}")

st.header("📰 Bloomberg 財經新聞")
for i, news in enumerate(get_bloomberg_news(), 1):
    st.markdown(f"**{i}.** {news}")

st.header("📰 Yahoo Finance 新聞")
for i, news in enumerate(get_yahoo_news(), 1):
    st.markdown(f"**{i}.** {news}")
