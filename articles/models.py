from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db import models
from .tasks import refresh_articles


class Article(models.Model):
    title = models.TextField()
    url = models.URLField(unique=True, max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

scheduler = BlockingScheduler()
scheduler.add_job(
    refresh_articles.send,
    CronTrigger.from_crontab("* * * * *"),
)
scheduler.start()
