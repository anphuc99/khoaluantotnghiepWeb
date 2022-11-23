import email
from math import fabs
from tabnanny import check
from turtle import st
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddAccount, Login, SeriAccount, Token
from .models import Account
from django.db import IntegrityError
from Game.consumers import ChatConsumer
from websocket import create_connection
import hashlib
import base64
import binascii
import os
import json
# Create your views here.
class RegisterAPI(APIView):    
    def  post(self, request):
        mydata = AddAccount(data=request.data)
        if not mydata.is_valid():
            return Response(data="not ok", status=status.HTTP_400_BAD_REQUEST)      
        if not self.CheckUserName(username= mydata.data["username"]):
            return Response(data=dict(msg = "account_exists"), status=status.HTTP_400_BAD_REQUEST)
        try:
            data = self.AddAcount(mydata.data)
            return Response(data=data.data, status=status.HTTP_200_OK)
        except IntegrityError as e:           
            return Response(data=dict(msg = "has_error"), status=status.HTTP_400_BAD_REQUEST)  
    
    def CheckUserName(self, username):
        try:
            check = Account.objects.get(username = username)
            return False
        except Account.DoesNotExist:
            return True
            
    def AddAcount(self, data):
        name = data["name"]
        email = data["email"]
        username = data["username"]
        password = hashlib.md5(data["password"].encode('utf-8')).hexdigest()
        _token = binascii.hexlify(os.urandom(35)).decode();  
        account = Account.objects.create(name = name, email = email, username = username, password = password, _token = _token)
        data = SeriAccount(account)
        return data

class LoginAPI(APIView):
    def post(self, request):     
        loginData = Login(data=request.data)
        if not loginData.is_valid():
            return Response(data="not ok", status=status.HTTP_400_BAD_REQUEST)   
        username = loginData.data["username"]
        password = hashlib.md5(loginData.data["password"].encode('utf-8')).hexdigest()
        account = self.checkLogin(username= username, password= password)
        if not account:
            return Response(data=dict(msg = "login_fail"), status=status.HTTP_400_BAD_REQUEST)            
        else:            
            account = SeriAccount(self.getToken(username= username))
            return Response(data=account.data, status=status.HTTP_200_OK)
    def checkLogin(self, username, password):
        try:
            check = Account.objects.get(username = username, password = password)
            return check
        except Account.DoesNotExist:
            return False
    
    def getToken(self, username):        
        account = Account.objects.get(username = username)
        ws = create_connection("ws://localhost:8000/ws/socket-server/")
        print ("connected")
        ws.send(json.dumps( {
                "type": "logout",
                "data": account._token
            }))
        ws.close()
        _token = binascii.hexlify(os.urandom(35)).decode();  
        account._token = _token
        account.save()
        return account
    
class TokenAPI(APIView):
    def post(self, request):
        tokenData = Token(data= request.data)
        if not tokenData.is_valid():
            return Response(data="not ok", status=status.HTTP_400_BAD_REQUEST)   
        token = self.checkToken(_token = tokenData.data["_token"])
        if not token:
            return Response(data=dict(msg = "login_fail"), status=status.HTTP_400_BAD_REQUEST)   
        else:
            print(token.username)
            account = SeriAccount(LoginAPI.getToken(self= LoginAPI ,username = token.username))
            return Response(data=account.data, status=status.HTTP_200_OK) 
        
    def checkToken(self, _token):
        try:
            token = Account.objects.get(_token = _token)
            return token
        except:
            return False