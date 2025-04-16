# main.py

import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BLOG_URL = os.environ.get("BLOG_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Type /movie <name> to get download link.")

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("❗ Please enter a movie name. Example: /movie Animal")
        return

    search_url = f"{BLOG_URL}/search?q={query.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    post = soup.find('h3', class_='post-title')
    if not post:
        await update.message.reply_text("❌ Movie not found.")
        return

    title = post.text.strip()
    link = post.find('a')['href']

    await update.message.reply_text(
        f"🎬 *{title}*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📥 Download Now", url=link)]
        ])
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movie", movie))
app.run_polling()
