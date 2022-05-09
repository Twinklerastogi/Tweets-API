from sqlite3 import Timestamp
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class User(models.Model):

    username = models.CharField(
        validators=[MinLengthValidator(8)], max_length=10,
        unique=True, null=False, blank=False)
    user_created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['username']
    

class Tweets(models.Model):

    text = models.TextField(
        validators=[MinLengthValidator(2), MaxLengthValidator(140)], 
        null=False, blank=False)
    tweet_created_at = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ['tweet_created_at']

    






    
