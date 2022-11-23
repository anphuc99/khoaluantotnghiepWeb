from rest_framework import serializers
from .models import Player

class ChooseCharater(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    _token = serializers.CharField(max_length=100)
    
class PlayerSeri (serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("account_id", "name", "level","exp", "fans", "speed", "jump", "shotForce", "point")
        
class AccountID (serializers.Serializer):
    account_id = serializers.IntegerField()
    
class AddPoint (serializers.Serializer):
    speed = serializers.IntegerField()
    jump = serializers.IntegerField()
    shotForce = serializers.IntegerField()
    point = serializers.IntegerField()
    _token = serializers.CharField()