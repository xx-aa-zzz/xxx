import requests
import telebot

# استبدل بالقيم الحقيقية
API_KEY = 'bAfJgNmJJaaL5C0GCUVgdELzcQRgim5Y38H5kLcL212oDM6nca9beqheympb'
BOT_TOKEN = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

bot = telebot.TeleBot(BOT_TOKEN)

def generate_image(prompt):
    url = 'https://api.modelslab.com/v1/text-to-image'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    data = {'prompt': prompt}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['imageUrl']
    else:
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا! أرسل لي نصًا وسأقوم بإنشاء صورة بناءً عليه.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    prompt = message.text
    bot.send_message(message.chat.id, "جاري إنشاء الصورة، انتظر قليلاً...")

    image_url = generate_image(prompt)

    if image_url:
        bot.send_photo(message.chat.id, image_url)
    else:
        bot.send_message(message.chat.id, "حدث خطأ أثناء إنشاء الصورة. حاول مرة أخرى لاحقًا.")

bot.infinity_polling()
