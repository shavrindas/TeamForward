from django.conf import settings
from django.shortcuts import render
from .models import UserPicture
from django.shortcuts import redirect
import random
import requests
from datetime import datetime
from .models import RecommendedClothes, UserData 
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
from django.contrib.auth.decorators import login_required

################################################################################

def recommend_clothes(request):
    user_email = request.COOKIES.get('user_email')  # 쿠키에서 사용자 이메일 읽어오기
    user_id = request.COOKIES.get('user_id')  # 이메일 아이디 대신 user_id를 사용하는 경우
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    situation = request.GET.get('situation', 'casual')  # 기본 상황을 'casual'로 설정
    
    user_pictures = UserPicture.objects.filter(user_id=user_id)
    image_paths = {picture.picture_name: settings.MEDIA_URL + str(picture.picture) for picture in user_pictures}

    # 날씨 정보 가져오기
    weather = weatherapi(latitude, longitude)
    temperature = weather['main']['temp'] if weather and 'main' in weather else 20  # 온도 정보 가져오기

    # 계절 정보 가져오기
    season = get_current_month()

    # 기본 이미지 경로 설정
    default_bottom_image_path = settings.MEDIA_URL + "user_pictures/pants.png"
    default_top_image_path = settings.MEDIA_URL + "user_pictures/shirt.png"
    default_outer_image_path = settings.MEDIA_URL + "user_pictures/jumper.png"

    # 선택된 이미지 경로
    selected_bottom_image_name, selected_bottom_image_path = select_image_by_type_color_brightness(image_paths, ['bottom'], temperature=temperature, situation=situation, is_base=True)
    base_color = selected_bottom_image_name.split('_')[1] if selected_bottom_image_name else None

    selected_top_image_name, selected_top_image_path = select_image_by_type_color_brightness(image_paths, ['t-shirts', 'shirt', 'jumper'], base_color=base_color, temperature=temperature, situation=situation)
    top_color = selected_top_image_name.split('_')[1] if selected_top_image_name else None

    selected_outer_image_name, selected_outer_image_path = select_image_by_type_color_brightness(image_paths, ['jacket', 'coat', 'cardigan'], base_color=base_color if top_color is None else top_color, temperature=temperature, situation=situation)

    # 선택된 이미지 경로가 없는 경우 기본 이미지 사용
    selected_bottom_image_path = selected_bottom_image_path if selected_bottom_image_path else default_bottom_image_path
    selected_top_image_path = selected_top_image_path if selected_top_image_path else default_top_image_path
    selected_outer_image_path = selected_outer_image_path if selected_outer_image_path else default_outer_image_path

    # 터미널에 사용자가 가진 이미지들 출력
    print("사용자가 가진 모든 이미지들:")
    for image_name, image_path in image_paths.items():
        print("이미지 이름:", image_name)
        print("이미지 경로:", image_path)

    print("선택된 이미지들:")
    print("하의 이미지 경로:", selected_bottom_image_path)
    print("상의 이미지 경로:", selected_top_image_path)
    print("외의 이미지 경로:", selected_outer_image_path)

    # 선택된 이미지들의 정보를 전달
    return render(request, 'recommend/recommendation.html', {
        'selected_bottom_image_path': selected_bottom_image_path,
        'selected_top_image_path': selected_top_image_path,
        'selected_outer_image_path': selected_outer_image_path,
        'user_email': user_email,  # 사용자 이메일을 전달
    })


################################################################################

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

def get_seasonal_weights(season):
    if season == 'spring':
        return {'cardigan': 1.2, 'coat': 1.2, 'jacket': 1.2, 'shirt': 1.2, 'jumper': 1.2}
    elif season == 'summer':
        return {'shirt': 1.1, 't-shirt': 1.2}
    elif season == 'fall':
        return {'cardigan': 1.2, 'coat': 1.2, 'jacket': 1.2, 'shirt': 1.2, 'jumper': 1.2}
    elif season == 'winter':
        return {'jumper': 1.2, 'coat': 1.2, 'jacket': 1.2}
    return {}

def get_brightness_weights(temperature):
    if temperature >= 20:  # 기온이 높거나 봄/여름인 경우
        return {'s': 1.5, 'l': 1.5, 'd': 0.5, '': 1}
    elif temperature < 10:  # 기온이 낮거나 가을/겨울인 경우
        return {'s': 0.5, 'l': 0.5, 'd': 1.5, '': 1}
    else:
        return {'s': 1, 'l': 1, 'd': 1, '': 1}


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
        return {'jumper': 1.2, 't-shirt': 1.2}
    return {}

def calculate_color_score(base_color, target_color):
    return color_combinations.get(base_color, {}).get(target_color, 0)

def select_image_by_type_color_brightness(image_paths, cloth_types, base_color=None, temperature=None, situation=None, is_base=False, confusion=0.05):
    """
    주어진 옷 타입 목록 중 하나에 해당하는 이미지를 무작위로 선택하거나
    특정 색상에 맞춰 가중치 부여하여 선택하는 함수
    """
    filtered_images = [(image_name, image_path) for image_name, image_path in image_paths.items() if any(image_name.startswith(cloth_type) for cloth_type in cloth_types)]
    
    if not filtered_images:
        return None, None

    if is_base or base_color is None:
        return random.choice(filtered_images)

    weighted_images = []
    brightness_weights = get_brightness_weights(temperature)
    situation_weights = situation_clothes_weight(situation)

    for image_name, image_path in filtered_images:
        image_color = image_name.split('_')[1]
        image_brightness = image_name.split('_')[2] if len(image_name.split('_')) > 2 else ''
        image_type = image_name.split('_')[0]
        color_score = calculate_color_score(base_color, image_color)
        brightness_score = brightness_weights.get(image_brightness, 1)
        situation_score = situation_weights.get(image_type, 1)
        score = color_score * brightness_score * situation_score
        weighted_images.extend([(image_name, image_path)] * int(score * 10))  # 가중치를 반영하여 확률 증가

    if random.random() < confusion:
        return random.choice(filtered_images)

    return random.choice(weighted_images) if weighted_images else random.choice(filtered_images)


def weatherapi(latitude, longitude):
    if latitude and longitude:
        api_key = 'cbd3023a75f5f25f7c80897189cbe42a'  # OpenWeatherMap에서 발급받은 API 키
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}"
        response = requests.get(url)
        weather = response.json()
        return weather  # JsonResponse 객체를 반환합니다.
    
def get_current_month():
    current_month = datetime.now().month
    if 3 <= current_month <= 5:
        return 'spring'
    elif 6 <= current_month <= 9:
        return 'summer'
    elif 10 <= current_month <= 11:
        return 'fall'
    else:
        return 'winter'
   
################################################################################
def save_recommendation(request):
    if request.method == 'POST':
        bottom = request.POST.get('selected_bottom_image_path')
        top = request.POST.get('selected_top_image_path')
        outer = request.POST.get('selected_outer_image_path')
        style = request.COOKIES.get('selected_style')  # 쿠키에서 스타일 정보 읽어오기

        # 쿠키에서 사용자 ID를 읽어옵니다.
        user_email = request.COOKIES.get('user_email')

        if user_email:
            # 추천 정보를 저장합니다.
            recommendation = RecommendedClothes.objects.create(
                user_email=user_email,
                bottom=bottom,
                top=top,
                outer=outer,
                date=datetime.now(),  # 현재 시각으로 저장
                style=style
            )

            # 저장 후에 recommend_clothes 페이지로 리디렉션합니다.
            return redirect('recommend_clothes')
        else:
            return HttpResponse('User ID not found in cookies')
    else:
        return HttpResponse('Invalid request method')

'''
def recommend_clothes(request):
    user_id = request.COOKIES.get('user_id')
    user_pictures = UserPicture.objects.filter(user_id=user_id)
    image_paths = {}
    for picture in user_pictures:
        image_paths[picture.picture_name] = settings.MEDIA_URL + str(picture.picture)

    # 사용자가 가진 사진이 충분하지 않은 경우를 고려하여 기본 이미지 양식 유지
    default_image_paths = [
        settings.MEDIA_URL + "user_pictures/1.jpg",
        settings.MEDIA_URL + "user_pictures/1.jpg",
        settings.MEDIA_URL + "user_pictures/1.jpg",
    ]

    # 딕셔너리에서 임의의 3개의 이미지 선택
    if image_paths:
        selected_images = random.sample(list(image_paths.items()), min(3, len(image_paths)))
        default_image_paths = [image_path for _, image_path in selected_images]

    print("사용자가 가진 모든 이미지들:")
    for image_name, image_path in image_paths.items():
        print("이미지 이름:", image_name)
        print("이미지 경로:", image_path)



    print("선택된 이미지들:")
    for image_name, image_path in selected_images:
        print("이미지 이름:", image_name)
        print("이미지 경로:", image_path)

    # 선택된 이미지들의 정보를 전달
    return render(request, 'recommend/recommendation.html', {'default_image_paths': default_image_paths})


'''

'''
def recommend_clothes(request):
    user_id = request.COOKIES.get('user_id')
    user_pictures = UserPicture.objects.filter(user_id=user_id)
    image_paths = {}
    for picture in user_pictures:
        image_paths[picture.picture_name] = settings.MEDIA_URL + str(picture.picture)

    # 터미널에 사용자가 가진 사진 파일들 출력
    print("사용자가 가진 사진들:")
    for picture in user_pictures:
        print("사진 이름:", picture.picture_name)
        print("파일 경로:", picture.picture)

    # 사용자가 가진 사진들의 정보를 전달
    return render(request, 'recommend/recommendation.html', {'image_paths': image_paths})

    
    bottom_image =   "1.jpg"
    top_image    =   "1.jpg"
    outer_image  =   "1.jpg"

    # 기본 사진의 경로 설정
    default_image_paths = [
        settings.MEDIA_URL + "user_pictures/" + bottom_image,
        settings.MEDIA_URL + "user_pictures/" + top_image,
        settings.MEDIA_URL + "user_pictures/" + outer_image,
    ]
    # 기본 사진 경로들을 전달
    return render(request, 'recommend/recommendation.html', {'image_paths': default_image_paths})


'''