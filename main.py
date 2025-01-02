import os
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN: Final = os.getenv('BOT_TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Thanks for Chatting With Me. I am an orange')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('I am an Orange! Type Something so I can Response!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Custom a Command!')

#Handle Responses
def handle_responses(text: str) -> str:
    processed: str = text.lower()
    if 'hello' == processed or 'hi' == processed:
        return 'Hello There! Nice to meet you!'

    elif 'how are you' == processed:
        return 'I\'m fine, thank you!'

    elif 'i love you' == processed:
        return 'Thank You, That\'s wonderful'

    elif 'i love python' == processed:
        return 'I love python too!'

    return 'Sorry, I don\'t understand.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global response
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User({update.message.from_user.id}) Type: {message_type} Text: {text}')

    if message_type == 'supergroup':
        # Check if the bot's username is mentioned
        if BOT_USERNAME in text:
            # Extract the remaining text after removing the username
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_responses(new_text)
        elif message_type=='private':
            # Ignore messages that don't mention the bot
            return
    else:
        # Handle private messages
        response = handle_responses(text)

    print(f'Bot: {response}')
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Telegram Bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polling
    print('Polling Telegram Bot...')
    app.run_polling(poll_interval=3)






