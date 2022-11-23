from rest_framework import serializers
    

class resutls(serializers.Serializer):
    roomID = serializers.CharField()
    playerTeams = serializers.CharField()
    redScore = serializers.IntegerField()
    blueScore = serializers.IntegerField()

class Room(serializers.Serializer):
    _token = serializers.CharField()
    roomID = serializers.CharField()
    
class MasterClientOut(serializers.Serializer):
    _token = serializers.Serializer
    roomID = serializers.Serializer
    newMaster = serializers.Serializer