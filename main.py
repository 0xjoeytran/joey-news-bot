import os
from dotenv import load_dotenv
from bot import bot

load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token or token == "your_discord_bot_token_here":
        print("❌ Chưa điền DISCORD_TOKEN trong file .env!")
    else:
        bot.run(token)
