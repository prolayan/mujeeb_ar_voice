import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
import os
import sys

# الردود الجاهزة (تقدر تضيف أي عدد)
replies = [
    (["كم رصيدي", "ما هو رصيدي", "ايش رصيدي"], "رصيدك الحالي هو ١٥٬٠٠٠ ريال."),
    (["حول", "ارسل"], "تم تحويل المبلغ بنجاح."),
    (["سدد فاتورة", "ادفع فاتورة"], "تم تسديد الفاتورة بنجاح."),
    (["مرحبا", "السلام عليكم", "هلا"], "مرحباً بك في بنك الإنماء، كيف أقدر أخدمك؟"),
    (["شكرا", "شكراً", "مشكور"], "العفو، في خدمتك دائماً."),
    (["وداعا", "مع السلامة", "باي"], "مع السلامة، نتمنى لك يوماً سعيداً."),
]

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import speech_recognition
        import gtts
        import playsound
        print("✅ جميع المكتبات المطلوبة متوفرة")
        return True
    except ImportError as e:
        print(f"❌ مكتبة مفقودة: {e}")
        print("قم بتثبيت المكتبات المطلوبة:")
        print("py -m pip install SpeechRecognition gtts playsound PyAudio")
        return False

def recognize_arabic():
    """Recognize Arabic speech from microphone"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("\n🎤 تكلم الآن (أو قل 'خروج' للإنهاء)...")
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            text = recognizer.recognize_google(audio, language='ar-SA')
            print(f"🎯 أنت قلت: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ لم أستطع فهم ما قلته. حاول مرة أخرى.")
            return ""
        except sr.RequestError as e:
            print(f"❌ خطأ في خدمة التعرف على الصوت: {e}")
            return ""
            
    except Exception as e:
        print(f"❌ خطأ في الوصول للميكروفون: {e}")
        print("تأكد من أن الميكروفون متصل ويعمل بشكل صحيح.")
        return ""

def reply_arabic(text):
    """Generate and play Arabic reply"""
    # ذكاء اصطناعي وهمي: يبحث عن رد جاهز
    reply = "عذراً، لم أفهم طلبك. جرب أمر آخر مثل 'كم رصيدي' أو 'مرحبا'."
    
    for patterns, r in replies:
        for pattern in patterns:
            if pattern in text:
                reply = r
                break
        if reply != "عذراً، لم أفهم طلبك. جرب أمر آخر مثل 'كم رصيدي' أو 'مرحبا'.":
            break
    
    print(f"🤖 مجيب: {reply}")
    
    try:
        # تحويل الرد إلى صوت وتشغيله
        tts = gTTS(text=reply, lang='ar', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_file = fp.name
        
        tts.save(temp_file)
        playsound(temp_file)
        os.remove(temp_file)
        
    except Exception as e:
        print(f"❌ خطأ في تحويل النص إلى صوت: {e}")
        print("تأكد من وجود اتصال بالإنترنت للوصول لخدمة Google Text-to-Speech.")

def show_help():
    """Show available commands"""
    print("\n📋 الأوامر المتاحة:")
    print("• 'كم رصيدي' - عرض الرصيد")
    print("• 'حول' أو 'ارسل' - تحويل مبلغ")
    print("• 'سدد فاتورة' - دفع فاتورة")
    print("• 'مرحبا' - تحية")
    print("• 'شكرا' - شكر")
    print("• 'وداعا' - إنهاء البرنامج")
    print("• 'خروج' أو 'قف' - إنهاء البرنامج")

def main():
    """Main function"""
    print("🎉 مرحباً بك في مجيب - المساعد الصوتي العربي!")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Show help
    show_help()
    
    # Main loop
    while True:
        try:
            text = recognize_arabic()
            
            if text.strip() == "":
                continue
                
            # Check for exit commands
            if any(x in text for x in ["خروج", "انهاء", "قف", "اخرج", "وداعا", "مع السلامة", "باي"]):
                print("👋 تم الإنهاء. مع السلامة!")
                break
            
            # Check for help command
            if any(x in text for x in ["مساعدة", "ساعدني", "help", "help me"]):
                show_help()
                continue
            
            reply_arabic(text)
            
        except KeyboardInterrupt:
            print("\n👋 تم الإنهاء بواسطة المستخدم. مع السلامة!")
            break
        except Exception as e:
            print(f"❌ خطأ غير متوقع: {e}")
            print("جاري إعادة المحاولة...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ خطأ في تشغيل البرنامج: {e}")
        input("اضغط Enter للخروج...")
