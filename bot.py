import telebot
from telebot import types
import json
import os
from datetime import datetime
import requests

# Bot tokeni (o'zingizni bot tokeningizni kiriting)
BOT_TOKEN = "8326460288:AAGjU7OOrxH6ktDej5yhpcIGyt1h-Mo2jaQ"
bot = telebot.TeleBot(BOT_TOKEN)

# Admin ID
ADMIN_ID = 2138780687

# API ma'lumotlari
SMM_API_KEY = "b1c75de81f29e150b1f86aa0261d2eb2"
SMM_API_URL = "https://smmpanel.net/api/v2"  # SMMPanel.net API

# Karta ma'lumotlari
CARD_NUMBER = "4177 4901 5211 4726"
CARD_HOLDER = "ДИЁРБЕК М."

# Narxlar (qirgiz somida) - Yangilangan
PRICES = {
    "instagram": {
        "followers": {
            "name": "📊 Obunachi",
            "options": [
                {"quantity": 100, "price": 45, "service_id": 2342},
                {"quantity": 200, "price": 85, "service_id": 2342},
                {"quantity": 300, "price": 125, "service_id": 2342},
                {"quantity": 400, "price": 165, "service_id": 2342},
                {"quantity": 500, "price": 205, "service_id": 2342},
                {"quantity": 600, "price": 245, "service_id": 2342},
                {"quantity": 700, "price": 290, "service_id": 2342},
                {"quantity": 1000, "price": 355, "service_id": 2342}
            ]
        },
        "story_views": {
            "name": "👁 Hikoya ko'rishlar",
            "options": [
                {"quantity": 100, "price": 25, "service_id": 720},
                {"quantity": 200, "price": 35, "service_id": 720},
                {"quantity": 300, "price": 45, "service_id": 720},
                {"quantity": 400, "price": 55, "service_id": 720},
                {"quantity": 500, "price": 65, "service_id": 720},
                {"quantity": 600, "price": 75, "service_id": 720},
                {"quantity": 700, "price": 100, "service_id": 720},
                {"quantity": 1000, "price": 120, "service_id": 720}
            ]
        },
        "video_views": {
            "name": "▶️ Video ko'rishlar",
            "options": [
                {"quantity": 1000, "price": 19, "service_id": 2550}
            ]
        },
        "likes": {
            "name": "❤️ Layklar",
            "options": [
                {"quantity": 100, "price": 30, "service_id": 847},
                {"quantity": 200, "price": 40, "service_id": 847},
                {"quantity": 300, "price": 50, "service_id": 847},
                {"quantity": 400, "price": 60, "service_id": 847},
                {"quantity": 500, "price": 70, "service_id": 847},
                {"quantity": 600, "price": 80, "service_id": 847},
                {"quantity": 700, "price": 90, "service_id": 847},
                {"quantity": 1000, "price": 130, "service_id": 847}
            ]
        }
    },
    "tiktok": {
        "followers": {
            "name": "📊 Obunachi",
            "options": [
                {"quantity": 100, "price": 45, "service_id": 2516},
                {"quantity": 200, "price": 90, "service_id": 2516},
                {"quantity": 300, "price": 135, "service_id": 2516},
                {"quantity": 400, "price": 170, "service_id": 2516},
                {"quantity": 500, "price": 215, "service_id": 2516},
                {"quantity": 600, "price": 250, "service_id": 2516},
                {"quantity": 700, "price": 295, "service_id": 2516},
                {"quantity": 1000, "price": 355, "service_id": 2516}
            ]
        },
        "video_views": {
            "name": "▶️ Video ko'rishlar",
            "options": [
                {"quantity": 1000, "price": 19, "service_id": 3019}
            ]
        },
        "likes": {
            "name": "❤️ Layklar",
            "options": [
                {"quantity": 100, "price": 30, "service_id": 1794},
                {"quantity": 200, "price": 40, "service_id": 1794},
                {"quantity": 300, "price": 50, "service_id": 1794},
                {"quantity": 400, "price": 60, "service_id": 1794},
                {"quantity": 500, "price": 70, "service_id": 1794},
                {"quantity": 600, "price": 80, "service_id": 1794},
                {"quantity": 700, "price": 90, "service_id": 1794},
                {"quantity": 1000, "price": 120, "service_id": 1794}
            ]
        }
    },
    "telegram": {
        "members": {
            "name": "👥 Kanalga a'zolar",
            "options": [
                {"quantity": 100, "price": 45, "service_id": 1868},
                {"quantity": 200, "price": 55, "service_id": 1868},
                {"quantity": 300, "price": 65, "service_id": 1868},
                {"quantity": 400, "price": 75, "service_id": 1868},
                {"quantity": 500, "price": 85, "service_id": 1868},
                {"quantity": 600, "price": 95, "service_id": 1868},
                {"quantity": 700, "price": 105, "service_id": 1868},
                {"quantity": 1000, "price": 155, "service_id": 1868}
            ]
        },
        "views": {
            "name": "👁 Ko'rishlar",
            "options": [
                {"quantity": 1000, "price": 19, "service_id": 2308}
            ]
        }
    }
}

# Ma'lumotlar fayli
DATA_FILE = "bot_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": {}, "orders": [], "pending_payments": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_balance(user_id):
    data = load_data()
    return data["users"].get(str(user_id), {}).get("balance", 0)

def update_balance(user_id, amount):
    data = load_data()
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {"balance": 0, "orders": []}
    data["users"][str(user_id)]["balance"] += amount
    save_data(data)

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📸 Instagram", "🎵 TikTok")
    markup.row("✈️ Telegram", "💰 Balansim")
    markup.row("💳 Balans to'ldirish")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    data = load_data()
    
    if str(user_id) not in data["users"]:
        data["users"][str(user_id)] = {
            "balance": 0,
            "orders": [],
            "username": message.from_user.username,
            "first_name": message.from_user.first_name
        }
        save_data(data)
    
    bot.send_message(
        message.chat.id,
        f"👋 Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "🚀 SMM Nakrutka Botiga xush kelibsiz!\n\n"
        "📱 Instagram, TikTok va Telegram uchun nakrutka xizmatlari:\n"
        "• Obunachi, layklar\n"
        "• Ko'rishlar, hikoya ko'rishlar\n"
        "• Kanalga a'zolar va boshqalar\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=create_main_menu()
    )

@bot.message_handler(func=lambda message: message.text == "📸 Instagram")
def instagram_menu(message):
    markup = types.InlineKeyboardMarkup()
    for key, service in PRICES["instagram"].items():
        markup.add(types.InlineKeyboardButton(
            f"{service['name']}",
            callback_data=f"instagram_{key}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
    
    bot.send_message(
        message.chat.id,
        "📸 *Instagram nakrutka xizmatlari*\n\n"
        "Kerakli xizmatni tanlang:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🎵 TikTok")
def tiktok_menu(message):
    markup = types.InlineKeyboardMarkup()
    for key, service in PRICES["tiktok"].items():
        markup.add(types.InlineKeyboardButton(
            f"{service['name']}",
            callback_data=f"tiktok_{key}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
    
    bot.send_message(
        message.chat.id,
        "🎵 *TikTok nakrutka xizmatlari*\n\n"
        "Kerakli xizmatni tanlang:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "✈️ Telegram")
def telegram_menu(message):
    markup = types.InlineKeyboardMarkup()
    for key, service in PRICES["telegram"].items():
        markup.add(types.InlineKeyboardButton(
            f"{service['name']}",
            callback_data=f"telegram_{key}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
    
    bot.send_message(
        message.chat.id,
        "✈️ *Telegram nakrutka xizmatlari*\n\n"
        "Kerakli xizmatni tanlang:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "💰 Balansim")
def check_balance(message):
    balance = get_user_balance(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"💰 *Sizning balansiz:* {balance} som\n\n"
        "💳 Balansni to'ldirish uchun '💳 Balans to'ldirish' tugmasini bosing",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: message.text == "💳 Balans to'ldirish")
def add_balance(message):
    msg = bot.send_message(
        message.chat.id,
        "💰 *Balansni to'ldirish*\n\n"
        "Qancha summa to'ldirmoqchisiz?\n"
        "Summani kiriting (faqat raqam, so'mda):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_amount_input)

def process_amount_input(message):
    try:
        amount = int(message.text)
        if amount < 10:
            bot.send_message(
                message.chat.id,
                "❌ Minimal summa 10 som!\n\n"
                "Qaytadan kiriting:",
                reply_markup=create_main_menu()
            )
            return
        
        # Ma'lumotni vaqtincha saqlash
        bot.send_message(
            message.chat.id,
            f"💳 *To'lov ma'lumotlari*\n\n"
            f"💰 Summa: {amount} som\n\n"
            f"📱 Karta raqami: `{CARD_NUMBER}`\n"
            f"👤 Karta egasi: {CARD_HOLDER}\n\n"
            f"Yoki QR kod orqali to'lang:",
            parse_mode="Markdown"
        )
        
        # QR kodni yuborish
        try:
            with open("qr_code.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
        except:
            bot.send_message(
                message.chat.id,
                "⚠️ QR kod yuklanmadi. Karta raqamidan foydalaning."
            )
        
        msg = bot.send_message(
            message.chat.id,
            "📸 *To'lov chekini yuboring*\n\n"
            f"To'lov summasi: *{amount} som*\n\n"
            "To'lovni amalga oshirgandan so'ng, chek rasmini yuboring.\n"
            "Admin tasdiqlashidan keyin balansingiz to'ldiriladi.",
            parse_mode="Markdown"
        )
        
        # Summani keyingi qadam uchun saqlash
        bot.register_next_step_handler(msg, lambda m: handle_payment_receipt(m, amount))
        
    except ValueError:
        bot.send_message(
            message.chat.id,
            "❌ Xato! Faqat raqam kiriting.\n\n"
            "Qaytadan urinib ko'ring:",
            reply_markup=create_main_menu()
        )

@bot.message_handler(content_types=['photo'])
def handle_payment_receipt(message, expected_amount=None):
    # Agar summa berilmagan bo'lsa, xato
    if expected_amount is None:
        bot.send_message(
            message.chat.id,
            "❌ Avval '💳 Balans to'ldirish' tugmasini bosing va summani kiriting!",
            reply_markup=create_main_menu()
        )
        return
    
    user_id = message.from_user.id
    username = message.from_user.username or "Yo'q"
    first_name = message.from_user.first_name
    
    data = load_data()
    payment_id = len(data["pending_payments"]) + 1
    
    payment = {
        "id": payment_id,
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "photo_id": message.photo[-1].file_id,
        "expected_amount": expected_amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending"
    }
    
    data["pending_payments"].append(payment)
    save_data(data)
    
    bot.send_message(
        message.chat.id,
        "✅ *Chek qabul qilindi!*\n\n"
        f"💰 So'ralgan summa: {expected_amount} som\n"
        "⏳ Admin tekshirmoqda...\n\n"
        "Tasdiqlangandan so'ng balansingiz to'ldiriladi.",
        parse_mode="Markdown",
        reply_markup=create_main_menu()
    )
    
    # Adminga xabar yuborish
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{payment_id}"),
        types.InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{payment_id}")
    )
    
    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"💳 <b>Yangi to'lov so'rovi</b>\n\n"
                f"👤 Foydalanuvchi: {first_name}\n"
                f"🆔 Username: @{username}\n"
                f"🆔 User ID: {user_id}\n"
                f"💰 Kutilayotgan summa: {expected_amount} som\n"
                f"📅 Sana: {payment['date']}\n\n"
                f"To'lov ID: #{payment_id}",
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_"))
def handle_payment_decision(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Sizda ruxsat yo'q!")
        return
    
    action, payment_id = call.data.split("_")
    payment_id = int(payment_id)
    
    data = load_data()
    payment = next((p for p in data["pending_payments"] if p["id"] == payment_id), None)
    
    if not payment:
        bot.answer_callback_query(call.id, "❌ To'lov topilmadi!")
        return
    
    if action == "approve":
        # Kutilayotgan summani ko'rsatish
        expected = payment.get("expected_amount", 0)
        
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=call.message.caption + f"\n\n⏳ Tasdiqlash jarayonida...\n💰 Kutilayotgan summa: {expected} som",
            parse_mode="HTML"
        )
        
        msg = bot.send_message(
            ADMIN_ID,
            f"💳 To'lov #{payment_id}\n\n"
            f"💰 Foydalanuvchi so'ragan summa: {expected} som\n\n"
            f"Chekda qancha pul bor?\n"
            f"Summani kiriting (faqat raqam):\n\n"
            f"⚠️ Agar summa {expected} somdan kam bo'lsa, foydalanuvchiga ogohlantirish beriladi!",
        )
        bot.register_next_step_handler(msg, lambda m: process_payment_approval(m, payment_id))
        
    else:
        payment["status"] = "rejected"
        save_data(data)
        
        bot.send_message(
            payment["user_id"],
            "❌ *To'lovingiz rad etildi*\n\n"
            "Iltimos, to'g'ri chek yuboring.\n\n"
            "📞 Muammo bo'lsa, admin bilan bog'laning: @diyorbek_muratjonov",
            parse_mode="Markdown",
            reply_markup=create_main_menu()
        )
        
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=call.message.caption + "\n\n❌ <b>Rad etildi</b>",
            parse_mode="HTML"
        )
        bot.answer_callback_query(call.id, "✅ To'lov rad etildi")

def process_payment_approval(message, payment_id):
    try:
        actual_amount = int(message.text)
        data = load_data()
        payment = next((p for p in data["pending_payments"] if p["id"] == payment_id), None)
        
        if not payment:
            bot.send_message(ADMIN_ID, "❌ To'lov topilmadi!")
            return
        
        expected_amount = payment.get("expected_amount", 0)
        user_id = payment["user_id"]
        
        # Agar chekdagi summa kutilgandan kam bo'lsa
        if actual_amount < expected_amount:
            payment["status"] = "rejected"
            save_data(data)
            
            bot.send_message(
                user_id,
                f"⚠️ *To'lov rad etildi!*\n\n"
                f"Siz {expected_amount} som so'ragan edingiz,\n"
                f"Lekin chekda faqat {actual_amount} som ko'rinmoqda.\n\n"
                f"❌ Noto'g'ri summa yoki soxta chek!\n\n"
                f"Iltimos, to'g'ri summada to'lov qiling.\n"
                f"📞 Muammo bo'lsa admin bilan bog'laning: @diyorbek_muratjonov",
                parse_mode="Markdown",
                reply_markup=create_main_menu()
            )
            
            bot.send_message(
                ADMIN_ID,
                f"⚠️ To'lov #{payment_id} rad etildi!\n\n"
                f"Sabab: Noto'g'ri summa\n"
                f"Kutilgan: {expected_amount} som\n"
                f"Chekda: {actual_amount} som"
            )
            return
        
        # Agar hammasi to'g'ri bo'lsa - balansga qo'shish
        # MUHIM: Avval balansni yangilash
        data_fresh = load_data()
        if str(user_id) not in data_fresh["users"]:
            data_fresh["users"][str(user_id)] = {"balance": 0, "orders": []}
        
        data_fresh["users"][str(user_id)]["balance"] += expected_amount
        
        # Payment statusni yangilash
        for p in data_fresh["pending_payments"]:
            if p["id"] == payment_id:
                p["status"] = "approved"
                p["actual_amount"] = actual_amount
                break
        
        save_data(data_fresh)
        
        # Yangi balansni olish
        new_balance = data_fresh["users"][str(user_id)]["balance"]
        
        # Agar kutilgandan ko'p pul kelgan bo'lsa
        if actual_amount > expected_amount:
            bot.send_message(
                user_id,
                f"✅ *To'lovingiz tasdiqlandi!*\n\n"
                f"💰 Balansingiz: {new_balance} som\n\n"
                f"ℹ️ Siz {actual_amount} som yuborgan edingiz,\n"
                f"Balansga {expected_amount} som qo'shildi.\n"
                f"Qolgan {actual_amount - expected_amount} som keyingi to'ldirish uchun hisobga olinadi.",
                parse_mode="Markdown",
                reply_markup=create_main_menu()
            )
        else:
            bot.send_message(
                user_id,
                f"✅ *To'lovingiz tasdiqlandi!*\n\n"
                f"💰 Balansingiz: {new_balance} som\n\n"
                f"Endi xizmatlardan foydalanishingiz mumkin!",
                parse_mode="Markdown",
                reply_markup=create_main_menu()
            )
        
        bot.send_message(
            ADMIN_ID,
            f"✅ To'lov #{payment_id} tasdiqlandi!\n\n"
            f"👤 Foydalanuvchi: {payment['first_name']}\n"
            f"💰 Kutilgan: {expected_amount} som\n"
            f"💰 Chekda: {actual_amount} som\n"
            f"✅ Balansga qo'shildi: {expected_amount} som\n"
            f"💳 Yangi balans: {new_balance} som"
        )
        
    except ValueError:
        bot.send_message(ADMIN_ID, "❌ Xato! Faqat raqam kiriting.")
        bot.send_message(
            ADMIN_ID,
            f"💰 To'lov #{payment_id} uchun summani kiriting (faqat raqam):",
        )
        bot.register_next_step_handler_by_chat_id(
            ADMIN_ID,
            lambda m: process_payment_approval(m, payment_id)
        )
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Xatolik yuz berdi: {str(e)}")
        print(f"ERROR: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("instagram_") or call.data.startswith("tiktok_") or call.data.startswith("telegram_"))
def handle_service_selection(call):
    parts = call.data.split("_")
    if len(parts) == 2:
        platform, service_key = parts
        service = PRICES[platform][service_key]
        
        # Miqdor tanlash menyusini ko'rsatish
        markup = types.InlineKeyboardMarkup()
        for option in service["options"]:
            markup.add(types.InlineKeyboardButton(
                f"{option['quantity']} ta - {option['price']} som",
                callback_data=f"order_{platform}_{service_key}_{option['quantity']}_{option['price']}_{option['service_id']}"
            ))
        markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data=f"back_{platform}"))
        
        bot.edit_message_text(
            f"📝 *{service['name']}*\n\n"
            f"💰 Balansiz: {get_user_balance(call.from_user.id)} som\n\n"
            f"Miqdorni tanlang:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    elif len(parts) >= 3:
        # Buyurtma berish
        handle_order_placement(call)




@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def handle_order_placement(call):
    parts = call.data.split("_")
    platform = parts[1]
    service_key = parts[2]
    quantity = int(parts[3])
    price = int(parts[4])
    service_id = parts[5]
    
    service_name = PRICES[platform][service_key]["name"]
    user_balance = get_user_balance(call.from_user.id)
    
    if user_balance < price:
        bot.answer_callback_query(
            call.id,
            f"❌ Balansda mablag' yetarli emas! Kerak: {price} som",
            show_alert=True
        )
        return
    
    bot.send_message(
        call.message.chat.id,
        f"📝 *{service_name}*\n\n"
        f"🔢 Miqdor: {quantity} ta\n"
        f"💰 Narx: {price} som\n"
        f"💳 Sizning balans: {user_balance} som\n\n"
        f"📎 Havola (link) yuboring:",
        parse_mode="Markdown"
    )
    
    bot.register_next_step_handler_by_chat_id(
        call.message.chat.id,
        lambda m: process_order(m, platform, service_key, service_name, quantity, price, service_id)
    )

def send_smm_order(service_id, link, quantity):
    """SMM Panel API ga buyurtma yuborish"""
    try:
        payload = {
            'key': SMM_API_KEY,
            'action': 'add',
            'service': service_id,
            'link': link,
            'quantity': quantity
        }
        
        response = requests.post(SMM_API_URL, data=payload)
        result = response.json()
        
        if 'order' in result:
            return {"success": True, "order_id": result['order']}
        else:
            return {"success": False, "error": result.get('error', 'Noma\'lum xato')}
    except Exception as e:
        return {"success": False, "error": str(e)}

def process_order(message, platform, service_key, service_name, quantity, price, service_id):
    link = message.text
    user_id = message.from_user.id
    
    # Balansdan yechish
    update_balance(user_id, -price)
    
    # SMM Panel ga buyurtma yuborish
    result = send_smm_order(service_id, link, quantity)
    
    # Buyurtmani saqlash
    data = load_data()
    order = {
        "id": len(data["orders"]) + 1,
        "user_id": user_id,
        "platform": platform,
        "service": service_name,
        "link": link,
        "price": price,
        "quantity": quantity,
        "service_id": service_id,
        "smm_order_id": result.get("order_id", "N/A") if result["success"] else "FAILED",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "processing" if result["success"] else "failed"
    }
    
    data["orders"].append(order)
    if str(user_id) in data["users"]:
        data["users"][str(user_id)]["orders"].append(order["id"])
    save_data(data)
    
    if result["success"]:
        bot.send_message(
            message.chat.id,
            f"✅ <b>Buyurtma qabul qilindi!</b>\n\n"
            f"📋 Buyurtma ID: {order['id']}\n"
            f"📋 SMM Order ID: {result['order_id']}\n"
            f"📱 Platforma: {platform.upper()}\n"
            f"📝 Xizmat: {service_name}\n"
            f"🔢 Miqdor: {quantity} ta\n"
            f"💰 Narx: {price} som\n"
            f"📎 Havola: {link}\n\n"
            f"✅ Buyurtma bajarilmoqda...\n"
            f"💳 Qolgan balans: {get_user_balance(user_id)} som",
            parse_mode="HTML",
            reply_markup=create_main_menu()
        )
        
        # Adminga xabar
        bot.send_message(
            ADMIN_ID,
            f"✅ <b>Buyurtma muvaffaqiyatli yuborildi!</b>\n\n"
            f"📋 ID: {order['id']}\n"
            f"📋 SMM Order: {result['order_id']}\n"
            f"👤 User: {message.from_user.first_name}\n"
            f"🆔 User ID: {user_id}\n"
            f"📱 Platforma: {platform.upper()}\n"
            f"📝 Xizmat: {service_name}\n"
            f"🔢 Miqdor: {quantity} ta\n"
            f"📎 Havola: {link}\n"
            f"📅 Sana: {order['date']}",
            parse_mode="HTML"
        )
    else:
        # Xatolik bo'lsa pulni qaytarish
        update_balance(user_id, price)
        
        bot.send_message(
            message.chat.id,
            f"❌ <b>Xatolik yuz berdi!</b>\n\n"
            f"Buyurtma bajarilmadi.\n"
            f"Pulingiz qaytarildi: {price} som\n\n"
            f"Xato: {result.get('error', 'Noma\'lum xato')}\n\n"
            f"📞 Admin bilan bog'laning: @diyorbek_muratjonov",
            parse_mode="HTML",
            reply_markup=create_main_menu()
        )
        
        # Adminga xabar
        bot.send_message(
            ADMIN_ID,
            f"❌ <b>Buyurtma xatolik!</b>\n\n"
            f"👤 User: {message.from_user.first_name}\n"
            f"📝 Xizmat: {service_name}\n"
            f"📎 Havola: {link}\n"
            f"⚠️ Xato: {result.get('error', 'Noma\'lum')}"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("back_"))
def handle_back_buttons(call):
    if call.data == "back_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "Asosiy menyu:",
            reply_markup=create_main_menu()
        )
    elif call.data == "back_instagram":
        instagram_menu_callback(call)
    elif call.data == "back_tiktok":
        tiktok_menu_callback(call)
    elif call.data == "back_telegram":
        telegram_menu_callback(call)

def instagram_menu_callback(call):
    markup = types.InlineKeyboardMarkup()
    for key, service in PRICES["instagram"].items():
        markup.add(types.InlineKeyboardButton(
            f"{service['name']}",
            callback_data=f"instagram_{key}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
    
    bot.edit_message_text(
        "📸 *Instagram nakrutka xizmatlari*\n\n"
        "Kerakli xizmatni tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup
    )

def tiktok_menu_callback(call):
    markup = types.InlineKeyboardMarkup()
    for key, service in PRICES["tiktok"].items():
        markup.add(types.InlineKeyboardButton(
            f"{service['name']}",
            callback_data=f"tiktok_{key}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
    
    bot.edit_message_text(
        "🎵 *TikTok nakrutka xizmatlari*\n\n"
        "Kerakli xizmatni tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup
    )

def telegram_menu_callback(call):
    markup = types.InlineKeyboardMarkup()
    for key, service in PRICES["telegram"].items():
        markup.add(types.InlineKeyboardButton(
            f"{service['name']}",
            callback_data=f"telegram_{key}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 Ortga", callback_data="back_main"))
    
    bot.edit_message_text(
        "✈️ *Telegram nakrutka xizmatlari*\n\n"
        "Kerakli xizmatni tanlang:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_to_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
        "Asosiy menyu:",
        reply_markup=create_main_menu()
    )

# Admin komandalar
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    data = load_data()
    total_users = len(data["users"])
    total_orders = len(data["orders"])
    pending_payments = len([p for p in data["pending_payments"] if p["status"] == "pending"])
    
    # Jami balans va daromad hisoblash
    total_balance = sum(user.get("balance", 0) for user in data["users"].values())
    completed_orders = [o for o in data["orders"] if o["status"] == "processing"]
    total_revenue = sum(o.get("price", 0) for o in completed_orders)
    
    bot.send_message(
        message.chat.id,
        f"👨‍💼 *Admin Panel*\n\n"
        f"📊 *Statistika:*\n"
        f"👥 Jami foydalanuvchilar: {total_users}\n"
        f"📦 Jami buyurtmalar: {total_orders}\n"
        f"✅ Bajarilgan: {len(completed_orders)}\n"
        f"⏳ Kutilayotgan to'lovlar: {pending_payments}\n\n"
        f"💰 *Moliya:*\n"
        f"💳 Foydalanuvchilar balansi: {total_balance} som\n"
        f"💵 Jami daromad: {total_revenue} som\n\n"
        f"⚙️ *Komandalar:*\n"
        f"/broadcast - Barcha foydalanuvchilarga xabar\n"
        f"/stats - Batafsil statistika\n"
        f"/users - Foydalanuvchilar ro'yxati",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(
        message.chat.id,
        "📢 *Broadcast xabari*\n\n"
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:\n\n"
        "• Matn yuboring\n"
        "• Rasm + matn yuboring\n"
        "• Video yuborishingiz mumkin\n\n"
        "Bekor qilish: /cancel",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.text and message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ Broadcast bekor qilindi.")
        return
    
    data = load_data()
    users = data["users"]
    
    if len(users) == 0:
        bot.send_message(message.chat.id, "⚠️ Hech qanday foydalanuvchi yo'q!")
        return
    
    # Tasdiqlash
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ Ha, yuborish", callback_data="broadcast_confirm"),
        types.InlineKeyboardButton("❌ Yo'q, bekor qilish", callback_data="broadcast_cancel")
    )
    
    # Xabarni saqlash
    if message.content_type == 'text':
        broadcast_data = {
            'type': 'text',
            'content': message.text
        }
    elif message.content_type == 'photo':
        broadcast_data = {
            'type': 'photo',
            'photo_id': message.photo[-1].file_id,
            'caption': message.caption or ''
        }
    elif message.content_type == 'video':
        broadcast_data = {
            'type': 'video',
            'video_id': message.video.file_id,
            'caption': message.caption or ''
        }
    else:
        bot.send_message(message.chat.id, "❌ Faqat matn, rasm yoki video yuborishingiz mumkin!")
        return
    
    # Vaqtincha saqlash
    data['temp_broadcast'] = broadcast_data
    save_data(data)
    
    bot.send_message(
        message.chat.id,
        f"📊 *Broadcast ma'lumoti:*\n\n"
        f"👥 Foydalanuvchilar soni: {len(users)}\n"
        f"📝 Xabar turi: {broadcast_data['type']}\n\n"
        f"Xabarni yuborishni tasdiqlaysizmi?",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("broadcast_"))
def handle_broadcast_decision(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Sizda ruxsat yo'q!")
        return
    
    if call.data == "broadcast_cancel":
        bot.edit_message_text(
            "❌ Broadcast bekor qilindi.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        return
    
    if call.data == "broadcast_confirm":
        data = load_data()
        broadcast_data = data.get('temp_broadcast')
        
        if not broadcast_data:
            bot.answer_callback_query(call.id, "❌ Xatolik!")
            return
        
        users = data["users"]
        total_users = len(users)
        success_count = 0
        failed_count = 0
        
        # Progress xabari
        progress_msg = bot.edit_message_text(
            f"⏳ Yuborilmoqda...\n\n"
            f"Jami: {total_users}\n"
            f"✅ Muvaffaqiyatli: 0\n"
            f"❌ Xato: 0",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        
        # Barcha foydalanuvchilarga yuborish
        for user_id in users.keys():
            try:
                if broadcast_data['type'] == 'text':
                    bot.send_message(int(user_id), broadcast_data['content'])
                elif broadcast_data['type'] == 'photo':
                    bot.send_photo(
                        int(user_id),
                        broadcast_data['photo_id'],
                        caption=broadcast_data['caption']
                    )
                elif broadcast_data['type'] == 'video':
                    bot.send_video(
                        int(user_id),
                        broadcast_data['video_id'],
                        caption=broadcast_data['caption']
                    )
                success_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to send to {user_id}: {e}")
            
            # Har 10 ta foydalanuvchidan keyin progress yangilash
            if (success_count + failed_count) % 10 == 0:
                try:
                    bot.edit_message_text(
                        f"⏳ Yuborilmoqda...\n\n"
                        f"Jami: {total_users}\n"
                        f"✅ Muvaffaqiyatli: {success_count}\n"
                        f"❌ Xato: {failed_count}",
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id
                    )
                except:
                    pass
        
        # Yakuniy natija
        bot.edit_message_text(
            f"✅ *Broadcast yakunlandi!*\n\n"
            f"📊 *Natijalar:*\n"
            f"👥 Jami foydalanuvchilar: {total_users}\n"
            f"✅ Muvaffaqiyatli yuborildi: {success_count}\n"
            f"❌ Xato: {failed_count}\n\n"
            f"📈 Muvaffaqiyat darajasi: {round(success_count/total_users*100, 1)}%",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
        
        # Temp broadcast ni o'chirish
        if 'temp_broadcast' in data:
            del data['temp_broadcast']
            save_data(data)

@bot.message_handler(commands=['stats'])
def detailed_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    data = load_data()
    users = data["users"]
    orders = data["orders"]
    
    # Platform bo'yicha statistika
    instagram_orders = len([o for o in orders if o["platform"] == "instagram"])
    tiktok_orders = len([o for o in orders if o["platform"] == "tiktok"])
    telegram_orders = len([o for o in orders if o["platform"] == "telegram"])
    
    # Eng ko'p buyurtma bergan foydalanuvchi
    user_order_counts = {}
    for order in orders:
        user_id = str(order["user_id"])
        user_order_counts[user_id] = user_order_counts.get(user_id, 0) + 1
    
    top_user = max(user_order_counts.items(), key=lambda x: x[1]) if user_order_counts else (None, 0)
    top_user_name = users.get(top_user[0], {}).get("first_name", "Noma'lum") if top_user[0] else "N/A"
    
    # Jami daromad
    total_revenue = sum(o.get("price", 0) for o in orders if o["status"] == "processing")
    
    bot.send_message(
        message.chat.id,
        f"📊 *Batafsil Statistika*\n\n"
        f"👥 *Foydalanuvchilar:*\n"
        f"Jami: {len(users)}\n\n"
        f"📦 *Buyurtmalar:*\n"
        f"Jami: {len(orders)}\n"
        f"📸 Instagram: {instagram_orders}\n"
        f"🎵 TikTok: {tiktok_orders}\n"
        f"✈️ Telegram: {telegram_orders}\n\n"
        f"💰 *Moliya:*\n"
        f"Jami daromad: {total_revenue} som\n\n"
        f"🏆 *Top foydalanuvchi:*\n"
        f"{top_user_name} - {top_user[1]} buyurtma",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    data = load_data()
    users = data["users"]
    
    if len(users) == 0:
        bot.send_message(message.chat.id, "⚠️ Hech qanday foydalanuvchi yo'q!")
        return
    
    user_list = "👥 *Foydalanuvchilar ro'yxati:*\n\n"
    for i, (user_id, user_data) in enumerate(list(users.items())[:20], 1):
        username = user_data.get("username", "Yo'q")
        first_name = user_data.get("first_name", "Noma'lum")
        balance = user_data.get("balance", 0)
        orders_count = len(user_data.get("orders", []))
        
        user_list += f"{i}. {first_name} (@{username})\n"
        user_list += f"   💰 {balance} som | 📦 {orders_count} buyurtma\n\n"
    
    if len(users) > 20:
        user_list += f"\n... va yana {len(users) - 20} ta foydalanuvchi"
    
    bot.send_message(message.chat.id, user_list, parse_mode="Markdown")

if __name__ == "__main__":
    print("✅ Bot ishga tushdi!")
    bot.infinity_polling()