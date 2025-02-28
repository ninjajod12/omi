import subprocess
import logging
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram Bot Token
TOKEN = "7636730003:AAFRKwkdag_9JwLRkwS7vhddut91jqIcJtM"
# Your Telegram User ID (for security)
AUTHORIZED_USER_ID = 6073143283

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def keep_alive():
    """Keep-alive function to prevent timeout."""
    while True:
        logger.info("Bot is still running...")
        time.sleep(30)  # Every 30 seconds, print this message to prevent idle timeout

# Start keep-alive thread
threading.Thread(target=keep_alive, daemon=True).start()

def start(update: Update, context: CallbackContext):
    if update.message.chat_id != AUTHORIZED_USER_ID:
        update.message.reply_text("Unauthorized access.")
        return
    update.message.reply_text("Welcome! Send me any command to execute on the VPS.")

def execute_command(update: Update, context: CallbackContext):
    if update.message.chat_id != AUTHORIZED_USER_ID:
        update.message.reply_text("Unauthorized access.")
        return
    
    command = update.message.text
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10)
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.output}"
    except subprocess.TimeoutExpired:
        output = "Error: Command timed out."
    except Exception as e:
        output = f"Error: {str(e)}"
    
    update.message.reply_text(f"Output:\n{output[:4000]}")  # Telegram has a 4096 character limit

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, execute_command))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
