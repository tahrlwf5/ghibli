import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# معلومات البوت و API
TELEGRAM_BOT_TOKEN = "5146976580:AAE2yXc-JK6MIHVlLDy-O4YODucS_u7Zq-8"  # أدخل توكن بوت تيليغرام هنا
PDFCO_API_KEY = "taheralnoori19999@gmail.com_lSK922RljsYJ2iMsB4zxCs24nCKXWluDVYBjrNTdaUfQAJffQcXigq7FS2KWmhge"

def upload_to_pdfco(file_path):
    """تحميل ملف إلى pdf.co للحصول على رابط مباشر"""
    api_url = "https://api.pdf.co/v1/file/upload"
    headers = {"x-api-key": PDFCO_API_KEY}
    files = {"file": open(file_path, "rb")}

    response = requests.post(api_url, files=files, headers=headers)
    result = response.json()

    if result.get("error", True) is False:
        return result.get("url")  # رابط الملف القابل للوصول
    return None

def translate_pdf(file_url, lang_from="en", lang_to="ar", name="translated_pdf"):
    """إرسال طلب ترجمة PDF إلى pdf.co"""
    api_url = "https://api.pdf.co/v1/pdf/translate"
    payload = {
        "url": file_url,
        "name": name,
        "langFrom": lang_from,
        "langTo": lang_to,  # ملاحظة: T كبيرة
        "async": False
    }
    headers = {
        "x-api-key": PDFCO_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def start(update: Update, context: CallbackContext):
    """ترحيب المستخدم عند بدء البوت"""
    update.message.reply_text("مرحباً! أرسل لي ملف PDF لترجمته.")

def handle_document(update: Update, context: CallbackContext):
    """معالجة ملفات PDF المرسلة"""
    document = update.message.document
    if document.mime_type != "application/pdf":
        update.message.reply_text("يرجى إرسال ملف PDF فقط.")
        return

    file = document.get_file()
    file_path = file.download()  # تحميل الملف محلياً

    update.message.reply_text("جاري رفع الملف للترجمة...")

    # رفع الملف إلى pdf.co أولاً
    file_url = upload_to_pdfco(file_path)
    if not file_url:
        update.message.reply_text("فشل رفع الملف إلى pdf.co، حاول مرة أخرى.")
        return

    update.message.reply_text("جاري ترجمة الملف... انتظر قليلاً.")

    # استدعاء دالة الترجمة
    result = translate_pdf(file_url, lang_from="en", lang_to="ar")

    if not result.get("error", True):
        translated_file_url = result.get("url")
        update.message.reply_text(f"تمت الترجمة بنجاح!\nيمكنك تحميل الملف من الرابط التالي:\n{translated_file_url}")
    else:
        error_message = result.get("message", "حدث خطأ أثناء الترجمة.")
        update.message.reply_text(f"فشل الترجمة: {error_message}")

def main():
    """بدء تشغيل البوت"""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("application/pdf"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
