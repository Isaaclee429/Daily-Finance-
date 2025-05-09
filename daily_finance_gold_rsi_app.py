# global_market_news_app.py（改為抓取正確新聞標題區）
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="全球財經頭條與市場影響快報", layout="wide")
st.title("🌍 全球財經頭條 + 美股與黃金市場影響分析")

# 🌐 正確抓取 Reuters World News 區塊標題
@st.cache_data
def get_reuters_headlines():
    try:
        url = "https://www.reuters.com/world/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select("article.story-card")
        headlines = []
        for article in articles[:8]:
            h = article.find(['h3', 'h2'])
            if h and h.text.strip():
                headlines.append(h.text.strip())
        return headlines
    except:
        return ["⚠️ 無法擷取 Reuters 世界新聞，請稍後再試"]

# 分析關聯並生成摘要
def analyze_headline(headline):
    headline_lower = headline.lower()
    stock_keywords = ["fed", "interest rate", "inflation", "nasdaq", "apple", "jobs report", "tech", "treasury"]
    gold_keywords = ["gold", "precious metal", "usd", "dollar", "geopolitical", "china", "safe haven", "central bank"]

    related_to_stock = any(keyword in headline_lower for keyword in stock_keywords)
    related_to_gold = any(keyword in headline_lower for keyword in gold_keywords)

    if related_to_stock and related_to_gold:
        tag = "📈 美股 & 🪙 黃金"
        summary = "此新聞可能同時影響美股與黃金市場，與利率或避險需求相關。"
    elif related_to_stock:
        tag = "📈 美股"
        summary = "與美股相關，可能涉及利率政策、財報或宏觀數據。"
    elif related_to_gold:
        tag = "🪙 黃金"
        summary = "與黃金相關，可能因地緣風險或央行動態造成影響。"
    else:
        tag = ""
        summary = "一般新聞，暫無明顯市場連動性。"
    return tag, summary

# 顯示區塊
st.subheader("📰 今日重點新聞（來自 Reuters World）")
headlines = get_reuters_headlines()

for i, h in enumerate(headlines, 1):
    tag, summary = analyze_headline(h)
    st.markdown(f"**{i}. {h}**  {tag if tag else ''}")
    st.markdown(f"📌 {summary}")
    st.markdown("---")
