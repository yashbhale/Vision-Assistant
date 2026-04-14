import os
from gtts import gTTS
import subprocess

# Text to convert to speech
text = "This is an example message for gTTS and terminal playback."

# Generate the audio file (replace 'output.mp3' with desired filename)
language = 'en'  # Adjust for your preferred language
tts = gTTS(text=text, lang=language)
tts.save("output.mp3")

# Platform-specific command for audio playback with error handling
if os.name == 'nt':  # Windows
    try:
        # Use raw string for path to avoid encoding issues
        command = [r"C:\Users\ll010\Downloads\mpg123-1.32.6-static-x86-64\mpg123-1.32.6-static-x86-64\mpg123.exe", "output.mp3"]
        subprocess.run(command)
    except FileNotFoundError:
        print("Error: mpg123.exe not found. Please install mpg123 and ensure it's in your system path or adjust the path in the script.")
    except Exception as e:  # Catch other potential errors
        print(f"An error occurred during playback: {e}")

else:
    print(f"Unsupported operating system: {os.name}")

# Optional: Delete the generated audio file after playback (uncomment if desired)
# os.remove("output.mp3")
