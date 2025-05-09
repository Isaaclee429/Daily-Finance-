# global_market_news_app.py（優化摘要顯示格式）
import streamlit as st
import requests
from bs4 import BeautifulSoup
import feedparser
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
            p = article.find('p')
            if h and h.text.strip():
                title = h.text.strip()
                summary = p.text.strip() if p else "（此新聞無內文摘要）"
                headlines.append({"title": title, "link": url, "content": summary})
        return headlines
    except:
        return [{"title": "⚠️ 無法擷取 Reuters 世界新聞", "link": "", "content": ""}]

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
            if (
                "/news" in href and
                20 < len(title) < 150 and
                not any(x in title.lower() for x in ["photo", "bloomberg", "getty", "video", "/live/"])
            ):
                full_url = href if href.startswith("http") else f"https://www.bloomberg.com{href}"
                titles.append({"title": title, "link": full_url, "content": "（內文無法公開取得）"})
        return titles[:5] if titles else [{"title": "⚠️ Bloomberg 無標題", "link": "", "content": ""}]
    except:
        return [{"title": "⚠️ 無法擷取 Bloomberg 新聞", "link": "", "content": ""}]

# Investing RSS 擷取
@st.cache_data
def get_investing_rss():
    try:
        feed = feedparser.parse("https://www.investing.com/rss/news_25.rss")
        entries = feed.entries[:5]
        return [{"title": e.title, "link": e.link, "content": e.summary if hasattr(e, "summary") else "（內文摘要缺失）"} for e in entries]
    except:
        return [{"title": "⚠️ 無法擷取 Investing.com RSS", "link": "", "content": ""}]

# 標籤與摘要分類

def analyze_headline(headline):
    headline_lower = headline.lower()
    stock_keywords = ["fed", "interest rate", "inflation", "nasdaq", "apple", "jobs", "tech", "treasury"]
    gold_keywords = ["gold", "precious", "usd", "dollar", "geopolitical", "china", "safe haven", "central bank"]

    related_to_stock = any(keyword in headline_lower for keyword in stock_keywords)
    related_to_gold = any(keyword in headline_lower for keyword in gold_keywords)

    if related_to_stock and related_to_gold:
        tag = "📈 美股 & 🪙 黃金"
        summary = "此新聞可能同時影響股市與黃金市場。"
    elif related_to_stock:
        tag = "📈 美股"
        summary = "與美股或利率政策、財報有關。"
    elif related_to_gold:
        tag = "🪙 黃金"
        summary = "與黃金價格、避險情緒或美元變化有關。"
    else:
        tag = ""
        summary = "無直接市場影響，但值得關注其背景變化。"
    return tag, summary

# 顯示新聞清單
def display_news(source_title, news_list):
    st.subheader(f"📰 {source_title}")
    for i, item in enumerate(news_list, 1):
        tag, market_summary = analyze_headline(item['title'])
        st.markdown(f"### {i}. [{item['title']}]({item['link']})  {tag}")
        with st.expander("🧠 市場關聯分析摘要"):
            st.markdown(f"{market_summary}")
        with st.expander("📝 新聞內容簡述"):
            st.markdown(f"{item['content']}")
        st.markdown("---")

# 顯示各新聞來源
display_news("Reuters 國際新聞", get_reuters_headlines())
display_news("Bloomberg 焦點新聞", get_bloomberg_headlines())
display_news("Investing.com RSS 新聞", get_investing_rss())
