import requests
import json
import config
import speech_recognition as sr
import re
import pyttsx3


def listen():
    base_url = 'https://api.openweathermap.org/data/2.5/weather?'
    engine = pyttsx3.init()

    # Microphone audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        # command = "what's the weather in quebec"  # --FOR TESTING PURPOSES--

        if re.match("what's the weather in [a-zA-Z]+(?:[-][a-zA-Z]+)*$", command):
            print(command)
            city = command.split(" ")[4]
            full_url = base_url + 'q=' + city + '&appid=' + config.api_key

            response = json.loads(requests.get(full_url).text)

            # print("It is " + str(float(response['main']['temp']) - 273) + "°C with a " + response['weather'][0][
            #     'description'] + ".")

            engine.say("It is " + str(float(response['main']['temp']) - 273) + "°C with " + response['weather'][0][
                'description'] + ".")
            engine.runAndWait()
        else:
            engine.say("Wrong command")
            engine.runAndWait()

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))


if __name__ == '__main__':
    listen()
