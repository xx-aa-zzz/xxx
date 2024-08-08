import cv2
import os
import shutil
import random
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توكن البوت الخاص بك
TOKEN = '7328901491:AAGoXuqwNQg7POYIQJF602Pb6eoo8dw7vyA'

# الوظيفة المسؤولة عن بدء المحادثة
def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبًا! أرسل لي فيديو وسأقوم بإنشاء صورة مصغرة منه.")

# الوظيفة المسؤولة عن استقبال الفيديو ومعالجته
def handle_video(update: Update, context: CallbackContext):
    video_file = update.message.video
    video_path = video_file.get_file().download()

    # استدعاء وظيفة معالجة الفيديو
    thumbnail_path = process_video(video_path, "النص الخاص بك هنا")
    
    if thumbnail_path:
        # إرسال الصورة المصغرة للمستخدم
        update.message.reply_photo(photo=open(thumbnail_path, 'rb'))
    else:
        update.message.reply_text("حدث خطأ أثناء معالجة الفيديو.")

# الوظيفة التي تقوم بمعالجة الفيديو وإنشاء الصورة المصغرة
def process_video(video_path, text):
    try:
        # مسار حفظ الصورة المصغرة
        thumbnail_dir = 'thumbnails'
        os.makedirs(thumbnail_dir, exist_ok=True)
        thumbnail_path = os.path.join(thumbnail_dir, 'thumbnail.jpg')

        # قراءة الفيديو
        cap = cv2.VideoCapture(video_path)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

                for (sx, sy, sw, sh) in smiles:
                    # اقتصاص الوجه
                    face_img = frame[y:y+h, x:x+w]
                    face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))

                    # إضافة خلفية ونص
                    background = Image.new('RGB', (w, h + 50), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    background.paste(face_pil, (0, 50))
                    
                    draw = ImageDraw.Draw(background)
                    font = ImageFont.load_default()
                    draw.text((10, 10), text, font=font, fill=(255, 255, 255))
                    
                    background.save(thumbnail_path)
                    return thumbnail_path
        
        cap.release()
        return None

    except Exception as e:
        print(f"Error processing video: {e}")
        return None

# الوظيفة الرئيسية لتشغيل البوت
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
