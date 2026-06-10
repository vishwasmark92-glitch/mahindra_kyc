# Telegram Bot KYC - Fix Guide

## Issue Fixed
**Error**: "409 Conflict: can't use getUpdates method while webhook is active; use deleteWebhook to delete the webhook first"

This occurred because the bot was trying to use polling mode while a webhook was already registered with Telegram.

## Solution Implemented

### 1. **bot.py** - Main Application
- ✅ Automatically deletes webhook before starting
- ✅ Uses **webhook mode for production** (Railway, etc.)
- ✅ Uses **polling mode for development** (local testing)
- ✅ Includes Flask routes for `/webhook`, `/get_commands`, `/admin/get_data`
- ✅ Health check endpoint at `/health`

### 2. **requirements.txt** - Dependencies
- `telebot==4.14.0` - Telegram bot library
- `Flask==3.0.0` - Web framework
- `gunicorn==21.2.0` - Production WSGI server

### 3. **Dockerfile** - Container Configuration
- Python 3.11 slim image
- Automatic health checks
- Gunicorn with 1 worker (to avoid conflicts)
- Exposes port 5000

### 4. **.env.example** - Configuration Template
Copy to `.env` and fill in your values

## Railway Deployment Steps

1. **Set Environment Variables in Railway**:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   WEBHOOK_URL=https://your-railway-domain.up.railway.app
   ENVIRONMENT=production
   PORT=5000
   ```

2. **Connect GitHub Repository**:
   - Go to Railway → New Project
   - Deploy from GitHub
   - Select this repository

3. **The app will automatically**:
   - Install dependencies from `requirements.txt`
   - Build Docker image from `Dockerfile`
   - Start the Flask app with gunicorn
   - Register webhook with Telegram

## How It Works

### Production Mode (Railway)
```
Bot receives updates → Telegram calls /webhook endpoint → Bot processes update
```

### Development Mode (Local)
```
Bot continuously polls Telegram for updates
```

## Testing Locally

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Set ENVIRONMENT=development in .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the bot
python bot.py
```

## Troubleshooting

If you still get 409 errors:
1. Make sure `ENVIRONMENT=production` is set on Railway
2. Verify `WEBHOOK_URL` is correct (get it from Railway dashboard)
3. Check bot logs: `railway logs`
4. Manually delete webhook: `bot.delete_webhook()` before restart

## Files Added/Modified

- ✅ `bot.py` - Complete bot with webhook/polling support
- ✅ `requirements.txt` - Python dependencies
- ✅ `Dockerfile` - Container image definition
- ✅ `.env.example` - Configuration template
- ✅ `README.md` - This file
