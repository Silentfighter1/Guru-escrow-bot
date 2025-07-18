from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID, LOG_CHANNEL

app = Client("guru_escrow_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Only Admin Filter
admin_filter = filters.user(ADMIN_ID)

# /start Command
@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply("🤖 Guru Escrow Bot is Active!")

# /add Command
@app.on_message(filters.command("add") & admin_filter)
async def add_deal(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("🔁 Is form message ko reply karke `/add` use karo.")
    form = message.reply_to_message.text
    await message.reply(f"✅ Deal Received:\n\n{form}")
    await app.send_message(LOG_CHANNEL, f"📥 New Deal Added:\n\n{form}")

# /close Command
@app.on_message(filters.command("close") & admin_filter)
async def close_deal(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("🔁 Is form message ko reply karke `/close` use karo.")
    form = message.reply_to_message.text
    await message.reply("✅ Deal Completed Successfully!")
    await app.send_message(LOG_CHANNEL, f"✅ DEAL COMPLETED:\n\n{form}")

# /refund Command
@app.on_message(filters.command("refund") & admin_filter)
async def refund(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("🔁 Is form message ko reply karke `/refund` use karo.")
    form = message.reply_to_message.text
    await message.reply("❌ Refund Issued Successfully!")
    await app.send_message(LOG_CHANNEL, f"❌ REFUND ISSUED:\n\n{form}")

# /stats Command
@app.on_message(filters.command("stats") & admin_filter)
async def stats(_, message: Message):
    await message.reply("📊 Guru Escrow Stats:\n\n✅ Total Deals: Live Count Not Implemented")

app.run()
