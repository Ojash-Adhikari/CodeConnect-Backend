from django.db import models

# Create your models here.
class CachedQuestion(models.Model):
    difficulty = models.CharField(max_length=20)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)