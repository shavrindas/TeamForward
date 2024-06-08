
from django.test import TestCase, Client
from django.urls import reverse
from recommend.models import RecommendedClothes
from datetime import date

class TodayRecommendClothesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('today_recommend_clothes')

    def test_no_recommendation_for_today(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "오늘 날짜에 해당하는 추천 의류가 없습니다.")
        self.assertIsNone(response.context['recommendation'])

    def test_recommendation_exists_for_today(self):
        today = date.today()
        recommendation = RecommendedClothes.objects.create(date=today, clothing_item="T-Shirt", description="A cool T-Shirt for today.")
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recommendation'], recommendation)
        self.assertContains(response, "T-Shirt")

    def test_recommendation_query_error(self):
        # 인위적으로 오류를 발생시키기 위해 아무 레코드도 생성하지 않고 테스트
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "추천 의류를 찾는 중 오류가 발생했습니다.")
        self.assertIsNone(response.context['recommendation'])
