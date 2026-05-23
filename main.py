import os
from dotenv import load_dotenv
from bot import bot

# Load .env cho local development
load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("❌ Chưa điền DISCORD_TOKEN! Vui lòng kiểm tra Environment Variables trên Railway.")
        exit(1)
    
    print("🚀 Joey News Bot đang khởi động...")
    bot.run(token)
