import os
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont

# حدد رمز الوصول الخاص بك من BotFather
TOKEN = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

# حدد المسارات للخلفيات والخطوط
BASE_PATH = os.path.abspath(".")
BACKGROUND_DIR = os.path.join(BASE_PATH, "backgrounds")
FONT_DIR = os.path.join(BASE_PATH, "font")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="مرحبا! أنا بوت لإنشاء صور مصغرة. أرسل لي صورة وسأضيف لها خلفية عشوائية.")

def add_background(img, font_path):
    # فتح الصورة
    img = Image.open(img).convert("RGBA")

    # إضافة خلفية عشوائية
    background = Image.open(os.path.join(BACKGROUND_DIR, random.choice(os.listdir(BACKGROUND_DIR)))).convert("RGBA")
    W, H = (1280, 720)
    background = background.resize((W, H), Image.Resampling.LANCZOS)

    # إضافة الصورة إلى الخلفية
    x = random.uniform(0, 1)
    if x >= 0.5:
        img = img.rotate(25)
    else:
        img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        img = img.rotate(-25)

    newimg = Image.new('RGBA', size=(W, H), color=(0, 0, 0, 0))
    newimg.paste(background, (0, 0))
    newimg.paste(img, (-120, -120), img)

    # إضافة نص عشوائي
    title_font = ImageFont.truetype(font_path, 80)
    title_text = "نص عشوائي"
    image_editable = ImageDraw.Draw(newimg)
    bbox = image_editable.textbbox((0, 0), title_text, font=title_font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    image_editable.text(((W - w) / 2, (H - h) - 75), title_text, (255, 255, 255), font=title_font, stroke_width=10, stroke_fill=(0, 0, 0))

    return newimg

def handle_photo(update, context):
    # تحميل الصورة المرسلة
    photo_file = update.message.photo[-1].get_file()
    photo_file.download("image.jpg")

    # إضافة خلفية عشوائية
    font_path = os.path.join(FONT_DIR, random.choice(os.listdir(FONT_DIR)))
    output_image = add_background("image.jpg", font_path)

    # إرسال الصورة النهائية
    with open("output.jpg", "wb") as f:
        output_image.save(f, "JPEG")
    with open("output.jpg", "rb") as f:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add the handlers here

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
