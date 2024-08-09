from telethon import TelegramClient, events
from PIL import Image, ImageDraw, ImageFont
import io

# إعدادات البوت
api_id = 26222032
api_hash = 'd7969684a520bd4dcb36701ac48be730'
bot_token = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

# إنشاء العميل (Client) للبوت
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# التعامل مع بدء المحادثة
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("مرحباً! أنا بوت لإنشاء صور مصغرة. أرسل لي صورة، ثم ملف خط (.ttf)، ثم الجملة التي تريد إضافتها.")
    raise events.StopPropagation

# استقبال الصورة من المستخدم
@bot.on(events.NewMessage(func=lambda e: e.photo))
async def handle_photo(event):
    await event.respond("تم استقبال الصورة! الآن أرسل لي ملف الخط (.ttf).")
    # تحميل الصورة وحفظها
    photo = await event.download_media(file=io.BytesIO())
    event.client._photo = photo  # حفظ الصورة في العميل

# استقبال ملف الخط من المستخدم
@bot.on(events.NewMessage(func=lambda e: e.file and e.file.name.endswith('.ttf')))
async def handle_font(event):
    await event.respond("تم استقبال ملف الخط! الآن أرسل لي النص الذي تريد إضافته على الصورة.")
    # تحميل ملف الخط وحفظه
    font_file = await event.download_media(file=io.BytesIO())
    event.client._font = font_file  # حفظ ملف الخط في العميل

# استقبال النص من المستخدم
@bot.on(events.NewMessage(func=lambda e: e.text))
async def handle_message(event):
    user_text = event.text
    await event.respond("جاري معالجة الصورة...")

    try:
        # تحميل الصورة والخط من الذاكرة
        image = Image.open(event.client._photo)
        font = ImageFont.truetype(io.BytesIO(event.client._font), size=40)

        # إعداد النص
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textbbox((0, 0), user_text, font=font)[2:]
        width, height = image.size
        position = ((width - text_width) // 2, (height - text_height) // 2)

        # إضافة النص على الصورة
        draw.text(position, user_text, font=font, fill="white")

        # حفظ الصورة المصغرة
        output = io.BytesIO()
        image.save(output, format='PNG')
        output.seek(0)

        # إرسال الصورة المعدلة للمستخدم
        await event.respond("تم إنشاء الصورة المصغرة:", file=output)

    except Exception as e:
        await event.respond(f"حدث خطأ أثناء معالجة الصورة: {str(e)}")

# بدء البوت
bot.run_until_disconnected()
        
