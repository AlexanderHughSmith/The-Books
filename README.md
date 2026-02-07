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
   GOOGLE_APPLICATION_CREDENTIALS=path/to/firebase-adminsdk.json
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```
   python Ledger.py
   ```

### Deployment to Fly.io

1. Install `flyctl`: https://fly.io/docs/hands-on/install-flyctl/
2. Login:
   ```
   flyctl auth login
   ```
3. Create the app (first time only):
   ```
   flyctl launch
   ```
4. Set secrets:
   ```
   flyctl secrets set TELEGRAM_BOT_TOKEN=your_token
   flyctl secrets set FIREBASE_DB_URL=your_url
   flyctl secrets set GOOGLE_APPLICATION_CREDENTIALS=/app/firebase-key.json
   ```
5. Deploy:
   ```
   flyctl deploy
   ```

## Environment Variables
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token from @BotFather
- `FIREBASE_DB_URL` - Your Firebase Realtime Database URL
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Firebase service account JSON file

## Notes
- Sensitive credentials are managed via environment variables and never committed to git
- The bot runs 24/7 on Fly.io free tier
- Firebase handles all data persistence
