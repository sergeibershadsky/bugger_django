import factory.fuzzy

from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    url = factory.Sequence(lambda link: f"https://{link}.com")
