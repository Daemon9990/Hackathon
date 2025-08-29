import json
import os
from pyrogram import Client, filters
from finance_core import calculate_savings, calculate_tax, suggest_investment, add_goal, track_goals

# Telegram bot setup
API_ID = int(os.getenv("API_ID", "24830912"))
API_HASH = os.getenv("API_HASH", "a1a1775593531b90850b8b82e3b14940")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8438748276:AAF_499AMQV-xXWC4ea36x_skxsjFkktpU8")

app = Client("finance_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Load database
DB_FILE = "database.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(
        "👋 Hello! I’m your Personal Finance Chatbot.\n\n"
        "I can help you with:\n"
        "💰 Savings guidance\n"
        "💸 Tax calculations\n"
        "📈 Investment suggestions\n"
        "🎯 Goal tracking\n\n"
        "Commands:\n"
        "/savings income expenses\n"
        "/tax salary investments\n"
        "/invest risk_level\n"
        "/goal amount description deadline\n"
        "/track\n"
    )

# Savings command
@app.on_message(filters.command("savings"))
def savings_cmd(client, message):
    try:
        _, income, expenses = message.text.split()
        result = calculate_savings(int(income), int(expenses))
        message.reply_text(result)
    except:
        message.reply_text("❌ Usage: /savings income expenses")

# Tax command
@app.on_message(filters.command("tax"))
def tax_cmd(client, message):
    try:
        _, salary, investments = message.text.split()
        result = calculate_tax(int(salary), int(investments))
        message.reply_text(result)
    except:
        message.reply_text("❌ Usage: /tax salary investments")

# Investment command
@app.on_message(filters.command("invest"))
def invest_cmd(client, message):
    try:
        _, risk = message.text.split()
        result = suggest_investment(risk.lower())
        message.reply_text(result)
    except:
        message.reply_text("❌ Usage: /invest low|balanced|high")

# Goal setting
@app.on_message(filters.command("goal"))
def goal_cmd(client, message):
    try:
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            message.reply_text("❌ Usage: /goal amount description deadline")
            return
        _, amount, description, deadline = parts
        user_id = str(message.from_user.id)

        db = load_db()
        msg = add_goal(db, user_id, int(amount), description, deadline)
        save_db(db)

        message.reply_text(msg)
    except:
        message.reply_text("❌ Usage: /goal amount description deadline")

# Track goals
@app.on_message(filters.command("track"))
def track_cmd(client, message):
    user_id = str(message.from_user.id)
    db = load_db()
    msg = track_goals(db, user_id)
    message.reply_text(msg)

if __name__ == "__main__":
    print("🚀 Bot is running...")
    app.run()
