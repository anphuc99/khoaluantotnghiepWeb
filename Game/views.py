from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import resutls, Room, MasterClientOut
from .models import Game, GameInfo
from Player.models import Player
from Account.models import Account
from Player.serializers import PlayerSeri
from rest_framework.response import Response
from rest_framework import status
import json
from types import SimpleNamespace
from SoccerLegend.Global import Global
from django.db import connection

# Create your views here.

def cursor_to_dict(cursor):
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        rowIndex = 0
        rowData = {}
        for column in columns:
            rowData[column] = row[rowIndex]
            rowIndex += 1
        data.append(rowData)
    return data

def chat(req):
    return render(req,"chat/lobby.html")

class GameResutls(APIView):
    def post(self, req):
        data = resutls(data= req.data)
        if not data.is_valid():
            return Response(data="not ok", status=status.HTTP_400_BAD_REQUEST)    
        Items = json.loads(data["playerTeams"].value, object_hook=lambda d: SimpleNamespace(**d))
        info = []
        for Item in Items.Items:
            info.append({
                "account_id": Item.account_id,
                "team": Item.team
            })
        JsonInfo = json.dumps(info)
        game = Game.objects.create(info = JsonInfo, redScore = data["redScore"].value, blueScore = data["blueScore"].value)
        for item in info:
            player = Player.objects.get(account_id = item["account_id"])
            history = player.history
            if history == "":
                player.history = str(game.id)
            else:
                player.history = history + "," + str(game.id)
            redScore = data["redScore"].value
            blueScore = data["blueScore"].value
            
            if redScore > blueScore and item["team"] == 0:
                player.score = player.score + 1
            elif redScore < blueScore and item["team"] == 1:
                player.score = player.score + 1
            elif redScore == blueScore:
                player.score = player.score + 1            
            player.save()
        
        return Response(status=status.HTTP_200_OK)    
        
class GetTopRank(APIView):
    def get(self, req):
        players = Player.objects.all().order_by('fans').reverse()[:100]
        playerSeris = []
        for player in players:
            playerSeris.append(PlayerSeri(player).data)
        return Response(data= {"Items": playerSeris}, status= status.HTTP_200_OK)    
    
class GetMyRank(APIView):
    def get(self, req, account_id):
        players = Player.objects.all().order_by('fans').reverse()[:1000]        
        myRank = 0
        for player in players:
            if player.account_id == account_id:
                break
            myRank += 1
        return Response(data= myRank, status= status.HTTP_200_OK)    
    
class GetHistory(APIView):
    def get(self, req, account_id):
        cursor = connection.cursor()
        cursor.execute("CALL GetHistory("+str(account_id)+")")
        return Response(data= {"Items": cursor_to_dict(cursor=cursor)},status= status.HTTP_200_OK)  
    
class GetResultGame(APIView):
    def get(self, req, game_id):
        gameInfo = GameInfo.objects.filter(gameID = game_id).values()
        game = Game.objects.filter(id = game_id).values()
        return Response(data= {"game":game[0], "gameInfo": gameInfo},status= status.HTTP_200_OK)  