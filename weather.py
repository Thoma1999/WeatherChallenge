import requests
import json
import os.path
from numpy import median
URI = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api"


def make_get_request(url):
    print('making get request to {}'.format(url))
    response = requests.get(url)
    return json.loads(response.text)


def get_temperature(candidate_number, city, day, hour):
    #Fetches the data for bath from the API
    data = make_get_request(URI + '/weather/'+str(candidate_number)+'/'+city+'/')
    #Fetches and returns the specific temperature at 10 on a wednesday from the bath data
    temperature = int(data[day][hour]['temperature'])
    return temperature

def is_pressure_below_x(candidate_number, city, day, pressure):
    data = make_get_request(URI + '/weather/'+str(candidate_number)+'/'+city+'/')
    day_data = data[day]
    for hour in day_data:
        if hour['pressure'] < pressure:
            return True
    return False

def get_median_temperature(candidate_number, city):
    data = make_get_request(URI + '/weather/'+str(candidate_number)+'/'+city+'/')
    temperatures = []
    for day in data:
        for hour in data[day]:
            temperatures.append(hour['temperature'])
    return int(median(temperatures))


def get_highest_windspeed_city(candidate_number):
    city_data = make_get_request(URI + '/cities')
    cities = city_data['cities']
    city_max_windspeed = {}
    for city in cities:
        windspeeds = []
        data = make_get_request(URI + '/weather/'+str(candidate_number)+'/'+city+'/')
        for day in data:
            for hour in data[day]:
                windspeeds.append(hour['wind_speed'])
        city_max_windspeed[city] = max(windspeeds)
    speeds = city_max_windspeed.values()
    topspeed = max(speeds)
    return sorted([k for k,v in city_max_windspeed.items() if v == topspeed])[0]


def will_snow(candidate_number):
    city_data = make_get_request(URI + '/cities')
    cities = city_data['cities']
    for city in cities:
        data = make_get_request(URI + '/weather/'+str(candidate_number)+'/'+city+'/')
        for day in data:
            for hour in data[day]:
                if hour['precipitation'] > 0 and hour['temperature'] < 2:
                    #print(city+','+str(hour['precipitation'])+','+str(hour['temperature']))
                    return True
    return False

    
if __name__ == "__main__":
    candidate_number = int(input("Input the candidate number: "))
    name_of_file = input("What is the name of the file?: ")
    save_path = input("where would you like this file to be saved? e.g. 'C:/example/': ")
    completeName = os.path.join(save_path, name_of_file+".txt")   
    answers = {}
    answers["What will the temperature be in Bath at 10am on Wednesday morning?"] = get_temperature(candidate_number, 'bath', 'wednesday', 10)
    answers["Does the pressure fall below 1000 millibars in Edinburgh at any time on Friday?"] = is_pressure_below_x(candidate_number, 'edinburgh', 'friday', 1000)
    answers["What is the median temperature during the week for Cardiff?"] = get_median_temperature(candidate_number, 'cardiff')
    answers["In which city is the highest wind speed recorded this week?"] = get_highest_windspeed_city(candidate_number)
    answers["Will it snow in any of the cities this week?"] = will_snow(candidate_number)
    json_object = json.dumps(answers, indent = 4) 
    with open(completeName, "w") as outfile:
        outfile.write(json_object)

