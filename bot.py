import os
import telebot
import random
from groq import Groq
from telebot import types
from datetime import datetime

TOKEN = os.environ.get("TOKEN", "8943790902:AAHTWz17cz4ShIFi-Fo2lkoqhC1nLBLkemU")
GROQ_KEY = os.environ.get("GROQ_KEY", "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")
ADMIN_ID = 7808117210

bot = telebot.TeleBot(TOKEN)
client = Groq(api_key=GROQ_KEY)

user_modes = {}
user_game_data = {}
user_dates = {}  # muhim sanalar
custom_truths = []  # o'z savollar
custom_dares = []   # o'z vazifalar
compatibility_data = {}  # mos kelish testi

# =====================
# MENYU
# =====================

def main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💬 AI Suhbat", callback_data="chat"),
        types.InlineKeyboardButton("🎮 O'yinlar", callback_data="game"),
        types.InlineKeyboardButton("🎵 Musiqa", callback_data="music"),
        types.InlineKeyboardButton("💌 Sevgi xati", callback_data="love"),
        types.InlineKeyboardButton("🎁 Sovg'a", callback_data="gift"),
        types.InlineKeyboardButton("🌹 Date ideya", callback_data="date"),
        types.InlineKeyboardButton("📅 Sanalar", callback_data="dates"),
        types.InlineKeyboardButton("🔮 Maslahat", callback_data="advice")
    )
    bot.send_message(chat_id,
        "❤️‍🔥 *M BOT*\n"
        "━━━━━━━━━━━━━━━━\n"
        " _Sevishganlar uchun maxsus bot_\n"
        "━━━━━━━━━━━━━━━━\n\n"
        " Siz uchun nima qila olaman?",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    main_menu(message.chat.id)

# =====================
# GURUH BUYRUQLARI
# =====================

@bot.message_handler(commands=['lucky'])
def lucky(message):
    responses = [
        "💕 Bugun sizning kuningiz! Sevgilingizga mehr ko'rsating!",
        "🌹 Bugun romantik kun — biror ajoyib narsa qiling!",
        "💫 Bugun baxt sizning tomoningizda!",
        "🎯 Bugun sevgilingizni hayratda qoldiring!",
        "✨ Bugun muhabbat havoda — his qiling!"
    ]
    bot.reply_to(message, random.choice(responses))

@bot.message_handler(commands=['kiss'])
def kiss(message):
    name = message.from_user.first_name
    kisses = ["😘 Bir o'pich yubordi!", "💋 Sevgi o'pichi!", "🥰 Yurak to'la mehr bilan!", "💝 Abadiy muhabbat bilan!"]
    bot.send_message(message.chat.id, f"💋 *{name}* — {random.choice(kisses)}", parse_mode="Markdown")

@bot.message_handler(commands=['hug'])
def hug(message):
    name = message.from_user.first_name
    hugs = ["🤗 Issiq quchoq yubordi!", "💞 Mehribon quchoq!", "🫂 Abadiy quchoq!"]
    bot.send_message(message.chat.id, f"🤗 *{name}* — {random.choice(hugs)}", parse_mode="Markdown")

@bot.message_handler(commands=['couple'])
def couple_game(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💌 Sevgi xati", callback_data="love"),
        types.InlineKeyboardButton("🎮 O'yin", callback_data="game"),
        types.InlineKeyboardButton("❓ Savol", callback_data="truth_custom"),
        types.InlineKeyboardButton("🎁 Sovg'a ideyasi", callback_data="gift")
    )
    bot.send_message(message.chat.id,
        "👫 *Juftlik o'yinlari!*\n\nNima qilmoqchisiz?",
        parse_mode="Markdown", reply_markup=markup)

# =====================
# HAQIQAT YOKI SHART
# =====================

@bot.message_handler(commands=['addsavol'])
def add_truth(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "❗ Format: /addsavol Savolingiz matni")
        return
    custom_truths.append(parts[1])
    bot.reply_to(message, f"✅ *Savol qo'shildi!*\n_{parts[1]}_", parse_mode="Markdown")

@bot.message_handler(commands=['addvazifa'])
def add_dare(message):
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "❗ Format: /addvazifa Vazifangiz matni")
        return
    custom_dares.append(parts[1])
    bot.reply_to(message, f"✅ *Vazifa qo'shildi!*\n_{parts[1]}_", parse_mode="Markdown")

@bot.message_handler(commands=['truth'])
def truth(message):
    savollar = custom_truths if custom_truths else [
        "Birinchi marta qachon sevgi his qildingiz?",
        "Sherikingizda eng yoqtirgan xususiyat nima?",
        "Eng romantik lahzangiz qaysi edi?",
        "Sevgilingizga aytmagan eng katta siringiz nima?",
        "Birinchi uchrashuvda nima his qildingiz?"
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Boshqa savol", callback_data="truth_custom"))
    bot.send_message(message.chat.id,
        "❓ *Haqiqat!*\n━━━━━━━━━━━━━━━━\n" + random.choice(savollar),
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['dare'])
def dare(message):
    vazifalar = custom_dares if custom_dares else [
        "Sevgilingizni quchoqla!",
        "Sevgilingizga chiroyli narsa de!",
        "Sevgilingizning qo'lini ushla!",
        "Sevgilingizga sevgi qo'shig'i kuy!",
        "Sevgilingizga kompliment ayt!"
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Boshqa vazifa", callback_data="dare_custom"))
    bot.send_message(message.chat.id,
        "🎯 *Shart!*\n━━━━━━━━━━━━━━━━\n" + random.choice(vazifalar),
        parse_mode="Markdown", reply_markup=markup)

# =====================
# MUHIM SANALAR
# =====================

@bot.message_handler(commands=['sana'])
def add_date(message):
    user_modes[message.chat.id] = 'add_date'
    bot.reply_to(message,
        "📅 *Muhim sana qo'shish*\n"
        "━━━━━━━━━━━━━━━━\n"
        "Format: `Sana nomi | KK.OO.YYYY`\n"
        "Masalan: `Birinchi uchrashuv | 14.02.2023`",
        parse_mode="Markdown")

# =====================
# MOS KELISH TESTI
# =====================

@bot.message_handler(commands=['mos'])
def compatibility(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.first_name

    if chat_id not in compatibility_data:
        compatibility_data[chat_id] = {}

    compatibility_data[chat_id][user_id] = name
    count = len(compatibility_data[chat_id])

    if count == 1:
        bot.send_message(chat_id,
            f"💕 *{name}* tayyor!\n"
            "Ikkinchi kishi ham /mos yozsin!",
            parse_mode="Markdown")
    elif count >= 2:
        names = list(compatibility_data[chat_id].values())
        score = random.randint(75, 100)
        hearts = "❤️" * (score // 10)
        bot.send_message(chat_id,
            f"💑 *Mos kelish testi*\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"👤 {names[0]} & {names[1]}\n\n"
            f"{hearts}\n\n"
            f"💯 Mos kelish: *{score}%*\n\n"
            f"{'💝 Siz bir-biringiz uchun yaratilgansiz!' if score > 90 else '💕 Sizning muhabbatingiz kuchli!'}",
            parse_mode="Markdown")
        compatibility_data[chat_id] = {}

# =====================
# INLINE TUGMALAR
# =====================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    if call.data == "chat":
        user_modes[chat_id] = 'chat'
        bot.send_message(chat_id,
            "💬 *AI suhbat rejimi*\n"
            "━━━━━━━━━━━━━━━━\n"
            "Istalgan narsani yozing 😊\n"
            "Chiqish uchun /menu",
            parse_mode="Markdown")

    elif call.data == "love":
        user_modes[chat_id] = 'love'
        bot.send_message(chat_id,
            "💌 *Sevgi xati*\n"
            "━━━━━━━━━━━━━━━━\n"
            "Sevgilingizga yozmoqchi bo'lgan matnni kiriting:\n"
            "_Men uni chiroyli qilib bezatib beraman_ 🌹",
            parse_mode="Markdown")

    elif call.data == "gift":
        user_modes[chat_id] = 'gift'
        bot.send_message(chat_id,
            "🎁 *Sovg'a maslahatchi*\n"
            "━━━━━━━━━━━━━━━━\n"
            "Sevgilingiz haqida ayting!\n"
            "_Yoshi, qiziqishlari yoki sevgan narsalarini yozing:_",
            parse_mode="Markdown")

    elif call.data == "music":
        user_modes[chat_id] = 'music'
        bot.send_message(chat_id,
            "🎵 *Musiqa qidirish*\n"
            "━━━━━━━━━━━━━━━━\n"
            "Kayfiyatingizni yoki qo'shiq nomini yozing!\n"
            "_Masalan: romantik, g'amgin, Shaxriyor_",
            parse_mode="Markdown")

    elif call.data == "advice":
        user_modes[chat_id] = 'advice'
        bot.send_message(chat_id,
            "🔮 *Munosabat maslahatchi*\n"
            "━━━━━━━━━━━━━━━━\n"
            "Muammoingizni yoki savolingizni yozing:\n"
            "_Men sizga maslahat beraman_ 💭",
            parse_mode="Markdown")

    elif call.data == "dates":
        chat_id_dates = user_dates.get(chat_id, {})
        if not chat_id_dates:
            bot.send_message(chat_id,
                "📅 *Muhim sanalar*\n"
                "━━━━━━━━━━━━━━━━\n"
                "Hali sana yo'q!\n"
                "/sana — sana qo'shish",
                parse_mode="Markdown")
        else:
            today = datetime.now()
            text = "📅 *Muhim sanalar*\n━━━━━━━━━━━━━━━━\n"
            for name, date in chat_id_dates.items():
                delta = (date - today).days
                if delta < 0:
                    years = today.year - date.year
                    text += f"🌹 {name}: {years} yil bo'ldi!\n"
                else:
                    text += f"⏳ {name}: {delta} kun qoldi!\n"
            bot.send_message(chat_id, text, parse_mode="Markdown")

    elif call.data == "date":
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=200,
            messages=[
                {"role": "system", "content": "Sen juftliklar uchun maslahatchi botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": "Juftlik uchun 1 ta romantik date ideyasi ber. Qisqa va aniq."}
            ]
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Boshqa ideya", callback_data="date"))
        bot.send_message(chat_id,
            "🌹 *Date ideyasi*\n"
            "━━━━━━━━━━━━━━━━\n" + response.choices[0].message.content,
            parse_mode="Markdown", reply_markup=markup)

    elif call.data == "game":
        user_modes[chat_id] = None
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔢 Sonni top", callback_data="guess"),
            types.InlineKeyboardButton("❓ Haqiqat", callback_data="truth_custom"),
            types.InlineKeyboardButton("🎯 Shart", callback_data="dare_custom"),
            types.InlineKeyboardButton("🧠 Viktorina", callback_data="quiz"),
            types.InlineKeyboardButton("💕 Mos kelish", callback_data="mos")
        )
        bot.send_message(chat_id,
            "🎮 *O'yinlar*\n"
            "━━━━━━━━━━━━━━━━\n"
            "Qaysi o'yinni o'ynamoqchisiz?",
            parse_mode="Markdown", reply_markup=markup)

    elif call.data == "mos":
        user_id = call.from_user.id
        name = call.from_user.first_name
        if chat_id not in compatibility_data:
            compatibility_data[chat_id] = {}
        compatibility_data[chat_id][user_id] = name
        count = len(compatibility_data[chat_id])
        if count == 1:
            bot.send_message(chat_id,
                f"💕 *{name}* tayyor!\nIkkinchi kishi ham tugmani bossin!",
                parse_mode="Markdown")
        elif count >= 2:
            names = list(compatibility_data[chat_id].values())
            score = random.randint(75, 100)
            hearts = "❤️" * (score // 10)
            bot.send_message(chat_id,
                f"💑 *Mos kelish testi*\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"👤 {names[0]} & {names[1]}\n\n"
                f"{hearts}\n\n"
                f"💯 Mos kelish: *{score}%*\n\n"
                f"{'💝 Siz bir-biringiz uchun yaratilgansiz!' if score > 90 else '💕 Sizning muhabbatingiz kuchli!'}",
                parse_mode="Markdown")
            compatibility_data[chat_id] = {}

    elif call.data == "guess":
        number = random.randint(1, 100)
        user_game_data[chat_id] = {'number': number, 'attempts': 0}
        user_modes[chat_id] = 'guess'
        bot.send_message(chat_id,
            "🔢 *Sonni top!*\n"
            "━━━━━━━━━━━━━━━━\n"
            "1 dan 100 gacha son o'yladim!\n"
            "_Urinishlar soni hisoblanadi_ 😄",
            parse_mode="Markdown")

    elif call.data == "truth_custom":
        savollar = custom_truths if custom_truths else [
            "Birinchi marta qachon sevgi his qildingiz?",
            "Sherikingizda eng yoqtirgan xususiyat nima?",
            "Eng romantik lahzangiz qaysi edi?",
            "Sevgilingizga aytmagan eng katta siringiz nima?",
            "Birinchi uchrashuvda nima his qildingiz?"
        ]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Boshqa savol", callback_data="truth_custom"))
        bot.send_message(chat_id,
            "❓ *Haqiqat!*\n━━━━━━━━━━━━━━━━\n" + random.choice(savollar),
            parse_mode="Markdown", reply_markup=markup)

    elif call.data == "dare_custom":
        vazifalar = custom_dares if custom_dares else [
            "Sevgilingizni quchoqla!",
            "Sevgilingizga chiroyli narsa de!",
            "Sevgilingizning qo'lini ushla!",
            "Sevgilingizga sevgi qo'shig'i kuy!",
            "Sevgilingizga kompliment ayt!"
        ]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Boshqa vazifa", callback_data="dare_custom"))
        bot.send_message(chat_id,
            "🎯 *Shart!*\n━━━━━━━━━━━━━━━━\n" + random.choice(vazifalar),
            parse_mode="Markdown", reply_markup=markup)

    elif call.data == "quiz":
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=200,
            messages=[
                {"role": "system", "content": "Sen juftliklar uchun viktorina o'tkazuvchi botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": "Juftliklar uchun 1 ta qiziqarli viktorina savoli yoz. Format:\nSavol: ...\nA) ...\nB) ...\nC) ...\nTo'g'ri javob: ..."}
            ]
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Boshqa savol", callback_data="quiz"))
        bot.send_message(chat_id,
            "🧠 *Viktorina*\n"
            "━━━━━━━━━━━━━━━━\n" + response.choices[0].message.content,
            parse_mode="Markdown", reply_markup=markup)

    bot.answer_callback_query(call.id)

# =====================
# BARCHA XABARLAR
# =====================

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    mode = user_modes.get(chat_id)
    text = message.text

    # Admin ga xabar yuborish
    if chat_id != ADMIN_ID:
        try:
            name = message.from_user.first_name
            username = message.from_user.username or "yo'q"
            bot.send_message(ADMIN_ID,
                f"👤 *Yangi xabar!*\n"
                f"━━━━━━━━━━━━\n"
                f"Ism: {name}\n"
                f"Username: @{username}\n"
                f"ID: `{chat_id}`\n"
                f"Xabar: {text}",
                parse_mode="Markdown")
        except:
            pass

    if mode == 'chat':
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=[
                {"role": "system", "content": "Sen sevishganlar uchun mo'ljallangan mehribon, romantik va qo'llab-quvvatlovchi AI yordamchisisisan. O'zbek tilida gapirasan. Qisqa va samimiy javob ber."},
                {"role": "user", "content": text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)

    elif mode == 'love':
        user_modes[chat_id] = None
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[
                {"role": "system", "content": "Sen romantik shoir botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": f"Quyidagi matnni chiroyli romantik tarzda bezat, emoji qo'sh:\n{text}"}
            ]
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💌 Yana yozish", callback_data="love"))
        bot.reply_to(message, response.choices[0].message.content, reply_markup=markup)

    elif mode == 'advice':
        user_modes[chat_id] = None
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=[
                {"role": "system", "content": "Sen munosabatlar bo'yicha tajribali maslahatchi botsan. O'zbek tilida samimiy, mehribon va amaliy maslahat berasan."},
                {"role": "user", "content": text}
            ]
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔮 Yana savol", callback_data="advice"))
        bot.reply_to(message, response.choices[0].message.content, reply_markup=markup)

    elif mode == 'add_date':
        user_modes[chat_id] = None
        try:
            parts = text.split('|')
            name = parts[0].strip()
            date = datetime.strptime(parts[1].strip(), "%d.%m.%Y")
            if chat_id not in user_dates:
                user_dates[chat_id] = {}
            user_dates[chat_id][name] = date
            today = datetime.now()
            delta = (date - today).days
            if delta < 0:
                years = today.year - date.year
                msg = f"🌹 {name}: {years} yil bo'ldi!"
            else:
                msg = f"⏳ {name}: {delta} kun qoldi!"
            bot.reply_to(message,
                f"✅ *Sana qo'shildi!*\n━━━━━━━━━━━━━━━━\n{msg}",
                parse_mode="Markdown")
        except:
            bot.reply_to(message,
                "❗ Format noto'g'ri!\nMasalan: `Birinchi uchrashuv | 14.02.2023`",
                parse_mode="Markdown")

    elif mode == 'guess':
        try:
            guess = int(text)
            data = user_game_data[chat_id]
            data['attempts'] += 1
            if guess < data['number']:
                bot.send_message(chat_id, "⬆️ Kattaroq son!")
            elif guess > data['number']:
                bot.send_message(chat_id, "⬇️ Kichikroq son!")
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔄 Yana o'ynash", callback_data="guess"))
                bot.send_message(chat_id,
                    f"🎉 *To'g'ri! {data['attempts']} ta urinishda topdingiz!*",
                    parse_mode="Markdown", reply_markup=markup)
                user_modes[chat_id] = None
        except:
            bot.send_message(chat_id, "Faqat son kiriting!")

    elif mode == 'music':
        user_modes[chat_id] = None
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=400,
            messages=[
                {"role": "system", "content": "Sen musiqa tavsiya qiluvchi botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": f"'{text}' kayfiyati uchun 5 ta musiqa tavsiya qil. Har biri uchun nomi, ijrochi va YouTube search linki ber. Format:\n🎵 Nomi - Ijrochi\n🔗 https://www.youtube.com/results?search_query=..."}
            ]
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎵 Yana qidirish", callback_data="music"))
        bot.reply_to(message, response.choices[0].message.content, reply_markup=markup)

    elif mode == 'gift':
        user_modes[chat_id] = None
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=400,
            messages=[
                {"role": "system", "content": "Sen sovg'a maslahatchi botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": f"'{text}' ma'lumotiga asoslanib sevgilisi uchun 5 ta sovg'a ideyasi ber. Har birini yangi qatordan yoz. Emoji qo'sh."}
            ]
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎁 Yana so'rash", callback_data="gift"))
        bot.reply_to(message, response.choices[0].message.content, reply_markup=markup)

    else:
        main_menu(chat_id)

print("Bot ishlamoqda... ✅")
bot.polling()