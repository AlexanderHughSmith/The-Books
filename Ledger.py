from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import ast
import operator
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Load Firebase credentials from JSON string in environment variable
firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if not firebase_creds_json:
    raise RuntimeError("Missing FIREBASE_CREDENTIALS_JSON environment variable.")

cred = credentials.Certificate(json.loads(firebase_creds_json))
firebase_admin.initialize_app(cred, {'databaseURL': os.getenv("FIREBASE_DB_URL")})

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def parse_amount(text: str) -> float:
    """Parse a plain number or a simple math expression (e.g. 10/2)."""
    text = text.strip()
    try:
        return float(text)
    except ValueError:
        pass

    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid amount: {text}") from exc

    return _eval_ast(tree.body)


def _eval_ast(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Invalid number in expression")
    if isinstance(node, ast.BinOp):
        op = _BINOPS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator")
        return op(_eval_ast(node.left), _eval_ast(node.right))
    if isinstance(node, ast.UnaryOp):
        op = _UNARYOPS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator")
        return float(op(_eval_ast(node.operand)))
    raise ValueError("Invalid expression")


def ledger_key(update: Update) -> str:
    """Firebase key: one ledger per chat, or per forum topic when in a thread."""
    chat_id = update.effective_chat.id
    msg = update.effective_message
    thread_id = msg.message_thread_id if msg else None
    if thread_id is not None:
        return f"{chat_id}_{thread_id}"
    return str(chat_id)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key = ledger_key(update)
    try:
        total = float(get_user_total(key))
        value = parse_amount(context.args[0])
        total += value
        total = round(total, 2)
        set_user_total(key, total)
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Invalid input. Use a number or expression (e.g. /add 10/2 food)."
        )
        return

    # Reply to the user with the updated total
    await update.message.reply_text(f"Total: {total}")


async def subtract(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key = ledger_key(update)
    try:
        total = float(get_user_total(key))
        value = parse_amount(context.args[0])
        total -= value
        total = round(total, 2)
        set_user_total(key, total)
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Invalid input. Use a number or expression (e.g. /sub 10/2 food)."
        )
        return

    # Reply to the user with the updated total
    await update.message.reply_text(f"Total: {total}")


async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key = ledger_key(update)
    try:
        total = float(0)
        set_user_total(key, total)
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
        "/add <value> [label] - Add a number or expression (e.g. /add 10/2 food)\n"
        "/sub <value> [label] - Subtract a number or expression\n"
        "/paid - Reset the total to zero\n"
    )


app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("sub", subtract))
app.add_handler(CommandHandler("paid", paid))
app.add_handler(CommandHandler("help", help))

app.run_polling()
