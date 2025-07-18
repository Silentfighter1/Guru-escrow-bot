from pyrogram import Client, filters from pyrogram.types import Message import datetime

API_ID = 26980796 API_HASH = "b216adeeef4c0951d0d710081a550e2f" BOT_TOKEN = "7756177830:AAE7y8w7W5ntfw7ixY64s6vzvVmWBbdaYYE"

LOG_CHANNEL = -1002693806027 ADMIN_IDS = [6389122186]

app = Client("guru_escrow_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_form_details(text): lines = text.splitlines() data = {} for line in lines: if "Bᴜʏᴇʀ:" in line: data['buyer'] = line.split("Bᴜʏᴇʀ:")[1].strip() elif "Sᴇʟʟᴇʀ:" in line: data['seller'] = line.split("Sᴇʟʟᴇʀ:")[1].strip() elif "Aᴍᴏᴜɴᴛ:" in line: data['amount'] = line.split("Aᴍᴏᴜɴᴛ:")[1].strip() elif "Dᴇᴀʟ Dᴇᴛᴀɪʟs:" in line: data['info'] = line.split("Dᴇᴀʟ Dᴇᴛᴀɪʟs:")[1].strip() return data

def log_deal(text): today = datetime.datetime.now().strftime("%Y-%m-%d") filename = f"deals_{today}.txt" with open(filename, "a") as file: file.write(text + "\n\n") return filename

@app.on_message(filters.command(["add", "close", "refund", "stats"]) & filters.reply) def handle_command(client, message: Message): if message.from_user.id not in ADMIN_IDS: message.reply("🚫 You are not authorized to use this command.") return

replied = message.reply_to_message
if not replied or not replied.text:
    message.reply("❌ Please reply to a valid form message.")
    return

data = extract_form_details(replied.text)
if not all(k in data for k in ("buyer", "seller", "amount")):
    message.reply("⚠️ Could not extract full form details.")
    return

trade_id = f"TXN_{datetime.datetime.now().strftime('%H%M%S')}"
admin_name = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

if message.text.startswith("/add"):
    text = f"📤 *Payment Received*

🆔 Trade ID : {trade_id} 💰 Amount : {data['amount']} 👤 Buyer : {data['buyer']} 👤 Seller : {data['seller']} 📝 DEAL INFO : {data.get('info', 'N/A')}

Escrow by {admin_name}" elif message.text.startswith("/close"): text = f"♻️ Deal Completed

📤 Trade ID : {trade_id} ✔️ Released Amount : {data['amount']} 👤 Buyer : {data['buyer']} 👤 Seller : {data['seller']}

Pw By @GuruxEscrow\nEscrower ~ {admin_name}" elif message.text.startswith("/refund"): text = f"↩️ Deal Refunded

📤 Trade ID : {trade_id} 💸 Refunded Amount : {data['amount']} 👤 Buyer : {data['buyer']} 👤 Seller : {data['seller']}

Escrower ~ {admin_name}" elif message.text.startswith("/stats"): today = datetime.datetime.now().strftime("%Y-%m-%d") try: with open(f"deals_{today}.txt", "r") as file: log_text = file.read() message.reply_document(f"deals_{today}.txt", caption=f"📊 Deals for {today}", quote=True) except FileNotFoundError: message.reply("No deals found for today.") return

message.reply(text, quote=True)
log_file = log_deal(text)
client.send_message(LOG_CHANNEL, text)

app.run()

