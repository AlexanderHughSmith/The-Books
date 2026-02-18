# The Books - Telegram Bot for Expense Tracking

A simple Telegram bot for tracking expenses using Firebase Realtime Database.

## Commands
- `/add <value>` - Add a value to your expense total
- `/sub <value>` - Subtract a value from your expense total
- `/paid` - Reset your total to zero
- `/hello` - Say hello
- `/help` - Show available commands

## Setup

### Local Development
1. Clone the repository
2. Create a `.env` file (copy from `.env.example`):
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   FIREBASE_DB_URL=your_firebase_db_url
   FIREBASE_CREDENTIALS_JSON={"type":"service_account",...}
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```
   python Ledger.py
   ```

### Deployment to Railway

1. Create a new project on Railway and connect this repository.
2. Add these Railway variables in your service settings:
   - `TELEGRAM_BOT_TOKEN`
   - `FIREBASE_DB_URL`
   - `FIREBASE_CREDENTIALS_JSON` (paste the full Firebase service account JSON as a single-line JSON string)
3. Deploy. Railway will install from `requirements.txt` and start the bot with:
   ```
   python Ledger.py
   ```

## Environment Variables
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token from @BotFather
- `FIREBASE_DB_URL` - Your Firebase Realtime Database URL
- `FIREBASE_CREDENTIALS_JSON` - Firebase service account JSON content

## Notes
- Sensitive credentials are managed via environment variables and never committed to git
- This project is configured to run on Railway as a worker process
- Firebase handles all data persistence
