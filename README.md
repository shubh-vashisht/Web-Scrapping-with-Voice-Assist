

#CoronaVirus Web scrapping with Python and Voice Assistance

In this project, I have scrapped the website https://www.worldometers.info/coronavirus/ to get
the details of all the coronavirus cases in all countries.
The code scrapes the data using parsehub, the accesses that data through the api, and then
processes that data to the user using Voice Assistance.

###Modules Used:
* requests
* re
* json
* threading
* time
* date
* pyttsx3

###Voice Assistance is implemented using modules such as :
1. pyttsx3
2. speech_recognition

The code then listens to the user and converts that into text, simultaneously using that text
to get the requested data from the api data stored.

##@This code repository was started on: 21st May,2021

#Guide to Corona Virus Net Scrapper:
The whole program is voice assisted, and you only have to type when you want to continue.
Whenever the program displays "listening...." you can request data by speaking into your microphone.
##The commands can be of the certain types:
* say "Total Cases": give the total cases in the entire world; 
   or say "How many total cases are there?" : this also returns the total number of cases
   c. say "Give me total cases": returns total number of cases in the world
* say "Total Recovered cases": returns total number of recovered cases
    say "Give me recovered cases": same result as above
*  say "total deaths" or "how many total deaths happened?": returns the total deaths
*  say "cases in {country_name}" or "how many cases in {country_name}" : returns total cases in named country
eg. if I say "cases in India" : this will return the total cases in India
*  say "active cases in {country_name}" or "active cases {country_name}": this will return current active cases in that country
*  say "deaths in {country_name}" or "deaths {country_name}": this will return total deaths in given country
*  say "update" : this will update the data and give you new numbers. (! only use this once a day)
*  say "exit" or "end": this will end the program