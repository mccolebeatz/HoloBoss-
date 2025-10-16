import os
import re
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv"8480613736:AAH0NiM2UfgSNT_Hyf0DFuIf3wf82Hq-0Fs"

DATA_FILE = "data.json"

# ---------------------- UTILITIES ----------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"links": [], "leaders": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def is_valid_link(link: str) -> bool:
    """Allow only Instagram or TikTok URLs"""
    pattern = r"^(https?:\/\/)?(www\.)?(instagram\.com|tiktok\.com)\/[^\s]+$"
    return re.match(pattern, link) is not None

# ---------------------- COMMAND1 /start ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Inner Circle 2025!\n\n"
        "Use /help to see all commands."
    )

# ---------------------- COMMAND2 /help ----------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 Command List:\n\n"
        "Command1 /start - Show welcome message\n"
        "Command2 /help - Show this help menu\n"
        "Command3 /rules - Show rules\n"
        "Command4 /queue - Show last 7 shared links\n"
        "Command5 /leaderboard - See the top sharers\n"
        "Command6 /share <link> - Share a new Instagram or TikTok link"
    )
    await update.message.reply_text(help_text)

# ---------------------- COMMAND3 /rules ----------------------
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 Rules:\n"
        "1. Be respectful and supportive.\n"
        "2. Share only Instagram or TikTok links.\n"
        "3. No spam or fake engagement.\n"
        "4. Stay positive and authentic!"
    )

# ---------------------- COMMAND4 /queue ----------------------
async def queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    links = data.get("links", [])
    if not links:
        await update.message.reply_text("🧾 No shared links yet!")
        return
    text = "🧾 Last 7 Shared Links:\n\n" + "\n".join(links[-7:])
    await update.message.reply_text(text)

# ---------------------- COMMAND5 /leaderboard ----------------------
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    leaders = data.get("leaders", {})
    if not leaders:
        await update.message.reply_text("🏁 No one has shared any links yet!")
        return
    sorted_leaders = sorted(leaders.items(), key=lambda x: x[1], reverse=True)
    leaderboard_text = "🏆 Top Sharers:\n\n"
    for i, (user, count) in enumerate(sorted_leaders[:5], start=1):
        leaderboard_text += f"{i}. {user} — {count} shares\n"
    await update.message.reply_text(leaderboard_text)

# ---------------------- COMMAND6 /share ----------------------
async def share(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please include a link.\nExample:\n/share https://instagram.com/yourpost")
        return

    link = context.args[0].strip()
    if not is_valid_link(link):
        await update.message.reply_text("🚫 Invalid link. Please share only Instagram or TikTok URLs.")
        return

    user = update.message.from_user.username or update.message.from_user.first_name
    data = load_data()

    data["links"].append(link)
    if len(data["links"]) > 50:  # limit stored links
        data["links"] = data["links"][-50:]

    data["leaders"][user] = data["leaders"].get(user, 0) + 1
    save_data(data)

    await update.message.reply_text(f"✅ Thanks {user}! Your link has been shared successfully.")

# ---------------------- RUN THE BOT ----------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("queue", queue))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("share", share))

    print("🤖 Inner Circle Bot is live and secured!")
    app.run_polling()

if __name__ == "__main__":
    main()
