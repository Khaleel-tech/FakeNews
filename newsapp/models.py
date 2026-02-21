from django.conf import settings
from django.db import models


class NewsCheck(models.Model):
    SOURCE_CHOICES = [
        ('Google', 'Google'),
        ('Reddit', 'Reddit'),
        ('Wikipedia', 'Wikipedia'),
        ('News Archive', 'News Archive'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news_checks')
    headline = models.CharField(max_length=200)
    content = models.TextField()
    classification = models.CharField(max_length=10)
    score = models.FloatField()
    source_reference = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.headline} ({self.classification})"
