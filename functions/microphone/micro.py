import speech_recognition as sr
from functions.keyboard.keyboards import speak

def recognize_speech():
    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 0.5 
    recognizer.energy_threshold = 200  
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language='vi-VN')
            speak(f"Bạn đã nói: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            speak("Xin vui lòng nói...")
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            speak(f"Không thể kết nối đến dịch vụ nhận dạng giọng nói: {e}")
            return None

def check():
    original_input = None
    while True:
        if not original_input:
            original_input = recognize_speech()
        
        if original_input:
            speak(f"Có phải bạn vừa nói {original_input} không?")
            speak("Trả lời 'phải rồi' hoặc 'không phải' để xác nhận.")
            
            confirmation = recognize_speech()

            if confirmation == "phải rồi":
                speak("Cảm ơn, chúng ta tiếp tục.")
                return original_input
            elif confirmation == "không phải":
                speak("Hãy nói lại.")
                original_input = None  
            else:
                speak("Xin lỗi, tôi không hiểu. Hãy xác nhận lại.")
        else:
            speak("Xin lỗi, tôi không nghe rõ. Hãy thử lại.")
            original_input = None 



