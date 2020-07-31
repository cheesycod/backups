from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
class User(AbstractUser):
    auction_id = models.AutoField(primary_key=True)
    address = models.CharField(blank="true", max_length=10000)
    first_name = models.CharField(blank="true", max_length=10000)
    last_name = models.CharField(blank="true", max_length=10000)
    dob = models.DateTimeField(default=datetime.datetime(2000, 1, 1).strftime("%Y-%m-%d"))
class Item(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bidder = models.CharField(blank="true", max_length=512)
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    current_price = models.FloatField(max_length=15)
    price = models.FloatField(max_length=15)
    image = models.CharField(blank="true", max_length=10000)
    def __str__(self):
        return f"{self.name}"
