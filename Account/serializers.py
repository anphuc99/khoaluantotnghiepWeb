from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import Account

class SeriAccount(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ("id", "name", "email", "username", "_token")
        
class AddAccount(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

class Login(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
class Token(serializers.Serializer):
    _token = serializers.CharField(max_length = 100)
