import requests
import json
import pyttsx3  # text to audio
import speech_recognition as sr
import re
import threading
import time
from datetime import date
from datetime import datetime

api_key = "tV3nQTyNdwgG"
project_token = "tXhAMN_ZBbPh"
run_toker = "tT5p-PGTeFtb"

alreadyUpdated = False
dateUpdated = date(2021, 5, 20)
updating = False


class Data:
    def __init__(self, api, project_toker):
        self.api_key = api
        self.project_token = project_toker
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()
        self.data = self.get_data()

    def get_data(self):
        content = requests.get(f"https://parsehub.com/api/v2/projects/{project_token}/last_ready_run/data",
                               params={"api_key": api_key})
        data = json.loads(content.text)
        return data

    def get_total_cases(self):
        data = self.data['total']
        for i in data:
            if i['name'] == 'Coronavirus Cases:':
                return i['value']

    def get_total_deaths(self):
        data = self.data['total']
        for i in data:
            if i['name'] == 'Deaths:':
                return i['value']

    def get_recovered_cases(self):
        data = self.data['total']
        for i in data:
            if i['name'] == 'Recovered:':
                return i['value']
        return "0"

    def get_country_data(self, country_name):
        data = self.data['country']
        for i in data:
            if i['name'].lower() == country_name.lower():
                return i
        return "0"

    def get_countries(self):
        data = self.data['country']
        countries = []
        for i in data:
            countries.append(i['name'].lower())
        return countries

    def update(self):
        if dateUpdated == date.today():
            global alreadyUpdated
            global updating
            alreadyUpdated = True
            updating = False
            return

        request = requests.post(f"https://parsehub.com/api/v2/projects/{project_token}/run", params=self.params)

        def poll():
            global updating, dateUpdated, alreadyUpdated
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    updating = False
                    dateUpdated = date.today()
                    alreadyUpdated = True
                    print("\n Yay ! success data updated \n")
                    break
                updating = True
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception:", str(e))
    return said.lower()


def exiting():
    print("Shutting program down! Thanks for using...")
    speak("Shutting program down! Thanks for using...")
    exit()


def main():
    print("started Program")
    data = Data(api_key, project_token)
    country_list = (data.get_countries())

    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases [\w\s]"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("total cases"): data.get_total_cases,
        re.compile("[\w\s]+ worldwide cases [\w\s]"): data.get_total_cases,
        re.compile("worldwide cases"): data.get_total_cases,
        re.compile("[\w\s]+ worldwide cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total death [\w\s]"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths [\w\s]"): data.get_total_deaths,
        re.compile("total deaths [\w\s]"): data.get_total_deaths,
        re.compile("total deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ recovered cases [\w\s]"): data.get_recovered_cases,
        re.compile("[\w\s]+ recovered cases"): data.get_recovered_cases,
        re.compile("total recovered cases"): data.get_recovered_cases,
        re.compile("stop"): exiting,
        re.compile("exit"): exiting
    }

    Country_patterns = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ cases+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile("deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile("deaths"): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile("death [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile("[\w\s]+ deaths+"): lambda country: data.get_country_data(country)['total_deaths'],
        re.compile("[\w\s]+ active cases [\w\s]+"): lambda country: data.get_country_data(country)['active_cases'],
        re.compile("active cases+"): lambda country: data.get_country_data(country)['active_cases'],
        re.compile("active cases [\w\s]+"): lambda country: data.get_country_data(country)['active_cases'],
        re.compile("[\w\s]+active cases+"): lambda country: data.get_country_data(country)['active_cases'],
    }
    update_command = "update"
    i = "y"
    while i == "y":
        print("please start speaking when you see the that the program is listening")
        time.sleep(1)
        print("listening....")
        text = get_audio()
        result = None
        if text == update_command:
            global alreadyUpdated, updating
            data.update()
            if alreadyUpdated:
                result = f"The data is already updated today {dateUpdated}. \nYou can only update the data once a day.\nDo you want to continue?"
            else:
                result = "We are currently updating the data from the website, this can take a minute or two... \n Do not type in an input until you recieve the success notification"
            while updating:
                "Please wait, we are currently updating"
                time.sleep(10)
        for pattern, func in Country_patterns.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break
                result = "Named Country Does not exist or has 0 coronavirus cases"

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if result:
            print(result)
            speak(result)
        else:
            print("Apologies could not understand you.. :( ")

        i = input("Do you want to continue? (y/n) >>")
        if i == "n": break
        while i != "n" and i != "y":
            print("Please enter a valid input!")
            i = input("Do you want to continue? (y/n) >>")


def info():
    f = open("info.txt", "r")
    print(f.read())


def guide():
    f = open("guide.txt", "r")
    print(f.read())


def starter():
    print("Hello and welcome to corona virus web scrapper")
    speak("Hello and welcome to corona virus web scrapper")
    print("This is a project developed by Shubh Vashisht")
    speak("This is a project developed by Shubh Vashisht")
    print(
        "It was made using python and modules including: requests, pyttsx3, speech_recognition, json, re, threading and date ")
    speak(
        "It was made using python and modules including: requests, pyttsx3, speech_recognition, json, re, threading and date ")
    inp = ""
    while inp != "start" and inp != "exit":
        inp = input(
            """To start the program, type "start"\nTo get the guide,type "guide"\nTo get the info for the project, type "info"\nTo exit the program, type "exit" \n >>""")
        if inp == "start":
            main()
        elif inp == "exit":
            exit()
        elif inp == "info":
            info()
        elif inp == "guide":
            guide()
        else:
            print("Please enter a valid input")
            inp = input(
                """To start the program, type "start"\nTo get the guide,type "guide"\nTo get the info for the project, type "info"\nTo exit the program, type "exit"\n >>""")


starter()
