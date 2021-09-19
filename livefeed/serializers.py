from rest_framework import serializers
import tweepy

class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    screen_name = serializers.CharField(max_length=200)
    url = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    verified = serializers.BooleanField()
    location = serializers.CharField(max_length=200)
    profile_image_url = serializers.URLField()
    following = serializers.BooleanField()