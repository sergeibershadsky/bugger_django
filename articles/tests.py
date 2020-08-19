from typing import List

from django.urls import reverse
from django.utils.crypto import get_random_string
from django_dramatiq.test import DramatiqTestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import ArticleFactory
from .tasks import refresh_articles_job
from .models import Article
from unittest.mock import patch


def fake_articles():
    return [
        {'title': get_random_string(),
         'url': f'http:{get_random_string()}.su'}
        for _ in range(30)
    ]


class ArticlesTestCase(APITestCase):

    def setUp(self):
        for _ in range(30):
            ArticleFactory()

    def test_retrieve_articles(self):
        url = reverse('posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data: List[dict] = response.json()
        self.assertEqual(len(data), 5, "Default response length")
        self.assertSetEqual(set(data[0].keys()), {'id', 'url', 'created', 'title'}, "Should contain fields")

        limit = 3
        offset = 1
        response = self.client.get(f'{url}?limit={limit}&offset={offset}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data: List[dict] = response.json()
        self.assertEqual(len(data), limit, "Custom limit")
        self.assertListEqual([el['id'] for el in data], [2, 3, 4], "Limited and sorted response")


class ScraperTestCase(DramatiqTestCase):
    def test_refresh_articles(self):
        url = reverse('force-refresh')
        with patch('articles.tasks.get_articles') as mock_get_articles:
            mock_get_articles.return_value = fake_articles()
            response = self.client.get(url)
            # refresh_articles_job.send()
        self.assertEqual(response.status_code, 200)
        self.broker.join("default")
        self.worker.join()

        self.assertEqual(len(Article.objects.all()), 30)
