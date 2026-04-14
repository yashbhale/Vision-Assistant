import speech_recognition as sr
from pydub import AudioSegment

def speech_to_mp3():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

        # Save audio as a WAV file
        with open("speech.wav", "wb") as wav_file:
            wav_file.write(audio_data.get_wav_data())

        try:
            # Recognize speech using Google Web Speech API
            print("Recognizing...")
            text = recognizer.recognize_google(audio_data)
            print(f"You said: {text}")

            # Write the recognized text to a file
            with open("recognized_text.txt", "w") as file:
                file.write(text)

            print("Text has been written to 'recognized_text.txt'")

            # Convert WAV file to MP3
            sound = AudioSegment.from_wav("speech.wav")
            sound.export("speech.mp3", format="mp3")
            print("MP3 file has been saved as 'speech.mp3'")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


if __name__ == "__main__":
    speech_to_mp3()
