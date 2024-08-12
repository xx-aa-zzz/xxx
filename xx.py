import os
import telebot
import openai
from telebot.types import Message

# تعيين التوكن الخاص ببوت تليجرام
BOT_TOKEN = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

# تعيين مفتاح API الخاص بـ ChatGPT
openai.api_key = 'o.Wp9Sy0RxEDzRozPCFLvGoZEuS9IdJtsU'

# إنشاء كائن البوت
bot = telebot.TeleBot(BOT_TOKEN)

# قراءة محتوى ملف قواعد هندسة الأوامر
with open('هندسة الاوامر.txt', 'r', encoding='utf-8') as file:
    prompt_engineering_rules = file.read()

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    user_prompt = message.text
    
    # إنشاء سياق للمطالبة المحسنة
    system_message = f"""أنت مساعد متخصص في تحسين المطالبات (prompts). استخدم القواعد التالية لتحسين المطالبة المقدمة:

{prompt_engineering_rules}

قم بتحليل المطالبة المقدمة وتحسينها باستخدام هذه القواعد والتقنيات. قدم المطالبة المحسنة مع شرح موجز للتحسينات التي تم إجراؤها."""

    try:
        # استخدام ChatGPT لتحسين المطالبة
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"قم بتحسين هذه المطالبة: {user_prompt}"}
            ]
        )
        
        improved_prompt = response.choices[0].message.content
        
        # إرسال المطالبة المحسنة للمستخدم
        bot.reply_to(message, improved_prompt)
    except Exception as e:
        bot.reply_to(message, f"عذرًا، حدث خطأ أثناء معالجة طلبك: {str(e)}")

# تشغيل البوت
if __name__ == '__main__':
    bot.polling()
