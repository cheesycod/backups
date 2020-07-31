from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
class Email(models.Model):
    dest_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destination")
    subject = models.CharField(blank=True, max_length=1024, default="No subject provided")
    body = models.TextField(blank=True, default="No message provided")
    date = models.DateTimeField(default=timezone.now)
    sender = models.IntegerField()