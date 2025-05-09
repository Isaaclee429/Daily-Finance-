# global_market_news_app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="全球財經頭條與市場影響快報", layout="wide")
st.title("🌍 全球財經頭條 + 美股與黃金市場影響分析")

# 🌐 抓取 Reuters 頭條
@st.cache_data
def get_reuters_headlines():
    try:
        url = "https://www.reuters.com/world/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all(['h2', 'h3'])[:10]
        return [h.get_text().strip() for h in headlines if h.get_text().strip()]
    except:
        return ["無法擷取 Reuters 世界新聞"]

# 關鍵字判斷是否與美股或黃金有關
def categorize_headline(headline):
    headline_lower = headline.lower()
    stock_keywords = ["fed", "interest rate", "inflation", "nasdaq", "apple", "jobs report", "tech", "treasury"]
    gold_keywords = ["gold", "precious metal", "usd", "dollar", "geopolitical", "china", "safe haven", "central bank"]

    related_to_stock = any(keyword in headline_lower for keyword in stock_keywords)
    related_to_gold = any(keyword in headline_lower for keyword in gold_keywords)

    tag = ""
    if related_to_stock and related_to_gold:
        tag = "📈 美股 & 🪙 黃金"
    elif related_to_stock:
        tag = "📈 美股"
    elif related_to_gold:
        tag = "🪙 黃金"
    else:
        tag = ""  # 一般新聞
    return tag

# 顯示區塊
st.subheader("📰 全球重要新聞頭條 (來源：Reuters World)")
headlines = get_reuters_headlines()

for i, h in enumerate(headlines, 1):
    tag = categorize_headline(h)
    if tag:
        st.markdown(f"**{i}.** {h} — {tag}")
    else:
        st.markdown(f"{i}. {h}")

st.info("🔍 以上標題會依內容自動標註與美股/黃金相關的新聞。後續可加入 AI 自動摘要與 Email 報告功能。")
