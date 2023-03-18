from django.shortcuts import render, redirect
import requests
import json
import datetime
from suntime import Sun

# THANKS TO OPENWEATHERMAP API
#pls install suntime
# Create your views here.
url = ""
def home(request):
    time = datetime.datetime.now()
    time_now = time.time()
    hour = int(time_now.strftime("%H"))
    global url
    if hour >= 5  and hour < 12:
        url = "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
    if hour >= 12 and hour < 16:
        url = "https://images.unsplash.com/photo-1512592585971-bff48f1c9815?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80"
    if hour >= 16 and hour <= 19:
        url = "https://images.unsplash.com/photo-1620473564823-8baf403595a9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80"
    if hour > 19 and hour <= 23 or hour >= 0 and hour < 5:
        url = "https://i0.wp.com/eos.org/wp-content/uploads/2023/02/skyglow-rural-suburbs-cities-globe-at-night.png?fit=1200%2C675&ssl=1"
    return render(request, 'weatherapp/index.html',{'hour': hour, 'url': url})

def weather(request):
    report = request.GET['place']
    api_key = "Your API KEY"
    parameters = {
        'q': report,
        'appid': api_key,
    }
    api_location_key = "http://api.openweathermap.org/geo/1.0/direct?"
    
    try:
        data = requests.get(url=api_location_key, params=parameters)
        data.raise_for_status()
        data_detail = data.json()  
    
        lat = data_detail[0]['lat']
        long = data_detail[0]['lon']
        
        sun = Sun(lat, long)

        time = datetime.datetime.now()
        date_today = time.date()
        time_zone = date_today
        sun_rise = sun.get_local_sunrise_time(time_zone)
        sun_dusk = sun.get_local_sunset_time(time_zone)
        
        api_end_key = "https://api.openweathermap.org/data/2.8/onecall"
        
        weather_params = {
            'lat': lat,
            'lon': long,
            'appid': api_key
        }
        weather_data = requests.get(url=api_end_key, params=weather_params)
        weather_data.raise_for_status()
        weather_detail = weather_data.json()
        
        cur_temp = int((weather_detail['current']['temp']) - 273.15)
        feels_like = int((weather_detail['current']['feels_like']) - 273.15)
        cur_press = weather_detail['current']['pressure']
        cur_hum = weather_detail['current']['humidity']
        cur_uvi = weather_detail['current']['uvi']
        cur_vis = (weather_detail['current']['visibility']) // 1000
        cur_wind = weather_detail['current']['wind_speed']
        weather = weather_detail['current']['weather'][0]['description']
        weather_dtl = weather_detail['current']['weather'][0]['main']
        min_temp = int((weather_detail['daily'][1]['temp']['min']) - 273.15)
        max_temp = int((weather_detail['daily'][1]['temp']['max']) - 273.15) 
        tmr_wtr = weather_detail['daily'][1]['weather'][0]['description']
        sun_rise = sun_rise.strftime('%H:%M')
        sun_dusk = sun_dusk.strftime('%H:%M')
        
        return render(request, 'weatherapp/weather.html', {'reports': report,
                                                       'lat': lat, 
                                                       'long': long, 
                                                       'cur_temp': cur_temp, 
                                                       'feels_like': feels_like, 
                                                       'cur_press': cur_press,
                                                       'cur_hum': cur_hum,
                                                       'cur_uvi': cur_uvi,
                                                       'cur_vis': cur_vis,
                                                       'cur_wind': cur_wind,
                                                       'weather': weather,
                                                       "weather_dtl": weather_dtl,
                                                       'min_temp': min_temp,
                                                       'max_temp': max_temp,
                                                       'tmr_wtr': tmr_wtr,
                                                       'sun_rise': sun_rise,
                                                       'sun_dusk': sun_dusk
                                                       })
    
    except IndexError:
        return redirect('error') 
    

    
def error(request):
    time = datetime.datetime.now()
    time_now = time.time()
    hour = int(time_now.strftime("%H"))
    if hour >= 5  and hour < 12:
        url = "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
    if hour >= 12 and hour < 16:
        url = "https://images.unsplash.com/photo-1512592585971-bff48f1c9815?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80"
    if hour >= 16 and hour <= 19:
        url = "https://images.unsplash.com/photo-1620473564823-8baf403595a9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80"
    if hour > 19 and hour <= 23 or hour >= 0 and hour < 5:
        url = "https://i0.wp.com/eos.org/wp-content/uploads/2023/02/skyglow-rural-suburbs-cities-globe-at-night.png?fit=1200%2C675&ssl=1"
    return render(request, 'weatherapp/error.html', {'hour': hour, 'url': url})    

   
