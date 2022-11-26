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
from django.db import transaction
import math

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

class GameResutls(APIView):
    def post(self, req):
        if req.data["key"] ==  "SqgfZ1SE4v3OKlWezV1ft3PrP3O17zi0pEU2O1FcRQORp5YUjv":
            data = req.data
            redScore = data["redScore"]
            blueScore = data["blueScore"]
            master = data["master"]
            playerTeam = data["playerTeam"]
            with transaction.atomic():
                game = Game.objects.create(redScore = redScore, blueScore = blueScore, master = master)
                for player in playerTeam:
                    playerDB = Player.objects.get(account_id = player["account_id"])
                    GameInfo.objects.create(gameID = game.id, 
                                            playerID = player["account_id"], 
                                            team = player["team"],
                                            name = playerDB.name,
                                            level = playerDB.level)
                self.setFansPlayer(redScore= redScore, blueScore= blueScore, playerTeams= playerTeam)
            return Response(data= {"gameID": game.id},status= status.HTTP_200_OK)  
        else:
            return Response(data= "not ok",status= status.HTTP_400_BAD_REQUEST)  
    def setFansPlayer(self, redScore, blueScore, playerTeams):
        for playerTeam in playerTeams:
            player = Player.objects.get(account_id = playerTeam["account_id"])
            if redScore > blueScore:
                if playerTeam["team"] == 0:
                    player.fans += 100
                    self.addExp(player= player, exp= 80)
                    player.save()
                else:
                    player.fans = max(player.fans - 50, 0)
                    self.addExp(player= player, exp= 20)
                    player.save()
            elif blueScore > redScore:
                if playerTeam["team"] == 1:
                    player.fans += 100
                    self.addExp(player= player, exp= 80)
                    player.save()
                else:
                    player.fans = max(player.fans - 50, 0)
                    self.addExp(player= player, exp= 20)
                    player.save()
            else:
                self.addExp(player= player, exp= 50)
    
    def addExp(self, player, exp):
        if player.level < 30:
            player.exp += exp
            if player.exp >= math.floor(1.4**(player.level-1) + 800):
                player.level += 1
                if player.level < 30:
                    player.exp -= math.floor(1.4**player.level + 800)
                else:
                    player.exp = 0                
                player.point += 1
        
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