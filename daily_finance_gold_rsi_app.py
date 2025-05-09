# daily_finance_news_app.py（僅保留新聞功能）
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="每日財經新聞快報", layout="wide")
st.title("📊 每日財經新聞快報")

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
