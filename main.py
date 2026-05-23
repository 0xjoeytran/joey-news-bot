import os
from bot import bot

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    
    print("🔍 Joey News Bot đang kiểm tra Environment Variables...")
    print(f"DISCORD_TOKEN tồn tại: {'✅ Có' if token else '❌ Không'}")
    
    if not token:
        print("❌ Không tìm thấy DISCORD_TOKEN!")
        print("Các variables hiện có:", [key for key in os.environ.keys() if "TOKEN" in key or "DISCORD" in key])
        print("💡 Hãy kiểm tra lại tên biến chính xác là DISCORD_TOKEN (không có khoảng trắng)")
    else:
        print("🚀 Joey News Bot đang khởi động trên Railway...")
        print("✅ DISCORD_TOKEN đã load thành công!")
        bot.run(token)
