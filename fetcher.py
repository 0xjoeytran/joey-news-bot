import os
from datetime import datetime
from dotenv import load_dotenv
import feedparser

load_dotenv()

async def fetch_latest_tweets():
    """Crawl từ X KOLs + Cointelegraph + The Block + Bloomberg"""
    
    tweets = []
    
    # ======================= RSS SOURCES =======================
    rss_sources = [
        ("Cointelegraph", "https://cointelegraph.com/rss"),
        ("The Block", "https://www.theblock.co/rss.xml"),
        ("Bloomberg Crypto", "https://feeds.bloomberg.com/crypto/news.rss"),   # Bloomberg Crypto
        ("Bloomberg Markets", "https://feeds.bloomberg.com/markets/news.rss")
    ]
    
    for source_name, rss_url in rss_sources:
        try:
            print(f"📰 Đang lấy tin từ {source_name}...")
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:6]:   # Lấy tối đa 6 tin mới nhất mỗi nguồn
                summary = entry.description[:250] if hasattr(entry, 'description') else ""
                tweets.append({
                    "text": f"{entry.title}. {summary}...",
                    "url": entry.link,
                    "source": source_name
                })
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy {source_name}: {e}")
    
    # ======================= DEMO KOLs (MACRO + SWING + ONCHAIN) =======================
    demo_tweets = [
        {
            "text": "Lạm phát Nhật Bản tiếp tục hạ nhiệt, BOJ có thể giữ lãi suất thấp hơn dự kiến → Tích cực cho carry trade và BTC.",
            "url": "https://x.com/example",
            "source": "RaoulGMI (Demo - MACRO)"
        },
        {
            "text": "BTC weekly chart cho thấy dấu hiệu breakout. Swing trade target ngắn hạn: 118k - 125k.",
            "url": "https://x.com/example",
            "source": "RektCapital (Demo - BTC_SWING)"
        },
        {
            "text": "On-chain data cho thấy whale tích lũy mạnh, exchange outflow tăng.",
            "url": "https://x.com/example",
            "source": "willywoo (Demo - ONCHAIN)"
        }
    ]
    
    tweets.extend(demo_tweets)
    
    print(f"✅ Tổng cộng {len(tweets)} tin từ RSS + Demo KOLs (MACRO + BTC_SWING + ONCHAIN)")
    return tweets
