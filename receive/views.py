from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import twilio.twiml
from twilio.rest import TwilioRestClient
import random
import os

# Create your views here.

PERSONAL_NUMBER = os.environ.get("PERSONAL_NUMBER")

client = TwilioRestClient()


@csrf_exempt
def handle(request):
    from_number = request.values.get("From", None)
    response = None
    if from_number == PERSONAL_NUMBER:
        response = personal(request)
    #else:
        #forward(request)
    if response is None:
        response = twilio.twiml.Response()
        response.message(str(random.randint(1, 2)))
    return HttpResponse(response)


def personal(request):
    body = request.body
    if body == "numbers":
        allnumbers = client.phone_numbers.list()
        numbers = ""
        for number in allnumbers:
            numbers += number.phone_number + "\n"
        response = twilio.twiml.Response()
        response.message(numbers)
        return response


'''def forward(request):'''
