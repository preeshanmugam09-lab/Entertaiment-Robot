import speech_recognition as sr
import google.generativeai as genai
import serial
import time
import os

# =====================
# GEMINI CONFIG
# =====================
os.environ["GOOGLE_API_KEY"] = "AIzaSyDljjdaAWvlBHoXjafJBybTSAfXjGG603A"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-flash-latest")

# =====================
# SERIAL (ESP32)
# =====================
esp = serial.Serial("COM12", 115200)
time.sleep(2)

# =====================
# SPEECH RECOGNITION
# =====================
r = sr.Recognizer()
mic = sr.Microphone()

def listen():
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, 0.5)
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""

def ask_gemini(text):
    response = model.generate_content(text)
    return response.text.strip()

print("🎤 Gemini Robot Ready")

while True:
    text = listen()
    if not text:
        continue

    print("You:", text)

    if text.lower() in ["exit", "stop"]:
        esp.write(b"Goodbye\n")
        break

    reply = ask_gemini(text)
    print("Gemini:", reply)

    esp.write((reply + "\n").encode())