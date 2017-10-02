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
from chatbot.bus import bus

PAGE_ACCESS_TOKEN = "EAAB3WIrhIvQBACM7e0UnCrz6Mb800BBzsZALw4eUlXOIuZADxtvnvKs9xLMrzKI0cP3p01JRpBkuHpCaQuNVlqlbKqeLi2dcJC0FrlG0h32tBJhkLW2f1iVufRs8DLtxmHnydqwwZBDGuoLZC4acCnLscZAfBXe8vlJQzh2V70YpckUjvlq3P"
VERIFY_TOKEN = "2318934571"

'''
def snippet_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
jokes = { 'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""", 
"""Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""], 
'fat':      ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""", 
""" Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """], 
'dumb': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""", 
"""Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] }

'''
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
        if not joke_text:
            joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!" 

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
    joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
'''
def post_facebook_message(fbid, received_message):           
    print(fbid, received_message)
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN) 
    msg = ""
    try:
        msg += scheduler(received_message)
    except:
        print("error during applying scheduler function")
    try:
        msg += bus(received_message)
    except:
        print("error during applying bus function")
    print(msg)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":msg}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(response_msg)
    print(status)
    print('---post_facebook_message----')


# Create your views here.
class ChatView(APIView):
    def get(self, request, format=None):
        if request.GET['hub.verify_token'] == '01020304':
            return Response(int(request.GET['hub.challenge']))
        else:
            return Response('Error, invalid token')
    def post(self, request, format=None):
        try:
            incoming_message = json.loads(self.request.body.decode('utf-8'))
            # Facebook recommends going through every entry since they might send
            # multiple messages in a single call during high load
            for entry in incoming_message['entry']:
                for message in entry['messaging']:
                    # Check to make sure the received call is a message call
                    # This might be delivery, optin, postback for other events 

                    if 'message' in message:
                        # Print the message to the terminal
                        # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                        # are sent as attachments and must be handled accordingly. 
                        post_facebook_message(message['sender']['id'], message['message']['text'])  
        except:
            pass
        return HttpResponse()    
