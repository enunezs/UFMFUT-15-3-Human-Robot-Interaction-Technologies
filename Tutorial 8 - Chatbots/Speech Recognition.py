import speech_recognition as sr

def recognize_speech_from_mic():
    # Create a Recognizer instance
    recognizer = sr.Recognizer()

    # Set up the microphone
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        # Recognize speech using Google Web Speech API
        print("Recognizing...")
        # Set timeout to 5 seconds and phrase_time_limit to 10 seconds
        # You can adjust here!
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognize_speech_from_mic()