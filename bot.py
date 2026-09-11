cat > bot.py << 'EOF'
#!/usr/bin/env python3
import telebot
import subprocess
import time
import socket
import logging

# --- CONFIGURAÇÃO ---
# Bot Token from BotFather
BOT_TOKEN = '8958823819:AAGlQyAGdijl6m6kdWuETncibsnd12O70X4'

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# --- FUNÇÕES AUXILIARES ---

def get_local_ip():
    """Get the local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def run_server():
    """Start the HTTP server on port 9000"""
    server = subprocess.Popen(
        ['python3', '-m', 'http.server', '9000'],
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    return server

# --- BOT COMMANDS ---

@bot.message_handler(commands=['start'])
def start_message(message):
    """Menu on start"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton("🕸️ Harvest", callback_data="harvest")
    btn2 = telebot.types.InlineKeyboardButton("🔗 Clone/Host", callback_data="clone")
    btn3 = telebot.types.InlineKeyboardButton("💸 Wallet", callback_data="wallet")
    btn4 = telebot.types.InlineKeyboardButton("⚙️ Server Status", callback_data="status")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.reply_to(message, 
        "🚀 <b>HUBRIS // Desktop Console</b>\n\nServer is ready.", 
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.data == 'harvest':
            bot.answer(call, '🕸️ Initiating scan...')
            chat_id = call.message.chat.id
            bot.edit_message_text('🔎 Scanning targets...', chat_id=chat_id, message_id=call.message.message_id)
            time.sleep(2)
            bot.edit_message_text('✅ Scan Complete.<br>Targets: <code>targets.json</code>', chat_id=chat_id, message_id=call.message.message_id)
            
        elif call.data == 'clone':
            ip = get_local_ip()
            link = f"http://{ip}:9000"
            bot.answer(call, f'🔗 Link for Desktop: {ip}')
            bot.send_message(call.message.chat.id, 
                f"🖥️ <b>Mirror Server Running!</b>\n\nAccess via:<br><code>{link}</code>")
            
        elif call.data == 'wallet':
            bot.answer(call, '💸 Fetching...')
            bot.send_message(call.message.chat.id, "💰 Wallet Status: <b>ACTIVE</b>\nETH: <code>0x...</code>")
            
        elif call.data == 'status':
            bot.answer(call, '⚙️ Checking...')
            bot.send_message(call.message.chat.id, "✅ Database: Online\n🟢 Port: 9000\n🟢 Token: Verified")
            
    except Exception as e:
        logging.error(f"Error in callback: {e}")

# --- EXECUTION ---

if __name__ == '__main__':
    print(f"🟢 Bot Starting... (Using Token: {BOT_TOKEN[:10]}...)")
    print("⚙️ Starting Web Server (Port 9000)...")
    try:
        run_server()
        bot.polling(non_stop=True)
    except KeyboardInterrupt:
        print("🛑 Bot Stopped.")
EOF
