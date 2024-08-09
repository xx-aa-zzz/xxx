from telethon import TelegramClient, events
from rembg import remove
from PIL import Image
import io

# بيانات الاعتماد الخاصة بك
api_id = 26222032
api_hash = 'd7969684a520bd4dcb36701ac48be730'
bot_token = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

client = TelegramClient('remove_bg_bot', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('مرحبًا! أرسل لي صورة وسأزيل الخلفية منها.')

@client.on(events.NewMessage(pattern='/?'))
async def remove_bg(event):
    if event.photo:
        await event.respond('جاري العمل على صورتك...')
        
        # تحميل الصورة
        original_image = await event.download_media(file=bytes)

        # إزالة الخلفية
        input_image = Image.open(io.BytesIO(original_image))
        output_image = remove(input_image)

        # حفظ الصورة بدون خلفية في الذاكرة بصيغة JPG
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='JPEG') 
        img_byte_arr = img_byte_arr.getvalue()

        # إرسال الصورة بدون خلفية مع تحديد نوع الملف
        await event.respond(file=img_byte_arr, message='الصورة بدون خلفية:')

    else:
        await event.respond('الرجاء إرسال صورة.')

client.start(bot_token=bot_token)
client.run_until_disconnected()
