from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import twilio.twiml

# Create your views here.


@csrf_exempt
def handle(request):
    response = twilio.twiml.Response()
    response.message("Thanks for the message")
    return HttpResponse(str(response))
