import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from gemini_python_api import GeminiAPI

# بيانات اعتماد Gemini API
GEMINI_API_KEY = 'AIzaSyAO1n7OWzbpFaNuEuNlDwkNampa_n-II40'
GEMINI_API_SECRET = '' # قد تحتاج إلى مفتاح سري، تحقق من وثائق Gemini API

# رمز بوت Telegram
BOT_TOKEN = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

# استبدل 'your_gemini_function' بالدالة التي تتفاعل مع Gemini API
def your_gemini_function(user_input):
    gemini_api = GeminiAPI(GEMINI_API_KEY, GEMINI_API_SECRET) # قم بتوفير المفتاح السري إذا لزم الأمر
    response = gemini_api.generate_text(user_input)
    return response.text

# تعريف الأوامر التي يستجيب لها البوت
def start(update, context):
    update.message.reply_text('مرحباً! كيف يمكنني مساعدتك اليوم؟')

def echo(update, context):
    user_input = update.message.text
    gemini_response = your_gemini_function(user_input)
    update.message.reply_text(gemini_response)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # تسجيل الأوامر التي يستجيب لها البوت
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.text & ~filters.command, echo)) # تم تغيير Filters إلى filters

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
