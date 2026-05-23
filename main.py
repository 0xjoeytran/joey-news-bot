import os
from dotenv import load_dotenv
from bot import bot

# Load .env cho local development
load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("❌ Không tìm thấy DISCORD_TOKEN!")
        print("💡 Đang kiểm tra Environment Variables từ Railway...")
        print("Các variables hiện có:", list(os.environ.keys()))
        
        # Thử lại sau 5 giây (cho Railway inject variable)
        import time
        time.sleep(5)
        token = os.getenv("DISCORD_TOKEN")
        
        if not token:
            print("❌ Vẫn không tìm thấy DISCORD_TOKEN. Vui lòng kiểm tra Variables trên Railway và Redeploy.")
            # Không exit để Railway không crash liên tục
            time.sleep(30)
        else:
            print("✅ Tìm thấy DISCORD_TOKEN sau khi retry!")
    else:
        print("🚀 Joey News Bot đang khởi động trên Railway...")
        print("✅ DISCORD_TOKEN đã load thành công!")
    
    if token:
        bot.run(token)
    else:
        print("⛔ Không thể khởi động bot do thiếu token.")
