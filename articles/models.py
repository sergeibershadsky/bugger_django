from django.db import models


class Article(models.Model):
    title = models.TextField()
    url = models.URLField(unique=True, max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

