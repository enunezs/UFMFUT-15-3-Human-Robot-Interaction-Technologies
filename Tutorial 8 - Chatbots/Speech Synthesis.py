from gtts import gTTS
import os
import pygame

def text_to_speech(text, language='en'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio file
    audio_file = "output.mp3"
    tts.save(audio_file)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait until the audio is finished playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Check every 100 ms

    # Optionally, remove the audio file after playing
    os.remove(audio_file)

if __name__ == "__main__":
    sample_text = "Hello! This is a sample text to demonstrate speech synthesis using Python."
    text_to_speech(sample_text)