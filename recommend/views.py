# recommend/views.py

import requests, json, random
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .utils import read_class_indices_clothesdata, get_user_clothes
from django.http import JsonResponse, HttpResponseBadRequest
from .models import RecommendedClothes
    
def weatherapi(latitude, longitude):
    if latitude and longitude:
        api_key = 'cbd3023a75f5f25f7c80897189cbe42a'  # OpenWeatherMap에서 발급받은 API 키
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}"
        response = requests.get(url)
        weather = response.json()
        return weather  # JsonResponse 객체를 반환합니다.
    

def get_current_month():
    current_month = datetime.now().month
    if 3 <=current_month <= 5:
        return 'spring'
    elif 6 <= current_month <= 9:
        return 'summer'
    elif 10 <= current_month <= 11:
        return 'fall'
    else:
        return 'winter'
    
    
def user_clothes_categorized():
    user_clothes = get_user_clothes()
    bottom_clothes = []
    outer_clothes = []
    top_clothes = []

    for file_name in user_clothes:
        # 파일 이름에서 옷의 종류를 추출
        if 'bottom' in file_name:
            bottom_clothes.append(file_name)
        elif any(item in file_name for item in ['t-shirts', 'shirt','jumper']):
            top_clothes.append(file_name)
        elif any(item in file_name for item in ['jacket', 'coat', 'cardigan']):
            outer_clothes.append(file_name)
    # print(bottom_clothes, outer_clothes, top_clothes)
    return bottom_clothes, outer_clothes, top_clothes

##########################################################################################################################################

### 추천 알고리즘 ###
## situation: 옷 입는 상황 - dandy, formal, casual, street,sporty
## current_temp: 현재 온도 - float형식
## current_month: 현재 월 - spring, summer, fall, winter
@csrf_exempt
def recommend_algorithm(request):
    # clothesdata = read_class_indices_clothesdata()  # 옷_색상 데이터를 가져오는 함수
    bottom_clothes, outer_clothes, top_clothes = user_clothes_categorized()  # 사용자가 저장한 옷을 종류별로 분류하는 함수
    
    season = get_current_month()
    # print(season)
    
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    weather_info = weatherapi(latitude, longitude)
    current_temp = 15 
    
    if weather_info and 'main' in weather_info and 'temp' in weather_info['main']:
        current_temp = weather_info['main']['temp']

    situation = None
    if request.method == 'POST':
        # POST 요청에서 situation 값을 가져옴
        try:
            data = json.loads(request.body)
            situation = data.get('situation')
        except (ValueError, KeyError):
            situation = None
    else:
        # GET 요청에서 situation 값을 가져옴
        situation = request.GET.get('situation')

        
    clothes_weights = clothes_weight(situation, season, current_temp)
    color_weights = color_weight(season, current_temp)
    brightness_weights = brightness_weight(season)
    #print("확인")
    #print(clothes_weight('dandy', 'summer', 100))
    # print()
    # print("Clothes Weights:", clothes_weights)
    # print("Color Weights:", color_weights)
    # print("Brightness Weights:", brightness_weights)
    # print()
    
    # 옷과 색상의 가중치를 곱하고 가장 높은 가중치를 가진 옷을 선택
    max_weight = 0

    selected_clothes_set = set()
    selected_clothes = {'bottom': None, 'top': None, 'outer': None}

  
    for clothes_category in [bottom_clothes, top_clothes, outer_clothes]:
        max_weight = 0  # 각 카테고리별로 별도의 max_weight 사용
        for clothes in clothes_category:
            clothes_type, color, brightness = classification(clothes)
            # 기존 가중치에 랜덤한 가중치를 곱함
            random_weight = random.uniform(1.000, 1.500)
            # print("random_weight: ", random_weight)
            weight = random_weight * clothes_weights.get(clothes_type, 1) * color_weights.get(color, 1) * brightness_weights.get(brightness, 1)
            if weight > max_weight and clothes not in selected_clothes_set and weight > 0.4:
                selected_clothes[clothes_type] = clothes
                selected_clothes_set.add(clothes)
                selected_color = selected_clothes[clothes_type].split('_')[1]
                for key in color_weights:
                    if key in color_combinations_weight(selected_color):
                        color_weights[key] *= color_combinations_weight(selected_color)[key]
                        max_weight = weight

    # print("최종 선택된 옷: ", selected_clothes, "가중치: ", max_weight)         

    
    return render(request, 'recommend/recommend.html', {
        'weather': weather_info,
        'selected_outer': selected_clothes['outer'],
        'selected_top': selected_clothes['top'],
        'selected_bottom': selected_clothes['bottom'],
    })

##########################################################################################################################################

def classification(filename):
    parts = filename.split('_')
    clothes = parts[0]
    color = parts[1]
    brightness = parts[2]  # 'l', 's', 'd' 중 하나를 가져옴
    if 'bottom' in clothes:
        clothes = 'bottom'
    elif any(item in clothes for item in ['t-shirts', 'shirt', 'jumper']):
        clothes = 'top'
    elif any(item in clothes for item in ['jacket', 'coat', 'cardigan']):
        clothes = 'outer'
    return clothes, color, brightness

def clothes_weight(situation, season, current_temp):
    clothes_weights = {"bottom": 1, "t-shirt": 1, "shirt": 1, "jumper": 1, "jacket": 1, "coat": 1, "cardigan": 1, "": 1}
    situation_weights = situation_clothes_weight(situation)
    season_weights = season_clothes_weight(season)
    temperature_weights = temperature_clothes_weight(current_temp)

    if situation_weights is None:
        situation_weights = {}
    
    for clothes in clothes_weights:
        clothes_weights[clothes] *= season_weights.get(clothes, 1)
        clothes_weights[clothes] *= temperature_weights.get(clothes, 1)
        clothes_weights[clothes] *= situation_weights.get(clothes, 1)
    
    return clothes_weights


def color_weight(season , current_temp):
    color_weights = {"black": 1, "blue": 1, "brown": 1, "gray": 1, "green": 1, "navy": 1, 
                  "orange": 1, "purple": 1, "red": 1, "white": 1, "yellow": 1}
    #color_combinations = color_combinations_weight()
    season_weights = season_color_weight(season)
    temperature_weights = temperature_color_weight(current_temp)
    # print(season_weights)
    # print()
    # print(temperature_weights)

    for color in color_weights:
        #color_weights[color] *= color_combinations.get(color, 1)
        color_weights[color] *= season_weights.get(color, 1)
        color_weights[color] *= temperature_weights.get(color, 1)
    return color_weights


### 색상 가중치 ###
def color_combinations_weight(selected_color):
    color_combinations = {
    'red':    {'red': 0.4, 'orange': 0.4, 'yellow': 0.5, 'green': 0.4, 'blue': 0.6, 'purple': 0.6, 'navy': 0.6, 'gray': 0.5, 'brown': 0.7, 'black': 0.8, 'white': 0.9},
    'orange': {'red': 0.4, 'orange': 0.4, 'yellow': 0.8, 'green': 0.5, 'blue': 0.4, 'purple': 0.4, 'navy': 0.8, 'gray': 0.5, 'brown': 0.9, 'black': 0.6, 'white': 0.8},
    'yellow': {'red': 0.4, 'orange': 0.8, 'yellow': 0.7, 'green': 0.6, 'blue': 0.4, 'purple': 0.4, 'navy': 0.8, 'gray': 0.5, 'brown': 0.6, 'black': 0.5, 'white': 0.9},
    'green':  {'red': 0.4, 'orange': 0.5, 'yellow': 0.6, 'green': 0.7, 'blue': 0.8, 'purple': 0.5, 'navy': 0.7, 'gray': 0.6, 'brown': 0.4, 'black': 0.5, 'white': 0.7},
    'blue':   {'red': 0.4, 'orange': 0.4, 'yellow': 0.4, 'green': 0.8, 'blue': 0.7, 'purple': 0.6, 'navy': 0.6, 'gray': 0.5, 'brown': 0.4, 'black': 0.5, 'white': 0.8},
    'purple': {'red': 0.4, 'orange': 0.4, 'yellow': 0.4, 'green': 0.5, 'blue': 0.6, 'purple': 0.7, 'navy': 0.4, 'gray': 0.5, 'brown': 0.5, 'black': 0.6, 'white': 0.8},
    'navy' :  {'red': 0.6, 'orange': 0.7, 'yellow': 0.4, 'green': 0.8, 'blue': 0.7, 'purple': 0.6, 'navy': 0.5, 'gray': 0.5, 'brown': 0.6, 'black': 0.5, 'white': 0.8},
    'gray':   {'red': 0.6, 'orange': 0.5, 'yellow': 0.5, 'green': 0.6, 'blue': 0.5, 'purple': 0.5, 'navy': 0.4, 'gray': 0.7, 'brown': 0.4, 'black': 0.6, 'white': 0.8},
    'brown':  {'red': 0.6, 'orange': 0.9, 'yellow': 0.6, 'green': 0.4, 'blue': 0.4, 'purple': 0.5, 'navy': 0.8, 'gray': 0.4, 'brown': 0.8, 'black': 0.7, 'white': 0.6},
    'black':  {'red': 0.8, 'orange': 0.7, 'yellow': 0.7, 'green': 0.7, 'blue': 0.7, 'purple': 0.6, 'navy': 0.8, 'gray': 0.6, 'brown': 0.8, 'black': 0.8, 'white': 0.7},
    'white':  {'red': 0.6, 'orange': 0.8, 'yellow': 0.9, 'green': 0.7, 'blue': 0.8, 'purple': 0.8, 'navy': 0.7, 'gray': 0.8, 'brown': 0.6, 'black': 0.7, 'white': 0.9}
    }
    return color_combinations.get(selected_color, {})
    
def season_color_weight(season):
    if season == 'spring':
        return {'yellow': 1.2, 'green': 1.2, 'blue': 1.2, 'purple': 1.2, 'navy': 1.2, 'orange' : 1.2 }
    elif season == 'summer':
        return {'yellow': 1.2, 'green': 1.2, 'blue': 1.2, 'purple': 1.2, 'white': 1.2, 'orange' : 1.2 }
    elif season == 'fall':
        return {'red' : 1.2, 'yellow': 1.2, 'brown': 1.2, 'navy' : 1.2, 'gray': 1.2, 'black': 1.2}
    elif season == 'winter':
        return {'red' : 1.2, 'green': 1.2, 'navy': 1.2, 'gray': 1.2, 'black': 1.2, 'white': 1.2}

    
def temperature_color_weight(current_temp):
    if current_temp <= 0:
        return {'black': 1.2, 'gray': 1.2, 'navy': 1.2, 'blue': 1.2, 'purple': 1.2}
    elif 0 < current_temp <= 10:
        return {'black': 1.2, 'gray': 1.2, 'navy': 1.2, 'green': 1.2, 'brown': 1.2}
    elif 10 < current_temp <= 20:
        return {'green': 1.2, 'blue': 1.2, 'purple': 1.2, 'red': 1.2, 'orange': 1.2}
    else:
        return {'yellow': 1.2, 'orange': 1.2, 'red': 1.2, 'white': 1.2, 'green': 1.2}


def brightness_weight(season):
    if season == 'spring':
        brightness_weights = {"s": 1, "l": 1.2, "d": 0.8}
    elif season == 'summer':
        brightness_weights = {"s": 1, "l": 1.3, "d": 0.7}
    elif season == 'fall':
        brightness_weights = {"s": 1, "l": 0.9, "d": 1.2}
    elif season == 'winter':
        brightness_weights = {"s": 1, "l": 0.8, "d": 1.3}
    return brightness_weights


### 옷 종류 가중치 ###
def season_clothes_weight(season):
    if season == 'spring':
        return {'cardigan': 1.2, 'coat': 1.2, 'jacket': 1.2, 'shirt': 1.2, 'jumper': 1.2, '': 1.2}
    elif season == 'summer':
        return {'shirt': 1.1, 't-shirt': 1.2, "" : 1.8}
    elif season == 'fall':
        return {'cardigan': 1.2, 'coat': 1.2, 'jacket': 1.2, 'shirt': 1.2, 'jumper': 1.2}
    elif season == 'winter':
        return {'jumper':1.2, 'coat': 1.2, 'jacket': 1.2}

    
def temperature_clothes_weight(current_temp):
    if current_temp <= 0:
        return {'coat': 1.2, 'jacket': 1.2, 'jumper': 1.2, "": 0.0}
    elif 0 < current_temp <= 10:
        return {'coat': 1.2, 'jacket': 1.2, 'cardigan': 1.2, 'jumper': 1.2}
    elif 10 < current_temp <= 20:
        return {'shirt': 1.2, 'cardigan': 1.2}
    else:
        return {'t-shirt': 1.2, 'shirt': 1.2, 'cardigan': 0.2, 'jacket': 0, 'coat': 0, 'jumper': 0, '': 1.2} 


def situation_clothes_weight(situation):
    if situation == 'dandy':
        return {'coat': 1.2, 'jacket': 1.2, 'shirt': 1.2, 'cardigan': 1.2}
    elif situation == 'formal':
        return {'coat': 1.2, 'jacket': 1.2, 'shirt': 1.2, 'cardigan': 1.2}
    elif situation == 'casual':
        return {'jumper': 1.2, 'cardigan': 1.2, 't-shirt': 1.2, 'shirt': 1.2}
    elif situation == 'street':
        return {'jumper': 1.2, 'jacket': 1.2, 't-shirt': 1.2}
    elif situation == 'sporty':
        return {'jumper': 1.2, 't-shirt': 1.2,}
    
    
    ###############################################################

def save_recommendation(request):
    if request.method == 'POST':
        date = datetime.now().date()
        top = request.POST.get('top')
        bottom = request.POST.get('bottom')
        outer = request.POST.get('outer')
    
        # 기존 추천 옷이 있으면 삭제
        RecommendedClothes.objects.all().delete()
    
        # 새로운 추천 옷 저장
        new_recommendation = RecommendedClothes(date=date,top=top, bottom=bottom, outer=outer)
        new_recommendation.save()
        
        return redirect('recommend_algorithm') # 추천 알고리즘 페이지로 리다이렉트
    
    return redirect('recommend_algorithm') # 추천 알고리즘 페이지로 리다이렉트

