from dataclasses import fields
from rest_framework import serializers
from .models import Tweets, User

class TweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ['id', 'text', 'tweet_created_at', 'user_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
        
    

    