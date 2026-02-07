from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
firebase_admin.initialize_app(cred, {'databaseURL': os.getenv("FIREBASE_DB_URL")})

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract the numerical value from the user's message
    chat_id = update.message.chat_id
    try:
        total = float(get_user_total(chat_id))
        value = float(context.args[0])
        total += value
        total = round(total, 2)
        set_user_total(chat_id, total)
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid input. Please provide a numerical value.")
        return

    # Reply to the user with the updated total
    await update.message.reply_text(f"Total: {total}")


async def subtract(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract the numerical value from the user's message
    chat_id = update.message.chat_id
    try:
        total = float(get_user_total(chat_id))
        value = float(context.args[0])
        total -= value
        total = round(total, 2)
        set_user_total(chat_id, total)
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid input. Please provide a numerical value.")
        return

    # Reply to the user with the updated total
    await update.message.reply_text(f"Total: {total}")


async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract the numerical value from the user's message
    chat_id = update.message.chat_id
    try:
        total = float(0)
        set_user_total(chat_id, total)
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid input. Please provide a numerical value.")
        return

    # Reply to the user with the updated total
    await update.message.reply_text(f"Total: {total}")

def set_user_total(user_id, total):
    ref = db.reference('/users')
    ref.child(str(user_id)).set(total)

# Function to return the value for a given user ID
def get_user_total(user_id):
    ref = db.reference('/users')
    user_ref = ref.child(str(user_id))

    if user_ref.get() is None:
        return 0  # Return 0 if the user reference does not exist
    else:
        return user_ref.get()



async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Available commands:\n"
        "/hello - Say hello\n"
        "/add <value> - Add a numerical value to the total\n"
        "/sub <value> - Subtract a numerical value from the total\n"
        "/paid - Reset the total to zero\n"
    )


app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("sub", subtract))
app.add_handler(CommandHandler("paid", paid))
app.add_handler(CommandHandler("help", help))

app.run_polling()
