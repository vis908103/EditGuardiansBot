# yazılımı aynı @EditGuardiansBot botu gibi yapmaya çalıştım benzemistir ins
import os
import logging 
from telethon import TelegramClient, events, Button
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BOT_TOKEN = "8081003333:AAFYXlsgCJWnNnt5vKLBxHkIVAiad5c4zOU"
MONGO_URI = "eg3skk3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
OWNER_ID = 1008989961
LOGGER_GROUP_ID = -4825904819

API_ID = 23480691
API_HASH = "519068128f1f5767dfeb224c15d23949"

bot = TelegramClient('anon', API_ID, API_HASH)

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.editguardian
users_collection = db["users"]
groups_collection = db["groups"]


async def add_user(user_id):
    if not await users_collection.find_one({"user_id": user_id}):
        await users_collection.insert_one({"user_id": user_id})

async def add_group(group_id):
    if not await groups_collection.find_one({"group_id": group_id}):
        await groups_collection.insert_one({"group_id": group_id}) 

async def remove_group(group_id):
    if await groups_collection.find_one({"group_id": group_id}):
        await groups_collection.delete_one({"group_id": group_id})

async def get_all_users():
    users = []
    async for user in users_collection.find():
        try:
            users.append(user["user_id"])
        except Exception:
            pass
    return users
    
async def get_all_groups():
    group = []
    async for chat in groups_collection.find():
        try:
            group.append(chat["group_id"])
        except Exception:
            pass
    return group    

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.send_message(LOGGER_GROUP_ID, "bot aktif")
    await bot.run_until_disconnected()

@bot.on(events.NewMessage(func = lambda e: len(e.text) > 800 and e.is_group, incoming=True))
async def delete_long_message(event):
    await event.delete()
    await event.respond("Mesajınız 800 karakterden fazla olduğu için silindi.")
    

@bot.on(events.NewMessage(func=lambda e: e.text.startswith("/start") and e.is_private, incoming=True))
async def handle_start(event):
    
    user_id = event.sender_id
    await add_user(user_id)
    user = await event.get_sender()
    photo = None
    async for p in bot.iter_profile_photos(user, limit=1):
        photo = await bot.download_media(p)
        break
        
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    message = (
        f"✨ *Kullanıcı Aktivite Kaydı*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *Kullanıcı ID:* `{user_id}`\n"
        f"🙋 *İsim:* {mention}\n"
        f"🔗 *Kullanıcı Adı:* {user.username if user.username else 'Kullanıcı adı yok'}\n"
        f"🔄 *Eylem:* Botu başlattı\n"
        f"⏰ *Zaman:* `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n"
        f"📡 *Bot Durumu:* Aktif\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💎 _Botumuza hoş geldiniz!_\n"
    )
    await bot.send_message(LOGGER_GROUP_ID, message, file=photo)

    start_text = (
        f"Merhaba {mention} 👋 I'm your 𝗘𝗱𝗶𝘁 𝗚𝘂𝗮𝗿𝗱𝗶𝗮𝗻 𝗕𝗼𝘁, here to maintain a secure environment for our discussions.\n\n"
       " 🚫 𝗘𝗱𝗶𝘁𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗗𝗲𝗹𝗲𝘁𝗶𝗼𝗻: 𝗜'𝗹𝗹 𝗿𝗲𝗺𝗼𝘃𝗲 𝗲𝗱𝗶𝘁𝗲𝗱 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝘁𝗼 𝗺𝗮𝗶𝗻𝘁𝗮𝗶𝗻 𝘁𝗿𝗮𝗻𝘀𝗽𝗮𝗿𝗲𝗻𝗰𝘆.*\n\n"
        "📣 𝗡𝗼𝘁𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻𝘀: 𝗬𝗼𝘂'𝗹𝗹 𝗯𝗲 𝗶𝗻𝗳𝗼𝗿𝗺𝗲𝗱 𝗲𝗮𝗰𝘁𝗶𝗺𝗲 𝘁𝗶𝗺𝗲 𝗮 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗶𝘀 𝗱𝗲𝗹𝗲𝘁𝗲𝗱.\n\n"
        🌟 𝗚𝗲𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱:* \n"
        "1. Add me to your group.\n"
        "2. I'll start protecting instantly.\n\n"
        "➡️ Click on 𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 to add me and keep our group safe!"
    )
    buttons = [
        [Button.url("𝐒ᴜᴘᴘᴏʀᴛ 𝐂ʜᴀɴɴᴇʟ", "t.me/anime_india_divi"),
         Button.url("𝐒ᴜᴘᴘᴏʀᴛ 𝐂ʜᴀᴛ", "https://t.me/anime_india_divine")],
        [Button.url("𝗔𝗱𝗱 𝗠𝗲 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽", "https://t.me/GuardianDivine_bot?startgroup=true")]
    ]
    await event.respond(start_text, buttons=buttons)
    

@bot.on(
    events.MessageEdited(func=lambda e: e.is_group, incoming=True)
)
async def on_message_edited(event):
    try:
        mention = f"[{event.sender.first_name}](tg://user?id={event.sender_id})"
        what_edited = "edited message"

        await event.delete()

        if event.message.text:
            what_edited = "edited text message"
        elif event.message.photo:
            what_edited = "edited photo"
        elif event.message.video:
            what_edited = "edited video"
        elif event.message.document:
            what_edited = "edited document"
        elif event.message.audio:
            what_edited = "edited audio file"
        elif event.message.video_note:
            what_edited = "edited video note"
        elif event.message.voice:
            what_edited = "edited voice message"
        elif event.message.sticker:
            what_edited = "edited sticker"

        reason = f"**⚠️ {mention}**, your message was deleted because it contained an **{what_edited}.**"
        buttons = [
    [Button.url("Update Channel", "https://t.me/Anime_ibdia_divi"),
     Button.url("Update Group", "https://t.me/Anime_india_divine")],
    [Button.url("Add Group", "https://t.me/GuardianDivineBot?start=start")]
    ]
        await event.reply(reason, buttons=buttons)
    except Exception:
        return

@bot.on(events.NewMessage(func=lambda e: e.text.startswith("/stats"), incoming=True))
async def handle_user_count(event):
    if event.sender_id == OWNER_ID:
        user_count = len(await get_all_users())
        group_count = len(await get_all_groups())
        await event.reply(f"Toplam kullanıcı sayısı: {user_count}\nToplam grup sayısı: {group_count}")
    else:
        await event.reply("Bu komutu kullanma yetkiniz yok.")
        

@bot.on(events.NewMessage(func=lambda e: e.text.startswith("/broadcast") and e.sender_id == OWNER_ID, incoming=True))
async def handle_broadcast(message):
    chat_ids = await get_all_users() + await get_all_groups()
    if event.is_reply:
        rmsg = await event.get_reply_message()
        for chat in chat_ids:
            try:
                await rmsg.forward_to(chat)
            except Exception:
                pass
    elif len(event.text.split()) >= 2:
        msg = event.text.replace("/broadcast", "")
        for chat in chat_ids:
            try:
                await bot.send_message(chat, msg, link_preview=False)
            except Exception:
                pass
    
    else:
        await event.reply("Bir mesaj verin veya bir mesaja yanıt vererek bunu yaymak için bir mesaj sağlarsanız.")
        

@bot.on(events.ChatAction(func=lambda e: e.user_kicked or e.user_added or e.user_left))
async def handle_bot_added_to_group(event):
    if users := await event.get_users():
        for user in users:
            if user.id == (await bot.get_me()).id:
                await add_group(event.chat_id) if event.user_added else await remove_group(event.chat_id)
                chat = await event.get_chat()
                action_emoji = "➕" if event.user_added else "➖"
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = (
                    f"✨ *Group Activity Diary*\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                    f"👥 *Grup ID:* `{event.chat_id}`\n"
                    f"🏷️ *Grup Name:* {chat.title}\n"
                    f"{action_emoji} *Eylem:* {'Eklendi' if event.user_added else 'Çıkartıldı'}\n"
                    f"⏰ *Time:* `{current_time}`\n"
                    f"📡 *Bot Status:* Aktif\n"
                    f"━━━━━━━━━━━━━━━━━━━\n"
                )
                await bot.send_message(LOGGER_GROUP_ID, message, link_preview=False)

                await event.reply(
                    f"""
**🤖 Beni {chat.title} grubuna eklediğiniz için teşekkürler! 🤖**

Grubunuzu daha güvenli ve verimli hale getirmek için buradayım!  
Özelliklerimi keşfetmek için aşağıdaki butona tıklayın.

**🌟 Özellikler:**
- Düzenlenen Mesajları Otomatik Silme
- Düzenlenen Medyaları Otomatik Silme
- Grup Güvenliği & İzleme

🚀 Hadi bu grubu birlikte harika yapalım!   
Yardım mı istiyorsunuz? Sadece sorun! 💬
""",
                    buttons=Button.url("Lütfen Beni Tıklayın", url="https://t.me/NsfwDrugsblockbot?start=start")
                )
                

if __name__ == "__main__":
    bot.loop.run_until_complete(main())
    
