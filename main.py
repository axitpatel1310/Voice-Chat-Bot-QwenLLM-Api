import requests
import json
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

tts_engine.setProperty('rate', 150)
tts_engine.setProperty('pitch', 50) 

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def get_voice_input():
    with sr.Microphone() as source:
        print("Listening... (say 'exit' or 'quit' to stop)")
        recognizer.adjust_for_ambient_noise(source)  
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            user_input = recognizer.recognize_google(audio)  
            print(f"You said: {user_input}")
            return user_input
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None

while True:
    user_input = get_voice_input()
    if not user_input:
        continue 
    if user_input.lower() in ["exit", "quit"]:
        speak_text("Exiting...")
        print("Exiting...")
        break
    user_question = {
        "type": "text",
        "text": user_input
    }
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer <APIKEY>",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "qwen/qwen2.5-vl-3b-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": [user_question]
                }
            ],
        })
    )

    # Process API response
    if response.status_code == 200:
        response_data = response.json()
        try:
            assistant_reply = response_data['choices'][0]['message']['content']
            print("Assistant's response:", assistant_reply)
            speak_text(assistant_reply)
        except KeyError as e:
            error_msg = f"Error: Could not find expected data in response: {e}"
            print(error_msg)
            speak_text(error_msg)
    else:
        error_msg = f"Request failed with status code {response.status_code}: {response.text}"
        print(error_msg)
        speak_text(error_msg)