from django.shortcuts import render
import json, requests, random, re
from django.http.response import HttpResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pprint
import json
from chatbot.schedule import scheduler
from chatbot.ara import AraChatbot
import chatbot.credentials as credit 
from chatbot.bus import bus
from chatbot.models import Account
from chatbot.AraChatbot.messenger import Session

PAGE_ACCESS_TOKEN = "EAAB3WIrhIvQBACM7e0UnCrz6Mb800BBzsZALw4eUlXOIuZADxtvnvKs9xLMrzKI0cP3p01JRpBkuHpCaQuNVlqlbKqeLi2dcJC0FrlG0h32tBJhkLW2f1iVufRs8DLtxmHnydqwwZBDGuoLZC4acCnLscZAfBXe8vlJQzh2V70YpckUjvlq3P"
VERIFY_TOKEN = "2318934571"



# Create your views here.
class ChatView(APIView):
    def __init__(self):
        self.ara_session = Session()
        self.counter = 0
    def get(self, request, format=None):
        if request.GET['hub.verify_token'] == '01020304':
            return Response(int(request.GET['hub.challenge']))
        else:
            return Response('Error, invalid token')
    def post(self, request, format=None):
        print('counter {}'.format(self.counter))
        self.counter += 1
        try:
            incoming_message = json.loads(self.request.body.decode('utf-8'))
            # Facebook recommends going through every entry since they might send
            # multiple messages in a single call during high load
            for entry in incoming_message['entry']:
                msg = ""
                for message in entry['messaging']:
                    # Check to make sure the received call is a message call
                    # This might be delivery, optin, postback for other events 

                    if 'message' in message:
                        # Print the message to the terminal
                        # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                        # are sent as attachments and must be handled accordingly. 
                        self.post_facebook_message(message['sender']['id'], message['message']['text'])
                        #if not User.objects.get(fid=message['sender']['id']):
                        try:
                            Account.objects.get(fbid=message['sender']['id'])
                        except Exception as e:
                            print(e)
                            try:
                                usr = Account(fbid = message['sender']['id'], context="")
                                usr.save()
                            except Exception as e:
                                print(e)
                                print('error during saving account')


        except:
            pass
        return HttpResponse()    

    def post_facebook_message(self, fbid, received_message):           
        print(fbid, received_message)
        post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN) 
        #print(received_message)
        #ara = AraChatbot(credit.USERNAME, credit.PASSWORD)
        #msg = ara.answer(received_message)

        msg = ""
        try:
            msg += self.ara_session.call(fbid, received_message)[-1] 
        except:
            print("error during applying arachatbot")
        try:
            msg += bus(received_message)
        except:
            print("error during applying bus function")

        if msg == "":
            try:
                if '언제' in received_message: 
                    msg += scheduler(received_message)
            except:
                print("error during applying scheduler function")
        print(msg)
        if len(msg) == 0:
            msg = received_message
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
        print(response_msg)
        print(status)
        print('---post_facebook_message----')
