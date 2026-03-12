import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
print(f"Found {len(voices)} voices:")
for i, voice in enumerate(voices):
    print(f"{i}: {voice.id} - {voice.name}")

engine.setProperty('voice', voices[0].id)
engine.say("This is a voice test from pyttsx3 on Windows.")
engine.runAndWait()
