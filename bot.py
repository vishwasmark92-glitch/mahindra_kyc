import os
import telebot
from flask import Flask, request
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-domain.com")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# ===================== BOT HANDLERS =====================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command"""
    bot.reply_to(message, "Welcome! I'm your KYC bot.")

@bot.message_handler(commands=['help'])
def send_help(message):
    """Handle /help command"""
    bot.reply_to(message, "Available commands:\n/start - Start the bot\n/help - Show this message")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    """Handle all other messages"""
    bot.reply_to(message, "I received your message: " + message.text)

# ===================== FLASK ROUTES =====================

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram webhook"""
    try:
        json_data = request.get_json()
        if json_data:
            update = telebot.types.Update.de_json(json_data)
            bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return "ERROR", 400

@app.route('/get_commands', methods=['GET'])
def get_commands():
    """Handle device commands"""
    device_id = request.args.get('device_id')
    logger.info(f"Device command request: {device_id}")
    return {"status": "ok", "device_id": device_id}, 200

@app.route('/admin/get_data', methods=['GET'])
def admin_get_data():
    """Handle admin data requests"""
    logger.info("Admin data request received")
    return {"status": "ok", "data": []}, 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}, 200

# ===================== INITIALIZATION =====================

def setup_webhook():
    """Setup webhook for Telegram bot"""
    try:
        # Delete any existing webhook to avoid conflicts
        bot.delete_webhook()
        logger.info("Existing webhook deleted")
        
        # Set new webhook
        webhook_url = f"{WEBHOOK_URL}/webhook"
        bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    except Exception as e:
        logger.error(f"Error setting up webhook: {e}")

def setup_polling():
    """Setup polling for Telegram bot"""
    try:
        # Delete any existing webhook first
        bot.delete_webhook()
        logger.info("Deleted webhook, starting polling mode")
        
        # Start polling
        bot.infinity_polling(allowed_updates=['message'], timeout=30)
    except Exception as e:
        logger.error(f"Error in polling: {e}")

# ===================== MAIN =====================

if __name__ == '__main__':
    if ENVIRONMENT == "production":
        # Production: Use webhook (for Railway, Heroku, etc.)
        logger.info("Starting in PRODUCTION mode with webhook...")
        setup_webhook()
        app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=False)
    else:
        # Development: Use polling
        logger.info("Starting in DEVELOPMENT mode with polling...")
        setup_polling()
