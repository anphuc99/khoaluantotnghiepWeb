from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChooseCharater, PlayerSeri, AccountID, AddPoint
from .models import Player
from Account.models import Account
from django.db import IntegrityError
import socket
# Create your views here.

class ChooseCharaterAPI(APIView):
    def post(self, request):
        data = ChooseCharater(data = request.data)
        if not data.is_valid():
            return Response(data="not ok", status=status.HTTP_400_BAD_REQUEST)      
        _token = data.data["_token"]
        name = data.data["name"]
        if not self.checkName(name= name):
            return Response(data=dict(msg = "name_exists"), status= status.HTTP_400_BAD_REQUEST)
        account = Account.objects.get(_token = _token)
        player = Player.objects.create(account_id = account.id, name = name)
        player = PlayerSeri(player)
        return Response(data= player.data, status= status.HTTP_200_OK)
    
    def checkName(self, name):
        try:
            player = Player.objects.get(name = name)
            return False
        except Player.DoesNotExist:
            return True
        
class CheckPlayerAPI(APIView):
    def post(self, request):
        try:
            account_id = AccountID(data= request.data)
            if not account_id.is_valid():
                return Response(data="not request", status=status.HTTP_400_BAD_REQUEST)    
            print(account_id.data["account_id"])
            player = Player.objects.get(account_id = account_id.data["account_id"])
            player = PlayerSeri(player)
            return Response(data= player.data, status= status.HTTP_200_OK)
        except Player.DoesNotExist:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        
class SetMultiplierAPI(APIView):
    def post(self, request):
        try:
            data = AddPoint(data= request.data)
            if not data.is_valid():
                print("is_valid")
                return Response(data="not request", status=status.HTTP_400_BAD_REQUEST)    
            speed = data["speed"].value
            jump = data["jump"].value
            shotForce = data["shotForce"].value
            point = data["point"].value
            _token = data["_token"].value            
            account = Account.objects.get(_token = _token)
            player = Player.objects.get(account_id = account.id)
            if speed + jump + shotForce + point == player.level:            
                player.speed = speed
                player.jump = jump
                player.shotForce = shotForce
                player.point = point
                player.save()
            else:
                return Response(status= status.HTTP_400_BAD_REQUEST)                          
            return Response(status= status.HTTP_200_OK)
        except Account.DoesNotExist:
            print("Account.DoesNotExist")
            return Response(status= status.HTTP_400_BAD_REQUEST)  

