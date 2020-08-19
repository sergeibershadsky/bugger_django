from django.urls import path

from articles.views import ArticlesView, refresh_articles_view

urlpatterns = [
    path('posts/', ArticlesView.as_view({'get': 'list'}), name='posts'),
    path('force-refresh/', refresh_articles_view, name='force-refresh')
]
