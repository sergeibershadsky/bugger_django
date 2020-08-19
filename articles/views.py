from django.http import HttpResponse
from rest_framework import viewsets, filters
from .models import Article
from .serializers import ArticleSerializer
from .pagination import CustomPagination
from .tasks import refresh_articles


class ArticlesView(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter]


def refresh_articles_view(request):
    refresh_articles.send()
    return HttpResponse()
