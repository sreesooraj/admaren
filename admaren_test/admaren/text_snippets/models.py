from django.db import models
from account.models import User
# Create your models here.

class Title(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Text(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="text_user")
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="text_title")
    text_snippet = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

