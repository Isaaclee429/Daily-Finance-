# global_market_news_app.py（加上日期顯示 + 加入 Yahoo Finance）
import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="全球財經頭條與市場影響快報", layout="wide")
st.title("🌍 全球財經頭條 + 美股與黃金市場影響分析")
st.markdown(f"🗓️ 今日日期：{datetime.today().strftime('%Y-%m-%d')}")

# Reuters 新聞擷取
@st.cache_data
def get_reuters_headlines():
    try:
        url = "https://www.reuters.com/world/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select("article.story-card")
        headlines = []
        for article in articles[:5]:
            h = article.find(['h3', 'h2'])
            if h and h.text.strip():
                headlines.append(h.text.strip())
        return headlines
    except:
        return ["⚠️ 無法擷取 Reuters 世界新聞"]

# Bloomberg 新聞擷取
@st.cache_data
def get_bloomberg_headlines():
    try:
        url = "https://www.bloomberg.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('a', href=True)
        titles = []
        for a in articles:
            title = a.get_text().strip()
            href = a['href']
            if len(title) > 25 and "/news" in href and title not in titles:
                titles.append(title)
        return titles[:5]
    except:
        return ["⚠️ 無法擷取 Bloomberg 新聞"]

# Yahoo Finance 新聞擷取
@st.cache_data
def get_yahoo_headlines():
    try:
        url = "https://finance.yahoo.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('h3')
        headlines = [i.get_text().strip() for i in items if len(i.get_text().strip()) > 20]
        return headlines[:5]
    except:
        return ["⚠️ 無法擷取 Yahoo Finance 新聞"]

# 簡易標籤 + AI 風格摘要

def analyze_headline(headline):
    headline_lower = headline.lower()
    stock_keywords = ["fed", "interest rate", "inflation", "nasdaq", "apple", "jobs", "tech", "treasury"]
    gold_keywords = ["gold", "precious", "usd", "dollar", "geopolitical", "china", "safe haven", "central bank"]

    related_to_stock = any(keyword in headline_lower for keyword in stock_keywords)
    related_to_gold = any(keyword in headline_lower for keyword in gold_keywords)

    if related_to_stock and related_to_gold:
        tag = "📈 美股 & 🪙 黃金"
        summary = "這則新聞同時關聯利率與避險主題，可能影響黃金與股市走勢。"
    elif related_to_stock:
        tag = "📈 美股"
        summary = "這則新聞與美股市場相關，可能影響投資人對政策或企業的預期。"
    elif related_to_gold:
        tag = "🪙 黃金"
        summary = "這則新聞與黃金價格相關，可能因市場避險需求升溫或美元變動所致。"
    else:
        tag = ""
        summary = "一般性國際新聞，目前尚無明確金融市場連結。"
    return
