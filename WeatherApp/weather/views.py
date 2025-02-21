from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import os
import environ

# Load environment variables
env = environ.Env()
environ.Env.read_env()


def home(request):
   
    if 'city' in request.POST:
         city = request.POST['city']
    else:
         city = 'patiala'     
    
    API_KEY_1 =  env("API_KEY_1")
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_1}'

    PARAMS = {'units':'metric'}

    API_KEY_2 = env("API_KEY_2")
    SEARCH_ENGINE_ID = env("SEARCH_ENGINE_ID")
     
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY_2}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    search_items = data.get("items", []) 

    if len(search_items) > 1:
        image_url = search_items[1]['link']
    elif len(search_items) > 0:
        image_url = search_items[0]['link']  #
    else:
        image_url = None  # No images found

    if image_url is None:
        messages.warning(request, "No image found for the selected city.")
    

    try:
          
          data = requests.get(url,params=PARAMS).json()
          description = data['weather'][0]['description']
          icon = data['weather'][0]['icon']
          temp = data['main']['temp']
          day = datetime.date.today()

          return render(request,'weather/index.html' , {'description':description , 'icon':icon ,'temp':temp , 'day':day , 'city':city , 'exception_occurred':False ,'image_url':image_url})
    
    except KeyError:
          exception_occurred = True
          messages.error(request,'Entered data is not available to API')   
          day = datetime.date.today()

          return render(request,'weather/index.html' ,{'description':'clear sky', 'icon':'01d'  ,'temp':25 , 'day':day , 'city':'patiala' , 'exception_occurred':exception_occurred } )
               
    
    