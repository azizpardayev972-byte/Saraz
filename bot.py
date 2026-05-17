import os
import telebot
import random
from groq import Groq
from telebot import types

TOKEN = os.environ.get("TOKEN", "8943790902:AAHTWz17cz4ShIFi-Fo2lkoqhC1nLBLkemU")
GROQ_KEY = os.environ.get("GROQ_KEY", "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")

bot = telebot.TeleBot(TOKEN)
client = Groq(api_key=GROQ_KEY)

user_modes = {}
user_game_data = {}

# =====================
# START
# =====================

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💬 Chat", callback_data="chat"),
        types.InlineKeyboardButton("🎮 O'yinlar", callback_data="game"),
        types.InlineKeyboardButton("🎵 Musiqa", callback_data="music"),
        types.InlineKeyboardButton("💌 Sevgi so'zlari", callback_data="love"),
        types.InlineKeyboardButton("🎁 Sovg'a", callback_data="gift"),
        types.InlineKeyboardButton("❓ Savollar", callback_data="truth")
    )
    bot.send_message(message.chat.id,
        "💝 *Salom! Men sevishganlar uchun maxsus botman!*\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['menu'])
def menu(message):
    start(message)

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

@bot.message_handler(commands=['couple'])
def couple_game(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💌 Sevgi xati", callback_data="love"),
        types.InlineKeyboardButton("🎮 O'yin", callback_data="game"),
        types.InlineKeyboardButton("❓ Savol", callback_data="truth"),
        types.InlineKeyboardButton("🎁 Sovg'a ideyasi", callback_data="gift")
    )
    bot.send_message(message.chat.id,
        "👫 *Juftlik o'yinlari!*\n\nNima qilmoqchisiz?",
        parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['kiss'])
def kiss(message):
    kisses = [
        "😘 Bir o'pich yubordi!",
        "💋 Sevgi o'pichi!",
        "🥰 Yurak to'la mehr bilan!",
        "💝 Abadiy muhabbat bilan!"
    ]
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"💋 *{name}* — {random.choice(kisses)}", parse_mode="Markdown")

@bot.message_handler(commands=['hug'])
def hug(message):
    name = message.from_user.first_name
    hugs = [
        "🤗 Issiq quchoq yubordi!",
        "💞 Mehribon quchoq!",
        "🫂 Abadiy quchoq!"
    ]
    bot.send_message(message.chat.id, f"🤗 *{name}* — {random.choice(hugs)}", parse_mode="Markdown")

@bot.message_handler(commands=['date'])
def date_idea(message):
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
    bot.send_message(message.chat.id,
        "🌹 *Date ideyasi:*\n\n" + response.choices[0].message.content,
        parse_mode="Markdown", reply_markup=markup)

# =====================
# INLINE TUGMALAR
# =====================

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    if call.data == "chat":
        user_modes[chat_id] = 'chat'
        bot.send_message(chat_id,
            "💬 *AI suhbat rejimi yoqildi!*\n"
            "Istalgan narsani yozing.\n"
            "Chiqish uchun /menu",
            parse_mode="Markdown")

    elif call.data == "love":
        user_modes[chat_id] = 'love'
        bot.send_message(chat_id,
            "💌 *Sevgilingizga yozmoqchi bo'lgan matnni kiriting:*\n"
            "Men uni chiroyli qilib bezatib beraman! 🌹",
            parse_mode="Markdown")

    elif call.data == "gift":
        user_modes[chat_id] = 'gift'
        bot.send_message(chat_id,
            "🎁 *Sevgilingiz haqida ayting!*\n"
            "Yoshi, qiziqishlari yoki sevgan narsalarini yozing:",
            parse_mode="Markdown")

    elif call.data == "music":
        user_modes[chat_id] = 'music'
        bot.send_message(chat_id,
            "🎵 *Kayfiyatingizni yoki qo'shiq nomini yozing!*",
            parse_mode="Markdown")

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
            "🌹 *Date ideyasi:*\n\n" + response.choices[0].message.content,
            parse_mode="Markdown", reply_markup=markup)

    elif call.data == "game":
        user_modes[chat_id] = None
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔢 Sonni top", callback_data="guess"),
            types.InlineKeyboardButton("❓ Romantik savollar", callback_data="truth"),
            types.InlineKeyboardButton("🧠 Viktorina", callback_data="quiz")
        )
        bot.send_message(chat_id,
            "🎮 *Qaysi o'yinni o'ynamoqchisiz?*",
            parse_mode="Markdown", reply_markup=markup)

    elif call.data == "guess":
        number = random.randint(1, 100)
        user_game_data[chat_id] = {'number': number, 'attempts': 0}
        user_modes[chat_id] = 'guess'
        bot.send_message(chat_id,
            "🔢 *1 dan 100 gacha son o'yladim!*\n"
            "Toping — urinishlar soni hisoblanadi 😄",
            parse_mode="Markdown")

    elif call.data == "truth":
        user_modes[chat_id] = None
        questions = [
            "❓ Birinchi marta qachon sevgi his qildingiz?",
            "❓ Sherikingizda eng yoqtirgan xususiyatingiz nima?",
            "❓ Eng romantik lahzangiz qaysi edi?",
            "❓ Kelajakda qayerda yashashni orzu qilasiz?",
            "❓ Sevgilingizga aytmagan eng katta siringiz nima?",
            "❓ Birinchi uchrashuvingizda nima his qildingiz?"
        ]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Boshqa savol", callback_data="truth"))
        bot.send_message(chat_id, random.choice(questions), reply_markup=markup)

    elif call.data == "quiz":
        user_modes[chat_id] = None
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
        bot.send_message(chat_id, response.choices[0].message.content, reply_markup=markup)

    bot.answer_callback_query(call.id)

# =====================
# BARCHA XABARLAR
# =====================

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    mode = user_modes.get(chat_id)
    text = message.text

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
                {"role": "user", "content": f"'{text}' kayfiyati uchun 5 ta musiqa tavsiya qil. Har biri uchun: nomi, ijrochi va YouTube search linki ber. Format: 🎵 Nomi - Ijrochi\n🔗 https://www.youtube.com/results?search_query=..."}
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
        start(message)

print("Bot ishlamoqda... ✅")
bot.polling()