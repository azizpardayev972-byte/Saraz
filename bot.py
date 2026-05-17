import telebot
import random
from groq import Groq

TOKEN = "8943790902:AAHTWz17cz4ShIFi-Fo2lkoqhC1nLBLkemU"
GROQ_KEY = "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"

bot = telebot.TeleBot(TOKEN)
client = Groq(api_key=GROQ_KEY)

user_modes = {}
user_game_data = {}

# =====================
# START & MENYU
# =====================

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "💝 Salom! Men sevishganlar uchun maxsus botman!\n\n"
        "📋 /menu — Barcha imkoniyatlar")

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id,
        "💝 Nima qilmoqchisiz?\n\n"
        "💬 /chat — AI bilan romantik suhbat\n"
        "🎮 /game — Juftlik o'yinlari\n"
        "🎵 /music — Musiqa tavsiya\n"
        "💌 /love — Sevgi so'zlari\n"
        "🎁 /gift — Sovg'a ideyalari")

# =====================
# AI CHAT
# =====================

@bot.message_handler(commands=['chat'])
def chat_mode(message):
    user_modes[message.chat.id] = 'chat'
    bot.send_message(message.chat.id,
        "💬 AI suhbat rejimi yoqildi!\n"
        "Istalgan narsani yozing. Chiqish uchun /menu")

# =====================
# SEVGI SO'ZLARI
# =====================

@bot.message_handler(commands=['love'])
def love_words(message):
    user_modes[message.chat.id] = 'love'
    bot.send_message(message.chat.id,
        "💌 Sevgilingizga yozmoqchi bo'lgan matnni kiriting:\n"
        "Men uni chiroyli qilib bezatib beraman! 🌹")

# =====================
# SOVG'A IDEYALARI
# =====================

@bot.message_handler(commands=['gift'])
def gift_ideas(message):
    user_modes[message.chat.id] = 'gift'
    bot.send_message(message.chat.id,
        "🎁 Sevgilingiz haqida ayting!\n"
        "Yoshi, qiziqishlari yoki sevgan narsalarini yozing:")

# =====================
# O'YINLAR
# =====================

@bot.message_handler(commands=['game'])
def game_menu(message):
    user_modes[message.chat.id] = None
    bot.send_message(message.chat.id,
        "🎮 Qaysi o'yinni o'ynamoqchisiz?\n\n"
        "1️⃣ /guess — Sonni top\n"
        "2️⃣ /quiz — Juftlik viktorinasi\n"
        "3️⃣ /truth — Romantik savollar")

@bot.message_handler(commands=['guess'])
def guess_game(message):
    number = random.randint(1, 100)
    user_game_data[message.chat.id] = {'game': 'guess', 'number': number, 'attempts': 0}
    user_modes[message.chat.id] = 'guess'
    bot.send_message(message.chat.id,
        "🔢 1 dan 100 gacha son o'yladim!\n"
        "Toping — urinishlar soni hisoblanadi 😄")

@bot.message_handler(commands=['truth'])
def truth_dare(message):
    user_modes[message.chat.id] = None
    questions = [
        "❓ Birinchi marta qachon sevgi his qildingiz?",
        "❓ Sherikingizda eng yoqtirgan xususiyatingiz nima?",
        "❓ Eng romantik lahzangiz qaysi edi?",
        "❓ Kelajakda qayerda yashashni orzu qilasiz?",
        "❓ Sevgilingizga aytmagan eng katta siringiz nima?",
        "❓ Birinchi uchrashuvingizda nima his qildingiz?"
    ]
    bot.send_message(message.chat.id, random.choice(questions))

@bot.message_handler(commands=['quiz'])
def quiz(message):
    user_modes[message.chat.id] = None
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=200,
        messages=[
            {"role": "system", "content": "Sen juftliklar uchun viktorina o'tkazuvchi botsan. O'zbek tilida javob berasan."},
            {"role": "user", "content": "Juftliklar uchun 1 ta qiziqarli viktorina savoli yoz. Format:\nSavol: ...\nA) ...\nB) ...\nC) ...\nTo'g'ri javob: ..."}
        ]
    )
    bot.send_message(message.chat.id, response.choices[0].message.content)

# =====================
# MUSIQA
# =====================

@bot.message_handler(commands=['music'])
def music(message):
    user_modes[message.chat.id] = 'music'
    bot.send_message(message.chat.id,
        "🎵 Kayfiyatingizni yoki qo'shiq nomini yozing!\n"
        "Masalan: 'romantik', 'g'amgin', 'Shaxriyor'")

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
        bot.reply_to(message, response.choices[0].message.content)

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
                bot.send_message(chat_id,
                    f"🎉 To'g'ri! {data['attempts']} ta urinishda topdingiz!\n"
                    "/game — Yana o'ynash")
                user_modes[chat_id] = None
        except:
            bot.send_message(chat_id, "Faqat son kiriting!")

    elif mode == 'music':
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[
                {"role": "system", "content": "Sen musiqa tavsiya qiluvchi botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": f"'{text}' kayfiyati uchun 5 ta musiqa tavsiya qil. O'zbek va xorijiy qo'shiqlardan. Har birini yangi qatordan yoz. Emoji qo'sh."}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)

    elif mode == 'gift':
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=400,
            messages=[
                {"role": "system", "content": "Sen sovg'a maslahatchi botsan. O'zbek tilida javob berasan."},
                {"role": "user", "content": f"'{text}' ma'lumotiga asoslanib sevgilisi uchun 5 ta sovg'a ideyasi ber. Har birini yangi qatordan yoz. Emoji qo'sh."}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)

    else:
        bot.reply_to(message, "📋 /menu — Barcha imkoniyatlarni ko'rish")

# =====================
# BOTNI ISHGA TUSHIRISH
# =====================

print("Bot ishlamoqda... ✅")
bot.polling()