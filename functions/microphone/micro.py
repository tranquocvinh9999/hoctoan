import speech_recognition as sr
from functions.keyboard.keyboards import speak

def recognize_speech():
    recognizer = sr.Recognizer()


    recognizer.pause_threshold = 0.8  
    recognizer.energy_threshold = 300 

    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            speak("Xin vui lòng nói...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio, language='vi-VN')
            speak(f"Bạn đã nói: {text}")
            return text
        except sr.UnknownValueError:
            speak("Xin lỗi, tôi không thể nhận dạng được âm thanh.")
            return None
        except sr.RequestError as e:
            speak(f"Không thể kết nối đến dịch vụ nhận dạng: {e}")
            return None
if __name__ == "__main__":
    recognized_text = recognize_speech()
