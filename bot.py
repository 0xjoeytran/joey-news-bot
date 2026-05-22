import discord
from discord.ext import tasks
from classifier import classify_news
from fetcher import fetch_latest_tweets
from config import CATEGORIES
import os
import sqlite3
import json
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

CHANNEL_MAP_FILE = 'channel_map.json'
channel_map = {}

def load_channel_map():
    if os.path.exists(CHANNEL_MAP_FILE):
        try:
            with open(CHANNEL_MAP_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_channel_map():
    with open(CHANNEL_MAP_FILE, 'w') as f:
        json.dump(channel_map, f, indent=2)

# ======================= DATABASE =======================
def init_db():
    conn = sqlite3.connect('news_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (timestamp TEXT, category TEXT, source TEXT, summary TEXT, url TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(category, source, summary, url):
    conn = sqlite3.connect('news_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO news VALUES (datetime('now'), ?, ?, ?, ?)", 
              (category, source, summary, url))
    conn.commit()
    conn.close()

def get_daily_news():
    conn = sqlite3.connect('news_history.db')
    c = conn.cursor()
    c.execute("""SELECT category, source, summary, url 
                 FROM news 
                 WHERE timestamp >= datetime('now', '-24 hours')
                 ORDER BY timestamp DESC""")
    return c.fetchall()

# ======================= DAILY DIGEST =======================
async def send_daily_digest():
    news = get_daily_news()
    if not news:
        return "📭 Không có tin mới trong 24h qua."

    digest = f"📊 **JOEY DAILY DIGEST - {datetime.now().strftime('%d/%m/%Y')}**\n\n"

    categories = {}
    for cat, source, summary, url in news:
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f"• {summary} | {source}")

    for cat_name, emoji in [("MACRO - Vĩ Mô", "📉"), ("BTC_SWING", "₿"), ("ONCHAIN", "📊")]:
        if cat_name in categories:
            digest += f"{emoji} **{cat_name}**\n" + "\n".join(categories[cat_name][:4]) + "\n\n"

    digest += "🔥 **Key Takeaway**: Theo dõi liquidity Nhật Bản và on-chain BTC."
    return digest

# ======================= CHANNEL MANAGEMENT =======================
def clean_channel_name(name):
    return name.lower().replace(" ", "-").replace("–", "-").replace("/", "").replace("'", "").replace(":", "").strip()

async def get_or_create_channel(guild, name):
    global channel_map
    clean_name = clean_channel_name(name)
    
    if clean_name in channel_map:
        channel = discord.utils.get(guild.channels, id=channel_map[clean_name])
        if channel:
            return channel

    for ch in guild.channels:
        if clean_channel_name(ch.name) == clean_name:
            channel_map[clean_name] = ch.id
            save_channel_map()
            return ch

    try:
        channel = await guild.create_text_channel(clean_name)
        channel_map[clean_name] = channel.id
        save_channel_map()
        print(f"🆕 Joey News Bot đã tạo channel: {clean_name}")
        return channel
    except:
        return None

@bot.event
async def on_ready():
    print(f"✅ Joey News Bot đã online!")
    global channel_map
    channel_map = load_channel_map()
    init_db()
    
    for guild in bot.guilds:
        print(f"🔧 Joey News Bot đang setup channels cho server: {guild.name}")
        
        for cat in CATEGORIES:
            await get_or_create_channel(guild, cat)
        
        await get_or_create_channel(guild, "daily-digest")
    
    news_scanner.start()
    daily_digest.start()

@tasks.loop(minutes=180)
async def news_scanner():
    print("🔍 Joey News Bot đang quét tin (3 giờ/lần)...")
    tweets = await fetch_latest_tweets()
    
    for tweet in tweets:
        result = await classify_news(tweet['text'])
        clean_name = clean_channel_name(result['category'])
        
        channel = discord.utils.get(bot.get_all_channels(), name=clean_name)
        if channel:
            msg = f"{result['emoji']} **{result['category']}** | {tweet['source']}\n{result['summary']}\n🔗 {tweet['url']}"
            await channel.send(msg)
            save_to_db(result['category'], tweet['source'], result['summary'], tweet['url'])

@tasks.loop(hours=1)
async def daily_digest():
    now = datetime.now()
    if now.hour == 20 and now.minute < 5:
        print("📋 Joey News Bot đang tạo Daily Digest...")
        digest_text = await send_daily_digest()
        channel = discord.utils.get(bot.get_all_channels(), name="daily-digest")
        if channel:
            await channel.send("────────────────────")
            await channel.send(digest_text)

print("✅ Joey News Bot đang chạy ổn định")
