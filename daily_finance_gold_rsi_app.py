# global_market_news_app.py（整合 Bloomberg 並加入 AI 風格摘要）
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="全球財經頭條與市場影響快報", layout="wide")
st.title("🌍 全球財經頭條 + 美股與黃金市場影響分析")

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

# 簡易標籤 + 模擬 AI 摘要

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
    return tag, summary

# 顯示 Reuters
st.subheader("📰 Reuters 國際新聞")
reuters_news = get_reuters_headlines()
for i, h in enumerate(reuters_news, 1):
    tag, summary = analyze_headline(h)
    st.markdown(f"**{i}. {h}**  {tag if tag else ''}")
    st.markdown(f"📌 {summary}")
    st.markdown("---")

# 顯示 Bloomberg
st.subheader("📰 Bloomberg 焦點新聞")
bloomberg_news = get_bloomberg_headlines()
for i, h in enumerate(bloomberg_news, 1):
    tag, summary = analyze_headline(h)
    st.markdown(f"**{i}. {h}**  {tag if tag else ''}")
    st.markdown(f"📌 {summary}")
    st.markdown("---")
