import speech_recognition as sr
from functions.keyboard.keyboards import speak
import keyboard

def recognize_speech():
    recognizer = sr.Recognizer()

    # Cấu hình ngưỡng năng lượng và khoảng dừng
    recognizer.pause_threshold = 1.3  # Tăng thời gian chờ trước khi xác định ngừng nói
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Điều chỉnh tự động
        speak("Xin mời bạn nói...")
        
        try:
            # Loại bỏ phrase_time_limit để thu âm không bị giới hạn thời gian
            audio = recognizer.listen(source, timeout=15)
            text = recognizer.recognize_google(audio, language='vi-VN')
            speak(f"Bạn đã nói: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            speak("Bạn không nói gì. Xin vui lòng thử lại.")
            return None
        except sr.UnknownValueError:
            speak("Xin lỗi, tôi không nghe rõ. Hãy thử nói lại.")
            return None
        except sr.RequestError as e:
            speak(f"Lỗi kết nối đến dịch vụ nhận dạng giọng nói: {e}")
            return None
def recognize_keypress():
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            return event.name
def check():
    original_input = None

    # Nhận diện giọng nói và xác nhận đầu vào
    while not original_input:
        original_input = recognize_speech()

        if original_input:
            speak(f"Có phải bạn vừa nói '{original_input}' không?")
            speak("Nếu đúng hãy nói 'Phải rồi' hoặc nhấn phím 1. Nếu sai hãy nói 'Không phải' hoặc nhấn phím 2.")

            # Chờ xác nhận
            while True:
                confirmation = recognize_speech() or recognize_keypress()

                if confirmation in ["phải rồi", "1"]:
                    speak("Cảm ơn thông tin đã được xác nhận.")
                    return original_input
                elif confirmation in ["không phải", "2"]:
                    speak("Vui lòng thử lại.")
                    original_input = None  # Yêu cầu nhập lại
                    break
                else:
                    speak("Tôi không hiểu. Hãy nói 'Phải rồi' hoặc 'Không phải' hoặc nhấn phím 1 hoặc 2.")
