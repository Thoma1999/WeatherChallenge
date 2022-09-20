import weather
import requests
BASE_URL = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api"
candidate_number = 89

def test_get_weather_for_city_check_status_code_equals_200():
    city = 'bath'
    url = BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/'
    response = requests.get(url)
    assert response.status_code == 200

def test_get_weather_for_city_check_status_code_equals_404():
    city = 'exeter'
    url = BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/'
    response = requests.get(url)
    assert response.status_code == 404

def test_get_temperature_for_city():
    city = 'bristol'
    day = 'friday'
    hour = 0
    url = BASE_URL + '/weather/'+str(candidate_number)+'/'+city.lower()+'/'
    data = weather.make_get_request(url)
    temperature = int(data[day][hour]['temperature'])
    assert temperature == 5

def test_get_cities():
    city_list = ['bristol', 'bath', 'southampton', 'manchester', 'portsmouth', 'liverpool', 'london', 'leeds', 'cardiff', 'swansea', 'edinburgh', 'glasgow', 'belfast']
    url = BASE_URL + '/cities'
    city_data = weather.make_get_request(url)
    assert city_data['cities'] ==  city_list

