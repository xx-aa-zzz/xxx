import os
from pathlib import Path
import telebot
from openai import OpenAI
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تعيين التوكن الخاص ببوت تليجرام
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA')
if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN is not set")
    raise ValueError("TELEGRAM_BOT_TOKEN is not set")

# تعيين مفتاح API الخاص بـ OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'o.Wp9Sy0RxEDzRozPCFLvGoZEuS9IdJtsU')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set")
    raise ValueError("OPENAI_API_KEY is not set")

# إنشاء كائن البوت
bot = telebot.TeleBot(BOT_TOKEN)

# إنشاء عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logger.info(f"Received message: {message.text}")
    user_text = message.text
    
    try:
        logger.info("Sending request to OpenAI for text-to-speech conversion")
        
        # إنشاء مسار الملف الصوتي
        speech_file_path = Path("speech.mp3")
        
        # تحويل النص إلى كلام
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=user_text
        )
        
        # حفظ الملف الصوتي
        response.stream_to_file(speech_file_path)
        
        logger.info(f"Audio file created: {speech_file_path}")
        
        # إرسال الملف الصوتي للمستخدم
        with open(speech_file_path, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)
        logger.info("Sent audio file to user")
        
        # حذف الملف الصوتي بعد الإرسال
        speech_file_path.unlink()
        logger.info("Deleted audio file")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        bot.reply_to(message, f"عذرًا، حدث خطأ أثناء معالجة طلبك: {str(e)}")

# تشغيل البوت
if __name__ == '__main__':
    logger.info("Starting bot polling")
    bot.polling()
