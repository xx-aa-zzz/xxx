import os
import telebot
import openai
from telebot.types import Message

# تعيين التوكن الخاص ببوت تليجرام
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA')

# تعيين مفتاح API الخاص بـ ChatGPT
openai.api_key = os.getenv('OPENAI_API_KEY', 'o.Wp9Sy0RxEDzRozPCFLvGoZEuS9IdJtsU')

# إنشاء كائن البوت
bot = telebot.TeleBot(BOT_TOKEN)

# قراءة قواعد هندسة الأوامر من متغير بيئي
prompt_engineering_rules = os.getenv('PROMPT_ENGINEERING_RULES', '''
العنصر الأول : المُهمّة الـTask
المهمة الثانية : الفلترة
المهمة الثالثة : الإستنباط
العنصر الثاني : السياق الـ Context
العنصر الثالث : الأدوار
العنصر الرابع : مؤشر المخرجات Output Indicator
العنصر الخامس : المدخلات Input Data

تقنيات التلقين Prompting Techniques :

1. Zero-Shot Prompting
2. Few-Shot Prompting
3. Chain-of-Thought Prompting
4. Self-Consistency Prompting
5. Role-Playing
6. Instruction Refinement
7. Constrained Generation
8. Context Priming
9. Template-based Prompting
10. Analogical Reasoning
11. Step-by-Step Analysis
12. Multi-turn Querying
13. Goal-oriented Prompting
14. Self-verification
15. Parallel Thinking
''')

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
