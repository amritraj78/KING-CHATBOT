import requests
import random
from MukeshAPI import api
from pyrogram import filters, Client
from pyrogram.enums import ChatAction
from nexichat import nexichat as app

def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice([
            "Love is in the air but needs a little spark.",
            "A good start but there's room to grow.",
            "It's just the beginning of something beautiful."
        ])
    elif love_percentage <= 70:
        return random.choice([
            "A strong connection is there. Keep nurturing it.",
            "You've got a good chance. Work on it.",
            "Love is blossoming, keep going."
        ])
    else:
        return random.choice([
            "Wow! It's a match made in heaven!",
            "Perfect match! Cherish this bond.",
            "Destined to be together. Congratulations!"
        ])

@app.on_message(filters.command("love", prefixes="/"))
async def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()
        
        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = f"{name1}💕 + {name2}💕 = {love_percentage}%\n\n{love_message}"
    else:
        response = "Please enter two names after /love command."
    await client.send_message(message.chat.id, response)

@app.on_message(filters.command(["gemini", "ai", "ask", "chatgpt"]))
async def gemini_handler(client, message):
    if (
        message.text.startswith(f"/gemini@{client.me.username}")
        and len(message.text.split(" ", 1)) > 1
    ):
        user_input = message.text.split(" ", 1)[1]
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await message.reply_text("Example :- `/ask who is Narendra Modi`")
            return

    try:
        response = api.gemini(user_input)
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        result = response.get("results")
        if result:
            await message.reply_text(result, quote=True)
            return
    except:
        pass  
    
    try:
        base_url = "https://chatwithai.codesearch.workers.dev/?chat="
        response = requests.get(base_url + user_input)
        if response and response.text.strip():
            await message.reply_text(response.text.strip(), quote=True)
        else:
            await message.reply_text("**Both Gemini and Chat with AI are currently unavailable**")
    except:
        await message.reply_text("**Chatgpt is currently dead. Try again later.**")
