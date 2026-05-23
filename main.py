import os
from dotenv import load_dotenv
from bot import bot

# Load .env cho local
load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("❌ Chưa điền DISCORD_TOKEN! Vui lòng kiểm tra Environment Variables trên Railway.")
        print("💡 Kiểm tra lại Variables và Redeploy.")
        # Không exit nữa, để Railway retry
        import time
        time.sleep(10)
    else:
        print("🚀 Joey News Bot đang khởi động trên Railway...")
        print(f"✅ DISCORD_TOKEN đã được load thành công!")
        bot.run(token)
