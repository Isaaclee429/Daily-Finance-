# global_market_news_app.py（Yahoo 移除 + 改抓 Investing.com）
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
            if "/news" in href and 20 < len(title) < 150 and title not in titles:
                titles.append(title)
        return titles[:5] if titles else ["⚠️ Bloomberg 無標題"]
    except:
        return ["⚠️ 無法擷取 Bloomberg 新聞"]

# Investing.com 新聞擷取
@st.cache_data
def get_investing_headlines():
    try:
        url = "https://www.investing.com/news/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select(".textDiv")
        headlines = [a.get_text(strip=True) for a in articles if 20 < len(a.get_text(strip=True)) < 150]
        return headlines[:5] if headlines else ["⚠️ Investing 無標題"]
    except:
        return ["⚠️ 無法擷取 Investing.com 新聞"]

# 標籤與摘要生成

def analyze_headline(headline):
    headline_lower = headline.lower()
    stock_keywords = ["fed", "interest rate", "inflation", "nasdaq", "apple", "jobs", "tech", "treasury"]
    gold_keywords = ["gold", "precious", "usd", "dollar", "geopolitical", "china", "safe haven", "central bank"]

    related_to_stock = any(keyword in headline_lower for keyword in stock_keywords)
    related_to_gold = any(keyword in headline_lower for keyword in gold_keywords)

    if related_to_stock and related_to_gold:
        tag = "📈 美股 & 🪙 黃金"
        summary = "同時涉及股市與黃金相關議題，可能對兩者皆造成影響。"
    elif related_to_stock:
        tag = "📈 美股"
        summary = "與股市、利率、就業或企業財報等議題相關。"
    elif related_to_gold:
        tag = "🪙 黃金"
        summary = "與避險情緒、美元走勢或黃金需求相關。"
    else:
        tag = ""
        summary = "新聞與金融市場無直接關聯，但可觀察背景發展。"
    return tag, summary

# 顯示 Reuters
st.subheader("📰 Reuters 國際新聞")
for i, h in enumerate(get_reuters_headlines(), 1):
    tag, summary = analyze_headline(h)
    st.markdown(f"**{i}. {h}**  {tag}")
    st.markdown(f"📌 {summary}")
    st.markdown("---")

# 顯示 Bloomberg
st.subheader("📰 Bloomberg 焦點新聞")
for i, h in enumerate(get_bloomberg_headlines(), 1):
    tag, summary = analyze_headline(h)
    st.markdown(f"**{i}. {h}**  {tag}")
    st.markdown(f"📌 {summary}")
    st.markdown("---")

# 顯示 Investing.com
st.subheader("📰 Investing.com 新聞")
for i, h in enumerate(get_investing_headlines(), 1):
    tag, summary = analyze_headline(h)
    st.markdown(f"**{i}. {h}**  {tag}")
    st.markdown(f"📌 {summary}")
    st.markdown("---")
