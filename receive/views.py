from django.shortcuts import render
import twilio.twiml

# Create your views here.


def handle(request):
    response = twilio.twiml.Response()
    response.message("Thanks for the message")
    return str(response)
