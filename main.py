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
Mujhe apne Channel\n ya Group me add karo 🤩

Phir kahi, Kuch Bhi forward karo ⏩
Sab kuch Hata dunga aap chaho toh aapka bhi laga dunga

Mentions
Usernames
@
link
t.me
sab kuch ⚡

Mere se jayda powerful\n Caption wala bot nahi dekha hoga 100% 

Brained by @ideafy"""

about_message = """  
<b>• Name : [GodMode Yedekho V1](t.me/{username})</b>

<b>• Developer : [Ideafy](https://t.me/ideafy) 

<b>• Language : apna kam karo

<b>• Library : apna kam karo</b>  

<b>• Updates : <a href=https://t.me/yedekho>⚡⚡MAGIC⚡⚡</a></b>"""


@AutoCaptionBot.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
  update.reply(start_message.format(update.from_user.mention), reply_markup=start_buttons(bot, update), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("start"))
def start_callback(bot, update):
  update.message.edit(start_message.format(update.from_user.mention), reply_markup=start_buttons(bot, update.message), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
  
@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
  bot = bot.get_me()
  update.message.edit(about_message.format(version=pyrogram.__version__, username=bot.username), reply_markup=about_buttons(bot, update.message), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)


@AutoCaptionBot.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):

  caption = update.caption
  if caption:
    caption = re.sub(r"@\w+\b|http\S+\b|www.\S+\b|t.me/\S+\b", "", caption, flags=re.IGNORECASE) 
    caption = re.sub(r"join", "", caption, flags=re.IGNORECASE)

  if os.environ.get("custom_caption"):
    motech, _ = get_file_details(update)

    try:
      update.edit_caption(caption + "\n" + custom_caption.format(file_name=motech.file_name))

    except pyrogram.errors.FloodWait as e:
      asyncio.sleep(e.x)  
      update.edit_caption(caption + "\n" + custom_caption.format(file_name=motech.file_name, mote=motech.mot))

  else:
    return
    

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
