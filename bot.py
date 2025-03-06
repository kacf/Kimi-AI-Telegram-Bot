
import os
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import json

# Configuration (replace with your actual keys)
API_ID = 26788480  # Get from https://my.telegram.org
API_HASH = "858d65155253af8632221240c535c314"  # Get from https://my.telegram.org
BOT_TOKEN = "7224277474:AAGyhCxdvKzNpe2sgDLwtks4015eZcMIohQ"  # Get from @BotFather
MOONSHOT_API_KEY = "sk-7JqUhqmM5qPFXKgBDmIfJpeUJNcq4pDnsr09OkZXKsZnAVbc"  # Get from Moonshot AI

# Initialize Pyrogram client
app = Client(
    "moonshot_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def query_moonshot(prompt: str) -> str:
    """Send prompt to Moonshot API and return response"""
    url = "https://api.moonshot.cn/v1/chat/completions"  # Check Moonshot's actual API endpoint
    
    headers = {
        "Authorization": f"Bearer {MOONSHOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "moonshot-v1-8k",  # Adjust based on available models
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error processing request: {str(e)}"

# Message handler for private chats
@app.on_message(filters.private & filters.text)
async def private_chat_handler(client: Client, message: Message):
    await message.reply_chat_action("typing")
    response = query_moonshot(message.text)
    await message.reply_text(response)

# Message handler for group mentions
@app.on_message(filters.group & filters.text & filters.regex(r"@your_bot_username"))
async def group_mention_handler(client: Client, message: Message):
    await message.reply_chat_action("typing")
    # Remove the bot mention from the message
    prompt = message.text.replace("@your_bot_username", "").strip()
    response = query_moonshot(prompt)
    await message.reply_text(response, reply_to_message_id=message.id)

# Start the bot
print("Bot is running...")
app.run()
