import os
import hashlib
import random
import string
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SERVER KEEP-ALIVE ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "TOOL MD5 TXGAME v13.0 ZENITH CORE ONLINE", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CẤU HÌNH HỆ THỐNG ---
TOKEN = '8985526419:AAGdRkntgFNYLBG53LoI-pNC7aHtOFMWhGA'
ADMIN_ID = 755092812
ADMIN_USERNAME = "lionvnios"

bot = telebot.TeleBot(TOKEN)
user_data = {}
all_users = set()
GLOBAL_CACHE = {}
gift_codes = {}

def is_admin(user):
    if not user: return False
    if user.id == ADMIN_ID: return True
    if user.username and user.username.lower() == ADMIN_USERNAME.lower(): return True
    return False

def init_user(uid):
    all_users.add(uid)
    if uid not in user_data:
        user_data[uid] = {"balance": 20, "web": "HitClub", "logs": []}

# --- 3. THUẬT TOÁN ĐỈNH CAO: TỔNG HẠT NHÂN (SUMMATION PARITY) ---
def zenith_algo(raw_code):
    clean_code = raw_code.strip().lower()
    
    if clean_code in GLOBAL_CACHE:
        return GLOBAL_CACHE[clean_code]

    # Phân rã chuỗi và tính tổng thập phân của toàn bộ ký tự
    # Đảm bảo tỷ lệ cân bằng tuyệt đối 50/50 theo lý thuyết chẵn/lẻ
    total_val = sum(int(char, 16) for char in hashlib.sha256(clean_code.encode()).hexdigest())

    is_tai = (total_val % 2 == 0)
    result = "TÀI" if is_tai else "XỈU"

    # Chỉ số hiển thị: Tỷ lệ mô phỏng (từ 50.1% đến 99.9%) và Độ trễ
    display_percent = 50.1 + (total_val % 498) / 10.0
    latency = round(0.001 + (total_val % 15) / 1000.0, 3)

    res_tuple = (result, round(display_percent, 1), latency)
    GLOBAL_CACHE[clean_code] = res_tuple
    return res_tuple

# --- 4. GIAO DIỆN CHÍNH THU GỌN ---
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⚙️ Cổng Game", callback_data="btn_web"),
        InlineKeyboardButton("🎁 Nhập Code", callback_data="btn_redeem")
    )
    markup.add(
        InlineKeyboardButton("💳 Ví & Lịch sử", callback_data="btn_info"),
        InlineKeyboardButton("💎 Liên hệ", callback_data="btn_nap")
    )
    return markup

# --- 5. LỆNH CƠ BẢN ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        text = (
            "⚡ **MD5 TX ZENITH v13.0**\n"
            f"🆔 `{uid}` | 💳 `{user_data[uid]['balance']}` lượt\n\n"
            "👉 **Dán mã MD5/SHA256 vào đây:**"
        )
        bot.reply_to(message, text, parse_mode="Markdown", reply_markup=main_menu())
    except:
        pass

@bot.message_handler(commands=['napcode'])
def redeem_code_cmd(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        parts = message.text.split()
        if len(parts) < 2: return
        code_input = parts[1].strip().upper()
        if code_input in gift_codes:
            amount = gift_codes.pop(code_input)
            user_data[uid]["balance"] += amount
            bot.reply_to(message, f"✅ **Nạp thành công!**\n🎁 MÃ: `{code_input}` (+{amount})\n💳 Dư: `{user_data[uid]['balance']}`", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ **Mã không hợp lệ!**")
    except:
        pass

# --- 6. ADMIN ĐIỀU KHIỂN ---
@bot.message_handler(commands=['taocode'])
def generate_code_cmd(message):
    try:
        if not is_admin(message.from_user): return
        parts = message.text.split()
        if len(parts) < 2: return
        amount = int(parts[1])
        count = int(parts[2]) if len(parts) >= 3 else 1
        created_codes = []
        for _ in range(count):
            code = f"VIP-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
            gift_codes[code] = amount
            created_codes.append(f"`{code}`")
        bot.reply_to(message, f"✅ **Tạo Code:**\n" + "\n".join(created_codes), parse_mode="Markdown")
    except:
        pass

@bot.message_handler(commands=['congxu'])
def add_coins(message):
    try:
        if not is_admin(message.from_user): return
        parts = message.text.split()
        if len(parts) != 3: return
        target_id, amount = int(parts[1]), int(parts[2])
        init_user(target_id)
        user_data[target_id]["balance"] += amount
        bot.reply_to(message, f"✅ Đã cộng `{amount}` cho `{target_id}`.", parse_mode="Markdown")
    except:
        pass

# --- 7. TƯƠNG TÁC GIAO DIỆN ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        uid = call.from_user.id
        init_user(uid)
        if call.data == "btn_web":
            markup = InlineKeyboardMarkup(row_width=3)
            games = ["HitClub", "B52", "Lucky88", "LC79", "Go88", "RikVIP"]
            btns = [InlineKeyboardButton(w, callback_data=f"web_{w}") for w in games]
            markup.add(*btns)
            bot.send_message(call.message.chat.id, "🌐 **Chọn máy chủ:**", parse_mode="Markdown", reply_markup=markup)
        elif call.data.startswith("web_"):
            web = call.data.split("_")[1]
            user_data[uid]["web"] = web
            bot.send_message(call.message.chat.id, f"✅ Đã kết nối: `{web}`", parse_mode="Markdown", reply_markup=main_menu())
        elif call.data == "btn_info":
            logs_str = "\n".join(user_data[uid]["logs"]) if user_data[uid]["logs"] else "Trống."
            bot.send_message(call.message.chat.id, f"💳 **ID:** `{uid}` | Dư: `{user_data[uid]['balance']}`\n📜 **Lịch sử:**\n{logs_str}", parse_mode="Markdown", reply_markup=main_menu())
        elif call.data == "btn_redeem":
            bot.send_message(call.message.chat.id, "👉 **Cách nạp:** Gõ `/napcode [Mã]`", parse_mode="Markdown")
        elif call.data == "btn_nap":
            bot.send_message(call.message.chat.id, f"💎 Gửi ID `{uid}` cho Admin @lionVnIos", parse_mode="Markdown")
    except:
        pass

# --- 8. PHÂN TÍCH TỐI GIẢN ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        text = message.text.strip().lower()
        
        if len(text) not in [32, 64]: return
        if user_data[uid]["balance"] < 1:
            bot.reply_to(message, "⚠️ Hết lượt. Vui lòng nạp thêm.", reply_markup=main_menu())
            return
            
        user_data[uid]["balance"] -= 1
        result, percent, latency = zenith_algo(text)
        
        res_icon = "🔴 TÀI" if result == "TÀI" else "🔵 XỈU"
        short_code = f"{text[:6]}...{text[-4:]}"
        
        user_data[uid]["logs"].insert(0, f"[{short_code}] ➔ {result}")
        if len(user_data[uid]["logs"]) > 3: user_data[uid]["logs"].pop()
            
        # Giao diện siêu thu gọn
        res_msg = (
            f"🖩 MD5: `{short_code}`\n"
            f"🎯 Kết quả: **{res_icon}** ({percent}%)\n"
            f"⚡ {user_data[uid]['web']} | ⏱ `{latency}s` | 💳 `{user_data[uid]['balance']}`"
        )
        bot.reply_to(message, res_msg, parse_mode="Markdown", reply_markup=main_menu())
    except:
        pass

if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    try:
        bot.remove_webhook()
    except:
        pass
    print("TOOL MD5 v13.0 ACTIVE...")
    bot.infinity_polling(none_stop=True)
