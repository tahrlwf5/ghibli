import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# قم بتعديل القيم التالية بمعلوماتك الشخصية
TELEGRAM_BOT_TOKEN = "5146976580:AAE2yXc-JK6MIHVlLDy-O4YODucS_u7Zq-8"  # أدخل توكن بوت تيليغرام هنا
PDFCO_API_KEY = "taheralnoori19999@gmail.com_lSK922RljsYJ2iMsB4zxCs24nCKXWluDVYBjrNTdaUfQAJffQcXigq7FS2KWmhge"

def translate_pdf(file_url, lang_from="en", lang_to="ar", name="translated_pdf"):
    """
    ترسل هذه الدالة طلب ترجمة ملف PDF إلى pdf.co API.
    """
    api_url = "https://api.pdf.co/v1/pdf/translate"
    payload = {
        "url": file_url,
        "name": name,
        "langFrom": lang_from,
        "langto": lang_to,  # لاحظ أن اسم المعامل مطابق للوثائق (langto بحرف t صغير)
        "async": False
    }
    headers = {
        "x-api-key": PDFCO_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def start(update: Update, context: CallbackContext):
    """
    دالة بدء المحادثة، ترسل رسالة ترحيبية للمستخدم.
    """
    update.message.reply_text("مرحباً! أرسل لي ملف PDF للترجمة.")

def handle_document(update: Update, context: CallbackContext):
    """
    دالة معالجة الرسائل التي تحتوي على ملفات PDF.
    """
    document = update.message.document
    if document.mime_type != "application/pdf":
        update.message.reply_text("يرجى إرسال ملف PDF فقط.")
        return

    # الحصول على الملف من تيليغرام
    file = document.get_file()
    file_url = file.file_path

    update.message.reply_text("جاري ترجمة الملف... انتظر قليلاً.")

    # استدعاء دالة الترجمة مع تحديد لغة المصدر والهدف
    result = translate_pdf(file_url, lang_from="en", lang_to="ar", name="translated_pdf")

    if not result.get("error", True):
        translated_file_url = result.get("url")
        update.message.reply_text(f"تمت الترجمة بنجاح!\nيمكنك تحميل الملف من الرابط التالي:\n{translated_file_url}")
    else:
        error_message = result.get("message", "حدث خطأ أثناء الترجمة.")
        update.message.reply_text(f"فشل الترجمة: {error_message}")

def main():
    # إنشاء Updater مع استخدام سياق (context) الإصدارة 13.15
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # إضافة معالج الأوامر والرسائل
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/pdf"), handle_document))
    
    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
