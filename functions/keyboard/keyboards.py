import os
import json
import threading
import queue
from gtts import gTTS
import pygame
from functions.resource_path.path import resource_path

# Load settings at the start
config_path = resource_path("config/data.json")
with open(config_path) as f:
    setting = json.load(f)
    file_counter = setting.get("filecount", 0)

# Cache dictionary to store pre-generated MP3 files
cache = {}

# Lock to prevent race condition on cache
cache_lock = threading.Lock()

# Initialize pygame mixer once
pygame.mixer.init(frequency=22050, size=-16, channels=2)  # Ensure proper initialization

# Queue for sequential sound playing
sound_queue = queue.Queue()

# Event to signal when speech has finished
speech_done_event = threading.Event()

def get_next_file_name():
    """Generate the next file name based on the counter."""
    global file_counter
    file_counter += 1
    return resource_path(f'stuff/temp_{file_counter}.mp3')

def save_counter():
    """Save the updated counter to the config file."""
    with open(config_path, "w") as f:
        json.dump({"filecount": file_counter}, f)

def play_sound(file_path):
    """Play the sound synchronously, ensuring no interruption."""
    try:
        print(f"Playing sound from {file_path}")
        pygame.mixer.music.load(file_path)  # Load the MP3 file
        pygame.mixer.music.play()  # Play the sound
        while pygame.mixer.music.get_busy():  # Wait until playback is complete
            pygame.time.Clock().tick(10)
        # Signal that the speech is done
        speech_done_event.set()  # Notify that speech has finished
    except Exception as e:
        print(f"Error playing sound: {e}")

def speak(text):
    """Generate or fetch an MP3 file and add it to the playback queue."""
    global cache
    text = text.replace(",", "phẩy")
    with cache_lock:  # Ensure no other thread modifies the cache while reading or writing
        if text in cache:
            file_path = cache[text]
        else:
            file_path = get_next_file_name()
            try:
                # Generate the speech file if not cached
                tts = gTTS(text, lang='vi', slow=False)
                tts.save(file_path)
                cache[text] = file_path
            except Exception as e:
                print(f"Error generating speech for '{text}': {e}")
                return

    # Ensure the file exists before attempting to queue it
    if not os.path.exists(file_path):
        print(f"File {file_path} was not created!")
        return

    # Reset the event before starting speech
    speech_done_event.clear()

    # Play the sound file in the background
    threading.Thread(target=play_sound, args=(file_path,), daemon=True).start()

    # Wait until the speech is finished
    speech_done_event.wait()  # This blocks until the speech is done

def stop_speech():
    """Stop any ongoing speech playback."""
    try:
        pygame.mixer.music.stop()  # Stop the current sound immediately
        print("Speech playback stopped.")
    except Exception as e:
        print(f"Error stopping speech: {e}")

# Ensure counter is saved when the program exits
import atexit
atexit.register(save_counter)

# Gracefully stop the queue thread when the program exits
def stop_queue():
    sound_queue.put(None)  # Send stop signal to the thread
atexit.register(stop_queue)
