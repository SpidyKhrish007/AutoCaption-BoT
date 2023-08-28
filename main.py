import pyrogram
import os 
import asyncio
import re

try:
  app_id = int(os.environ.get("app_id", None)) 
except Exception as e:
  print(f"⚠️ App ID Invalid {e}")

try:
  api_hash = os.environ.get("api_hash", None)  
except Exception as e:
  print(f"⚠️ Api Hash Invalid {e}")

try:
  bot_token = os.environ.get("bot_token", None)
except Exception as e:
  print(f"⚠️ Bot Token Invalid {e}")
  
try:
  custom_caption = os.environ.get("custom_caption", "`{file_name}`") 
except Exception as e:
  print(f"⚠️ Custom Caption Invalid {e}")

AutoCaptionBot = pyrogram.Client(
    name="AutoCaptionBot", 
    api_id=app_id, 
    api_hash=api_hash,
    bot_token=bot_token
)

start_message = """
<b>❤️ Kaha the aap 🥲 {}</b> 

<i>Mai kya kya kar sakta hu 👇🏻</i>
Mujhe apne Channel me add karo 🤩
Kuch Bhi forward karo, <b>I WILL REMOVE<b/> 👇🏻🙅
<code>Mentions
Usernames
@
link
t.me</code>

I have superpowers 🏋️
Brained by @ideafy"""

about_message = """  
<b>• Name : [GodMode Yedekho V1]</b>

<b>• Developer : [@Ideafy]

<b>• Updates : <a href=https://t.me/yedekho>⚡⚡MAGIC⚡⚡</a></b>"""

@AutoCaptionBot.on_message(pyrogram.filters.private & pyrogram.filters.command("start"))
def start_command(bot, message):
   message.reply("Hi I'm Auto Caption Bot!")
   
@AutoCaptionBot.on_message(pyrogram.filters.private & pyrogram.filters.command("caption"))
def set_caption(bot, message):
  
  user_id = message.from_user.id
  custom_caption = message.text.split(maxsplit=1)[1]
  
  custom_captions[user_id] = custom_caption
  
  message.reply("Your custom caption has been saved!")
  
# Core caption edit logic

@AutoCaptionBot.on_message(pyrogram.filters.channel)
def edit_caption(bot, message):

  try:
    caption = message.caption
    caption = re.sub(r"@\w+\b|http\S+\b", "", caption, flags=re.IGNORECASE) 
    
    if message.from_user.id in custom_captions:
      custom = custom_captions[message.from_user.id]
      caption += "\n\n" + custom
      
    message.edit_caption(caption)
    
  except Exception as e:
    print(e)

def get_file_details(update: pyrogram.types.Message):
  if update.media:
    for message_type in (
      "photo",
      "animation",
      "audio",
      "document",
      "video",
      "video_note",
      "voice",
      "sticker"
    ):
      obj = getattr(update, message_type)
      if obj:
        return obj, obj.file_id

def start_buttons(bot, update):
  bot = bot.get_me()
  buttons = [
    [
      pyrogram.types.InlineKeyboardButton("Updats", url="https://t.me/yedekho_in"),
      pyrogram.types.InlineKeyboardButton("Inside Info ℹ️", callback_data="about") 
    ],
    [
      pyrogram.types.InlineKeyboardButton("Experience The magic ✨", url=f"http://t.me/{bot.username}?startchannel=true")
    ]
  ]
  return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
  buttons = [
    [
      pyrogram.types.InlineKeyboardButton("⏩ Home", callback_data="start")
    ]
  ]
  return pyrogram.types.InlineKeyboardMarkup(buttons)


print("AutoCaption Bot Started")
AutoCaptionBot.run()
