from telethon import TelegramClient, events, Button
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# إعدادات البوت
API_ID = os.getenv('26222032')
API_HASH = os.getenv('d7969684a520bd4dcb36701ac48be730')
BOT_TOKEN = os.getenv('7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA')

# التحقق من وجود المتغيرات البيئية
if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("يرجى التأكد من تعيين جميع المتغيرات البيئية المطلوبة.")

# إنشاء العميل (Client) للبوت
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# تخزين البيانات في ذاكرة البوت
user_data = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_message = (
        "مرحباً! أنا بوت لإنشاء صور مصغرة احترافية. إليك الخطوات:\n\n"
        "1. أرسل لي الصورة\n"
        "2. أرسل ملف الخط (.ttf)\n"
        "3. أرسل النص المراد إضافته\n"
        "4. اختر الإعدادات المتقدمة (اختياري)\n\n"
        "لنبدأ! أرسل لي الصورة الآن."
    )
    await event.respond(welcome_message)

@bot.on(events.NewMessage(func=lambda e: e.photo))
async def handle_photo(event):
    sender = await event.get_sender()
    user_id = sender.id
    user_data[user_id] = {'step': 'font'}
    
    photo = await event.download_media(file=io.BytesIO())
    user_data[user_id]['photo'] = Image.open(photo)
    await event.respond("تم استلام الصورة! الآن أرسل لي ملف الخط (.ttf).")

@bot.on(events.NewMessage(func=lambda e: e.document and e.document.mime_type == 'font/ttf'))
async def handle_font(event):
    sender = await event.get_sender()
    user_id = sender.id
    
    if user_id not in user_data or user_data[user_id]['step'] != 'font':
        await event.respond("يرجى إرسال الصورة أولاً.")
        return
    
    user_data[user_id]['step'] = 'text'
    font_file = await event.download_media(file=io.BytesIO())
    user_data[user_id]['font'] = font_file.getvalue()
    await event.respond("تم استلام ملف الخط! الآن أرسل لي النص الذي تريد إضافته على الصورة.")

@bot.on(events.NewMessage(func=lambda e: e.text and not e.text.startswith('/')))
async def handle_message(event):
    sender = await event.get_sender()
    user_id = sender.id
    
    if user_id not in user_data or user_data[user_id]['step'] != 'text':
        await event.respond("يرجى إرسال الصورة وملف الخط أولاً.")
        return
    
    user_data[user_id]['text'] = event.text
    user_data[user_id]['step'] = 'settings'
    
    # إنشاء أزرار للإعدادات المتقدمة
    buttons = [
        [Button.inline("تغيير حجم الخط", b"font_size"),
         Button.inline("تغيير لون الخط", b"font_color")],
        [Button.inline("إضافة ظل للنص", b"text_shadow"),
         Button.inline("تأثيرات على الصورة", b"image_effects")],
        [Button.inline("إنشاء الصورة", b"create_image")]
    ]
    
    await event.respond("تم استلام النص! هل ترغب في تعديل أي إعدادات متقدمة؟", buttons=buttons)

@bot.on(events.CallbackQuery())
async def handle_callback(event):
    sender = await event.get_sender()
    user_id = sender.id
    
    if user_id not in user_data:
        await event.answer("حدث خطأ. يرجى بدء العملية من جديد.")
        return
    
    data = event.data.decode()
    
    if data == "font_size":
        user_data[user_id]['step'] = 'font_size'
        await event.respond("أدخل حجم الخط (مثال: 40)")
    elif data == "font_color":
        user_data[user_id]['step'] = 'font_color'
        await event.respond("أدخل لون الخط بصيغة HEX (مثال: #FFFFFF للون الأبيض)")
    elif data == "text_shadow":
        user_data[user_id]['text_shadow'] = not user_data[user_id].get('text_shadow', False)
        await event.answer(f"{'تم تفعيل' if user_data[user_id]['text_shadow'] else 'تم إلغاء'} ظل النص")
    elif data == "image_effects":
        user_data[user_id]['step'] = 'image_effects'
        await event.respond("اختر تأثير: blur, sharpen, contrast")
    elif data == "create_image":
        await create_image(event, user_id)

async def create_image(event, user_id):
    try:
        photo_data = user_data[user_id]['photo']
        font_data = user_data[user_id]['font']
        user_text = user_data[user_id]['text']

        # تطبيق الإعدادات المتقدمة
        font_size = user_data[user_id].get('font_size', 40)
        font_color = user_data[user_id].get('font_color', "white")
        text_shadow = user_data[user_id].get('text_shadow', False)
        image_effect = user_data[user_id].get('image_effect', None)

        # تطبيق تأثيرات الصورة
        if image_effect == 'blur':
            photo_data = photo_data.filter(ImageFilter.BLUR)
        elif image_effect == 'sharpen':
            photo_data = photo_data.filter(ImageFilter.SHARPEN)
        elif image_effect == 'contrast':
            enhancer = ImageEnhance.Contrast(photo_data)
            photo_data = enhancer.enhance(1.5)

        # تحميل الخط
        font = ImageFont.truetype(io.BytesIO(font_data), size=font_size)

        # إعداد النص
        draw = ImageDraw.Draw(photo_data)
        text_width, text_height = draw.textbbox((0, 0), user_text, font=font)[2:]
        width, height = photo_data.size
        position = ((width - text_width) // 2, (height - text_height) // 2)

        # إضافة ظل للنص إذا تم تفعيله
        if text_shadow:
            shadow_color = "black"
            shadow_position = (position[0] + 2, position[1] + 2)
            draw.text(shadow_position, user_text, font=font, fill=shadow_color)

        # إضافة النص على الصورة
        draw.text(position, user_text, font=font, fill=font_color)

        # حفظ الصورة المصغرة
        output = io.BytesIO()
        photo_data.save(output, format='PNG')
        output.seek(0)

        # إرسال الصورة المعدلة للمستخدم
        await bot.send_file(event.chat_id, output, caption="تم إنشاء الصورة المصغرة:", file_name="thumbnail.png")

        # تنظيف بيانات المستخدم
        del user_data[user_id]

    except Exception as e:
        await event.respond(f"حدث خطأ أثناء معالجة الصورة: {str(e)}")
        del user_data[user_id]

# بدء البوت
if __name__ == "__main__":
    print("جاري تشغيل البوت...")
    bot.run_until_disconnected()
