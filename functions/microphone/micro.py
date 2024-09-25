import speech_recognition as sr
from functions.keyboard.keyboards import speak

def recognize_speech():
    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 0.8  
    recognizer.energy_threshold = 300 
    with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)

            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language='vi-VN')
                speak(f"Bạn đã nói: {text}")
                return text
            except sr.WaitTimeoutError:
                speak("Xin vui lòng nói...")
                audio = recognizer.listen(source, phrase_time_limit=5)
                try:
                    text = recognizer.recognize_google(audio, language='vi-VN')
                    speak(f"Bạn đã nói: {text}")
                    return text
                except sr.UnknownValueError:
                    speak("Xin lỗi, tôi không thể nhận dạng được âm thanh.")
                    recognize_speech()
                    return None
                except sr.RequestError as e:
                    speak(f"Không thể kết nối đến microphone: {e}")
                    return None
            except sr.UnknownValueError:
                speak("Xin lỗi, tôi không thể nhận dạng được âm thanh.")
                recognize_speech()
                return None
            except sr.RequestError as e:
                speak(f"Không thể kết nối đến microphone: {e}")
                return None


def check():
    k = recognize_speech()
    speak(f"Có phải bạn vừa nói {k} không")
    speak(f"phải rồi hoặc là không phải để nói lại")
    ntn = recognize_speech()
    if ntn == None:
        recognize_speech()
    elif ntn == "phải rồi":
        return k
    elif ntn == "không phải":
        recognize_speech()