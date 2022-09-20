from pickletools import unicodestringnl
from timeit import repeat
import requests
import json
import os.path
from numpy import median
BASE_URL = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api"



def make_get_request(url):
    """
      Makes a GET request to the API.

      Parameter url: a string constructed from the BASE_URL and API endpoint.  
    """
    try:
        print('making get request to {}'.format(url))
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    return json.loads(response.text)


def get_temperature(candidate_number, city, day, hour):
    """
      Returns the temperature of a given city at a specific day and hour.

      Parameter candidate_number: the candidate number to access the API.
      Precondition: candidate_number is an int

      Parameter city: the name of a city.
      Precondition: city is an string

      Parameter day: the day of a week.
      Precondition: day is an string

      Parameter hour: the hour of the day. 
      Precondition: hour is an int, 0 <= hour < 24

    """
    data = make_get_request(BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/')
    temperature = int(data[day][hour]['temperature'])
    return temperature

def is_pressure_below_threshold(candidate_number, city, day, pressure_threshold):
    """
      Returns True if the pressure is below the specified pressure threshold for a given city and day at anytime.

      Parameter candidate_number: the candidate number to access the API.
      Precondition: candidate_number is an int
      
      Parameter city: the name of a city.
      Precondition: city is an string

      Parameter day: the day of a week.
      Precondition: day is an string

      Parameter pressure_threshold: the pressure to test the condition against.
      Precondition: pressure_threshold is an int
    """
    data = make_get_request(BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/')
    data_for_day = data[day]
    for hour in data_for_day:
        if hour['pressure'] < pressure_threshold:
            return True
    return False

def get_median_temperature(candidate_number, city):
    """
      Returns the median temperature for a specified city over the week.

      Parameter candidate_number: the candidate number to access the API.
      Precondition: candidate_number is an int
      
      Parameter city: the name of a city.
      Precondition: city is an string
    """
    data = make_get_request(BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/')
    temperatures = []
    for day in data:
        for hour in data[day]:
            temperatures.append(hour['temperature'])
    return int(median(temperatures))


def get_highest_windspeed_city(candidate_number):
    """
      Returns the city the with the highest record wind speed over the week.

      If there is multiple cities the one earliest in the alphabet is returned.

      Parameter candidate_number: the candidate number to access the API.
      Precondition: candidate_number is an int
    """
    city_data = make_get_request(BASE_URL + '/cities')
    cities = city_data['cities']
    city_max_windspeed = {}
    for city in cities:
        windspeeds = []
        data = make_get_request(BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/')
        for day in data:
            for hour in data[day]:
                windspeeds.append(hour['wind_speed'])
        city_max_windspeed[city] = max(windspeeds)
    speeds = city_max_windspeed.values()
    topspeed = max(speeds)
    return sorted([k for k,v in city_max_windspeed.items() if v == topspeed])[0]


def will_snow(candidate_number):
    """
      Returns True if it is likely to snow in any of the cities for the week.

      It is likely to snow if there is precipitation when the temperature is below 2 degrees.

      Parameter candidate_number: the candidate number to access the API.
      Precondition: candidate_number is an int
    """
    temp_threshold  = 2
    precipitation_threshold = 0
    city_data = make_get_request(BASE_URL + '/cities')
    cities = city_data['cities']
    for city in cities:
        data = make_get_request(BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/')
        for day in data:
            for hour in data[day]:
                if hour['precipitation'] > precipitation_threshold and hour['temperature'] < temp_threshold:
                    return True
    return False

def save_file(answers):
    """
      Saves a json formatted textfile of the answered questions at a user specified location.

      Parameter answers: pairs of questions and their answers.
      Precondition: answers is a dictionary where each key and value pairs corresponds to a question and answer.
    """
    print("Saving...")
    name_of_file = input("What is the name of the file?: ")
    save_path = input("where would you like this file to be saved? e.g. 'C:/example/': ")
    complete_name = os.path.join(save_path, name_of_file+".txt")
    json_object = json.dumps(answers, indent = 4) 
    with open(complete_name, "w") as outfile:
        outfile.write(json_object)
    print("Saved at "+complete_name)

    
if __name__ == "__main__":
    while True:
        try:
            candidate_number = int(input("Input the candidate number: "))
            break
        except ValueError:
            print("Invalid candidate number, please try again")
    answers = {}
    answers["What will the temperature be in Bath at 10am on Wednesday morning?"] = get_temperature(candidate_number, 'bath', 'wednesday', 10)
    answers["Does the pressure fall below 1000 millibars in Edinburgh at any time on Friday?"] = is_pressure_below_threshold(candidate_number, 'edinburgh', 'friday', 1000)
    answers["What is the median temperature during the week for Cardiff?"] = get_median_temperature(candidate_number, 'cardiff')
    answers["In which city is the highest wind speed recorded this week?"] = get_highest_windspeed_city(candidate_number)
    answers["Will it snow in any of the cities this week?"] = will_snow(candidate_number)
    save_file(answers)

