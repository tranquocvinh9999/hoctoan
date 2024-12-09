import speech_recognition as sr
from functions.keyboard.keyboards import speak
from functions.resource_path.path import resource_path
import keyboard  

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


def recognize_keypress():
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN: 
        return event.name  
def check():
    original_input = None
    while True:
        if not original_input:
            original_input = recognize_speech()
        
        if original_input:
            speak(f"Có phải bạn vừa nói {original_input} không?")
            speak("Nhấn phím 1 để xác nhận 'đúng', nhấn phím 2 để xác nhận 'sai'.")
            
            confirmation = recognize_keypress() 

            if confirmation == "1": 
                speak("Cảm ơn, chúng ta tiếp tục.")
                return original_input
            elif confirmation == "2": 
                speak("Hãy nói lại.")
                original_input = None  
            else:
                speak("Xin lỗi, tôi không hiểu. Hãy xác nhận lại bằng cách nhấn phím 1 hoặc 2.")
        else:
            speak("Xin lỗi, tôi không nghe rõ. Hãy thử lại.")
            original_input = None



