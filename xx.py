from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeFilename
from PIL import Image, ImageDraw, ImageFont
import io

# إعدادات البوت
api_id = '26222032'
api_hash = 'd7969684a520bd4dcb36701ac48be730'
bot_token = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

client = TelegramClient('thumbnail_bot', api_id, api_hash).start(bot_token=bot_token)

# المتغيرات لتخزين المدخلات
user_image = None
user_font = None
user_text = None

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("مرحباً! أنا بوت لإنشاء صور مصغرة. أرسل لي صورة، ثم ملف خط (.ttf)، ثم الجملة التي تريد إضافتها.")

@client.on(events.NewMessage)
async def handle_message(event):
    global user_image, user_font, user_text

    # استلام الصورة
    if event.photo:
        user_image = await event.download_media(file=bytes)
        await event.reply("تم استلام الصورة. الآن، أرسل لي ملف الخط (.ttf).")

    # استلام ملف الخط
    elif event.file and event.file.name.endswith('.ttf'):
        user_font = await event.download_media(file=bytes)
        await event.reply("تم استلام ملف الخط. الآن، أرسل لي الجملة التي تريد إضافتها.")

    # استلام النص
    elif event.raw_text and user_image and user_font:
        user_text = event.raw_text

        # إنشاء الصورة المصغرة
        image = Image.open(io.BytesIO(user_image))
        draw = ImageDraw.Draw(image)
        
        # إعداد الخط
        font = ImageFont.truetype(io.BytesIO(user_font), size=50)
        
        # حساب حجم النص وتحديد الموقع
        text_width, text_height = draw.textsize(user_text, font=font)
        width, height = image.size
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        # إضافة النص للصورة
        draw.text(position, user_text, font=font, fill="white")
        
        # حفظ الصورة
        output = io.BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        
        # إرسال الصورة للمستخدم
        await client.send_file(event.chat_id, output, caption="هذه هي الصورة المصغرة الخاصة بك!")

        # إعادة تعيين المتغيرات
        user_image = None
        user_font = None
        user_text = None

    else:
        await event.reply("يرجى التأكد من إرسال صورة، ملف خط (.ttf)، ونص.")

client.run_until_disconnected()
        
