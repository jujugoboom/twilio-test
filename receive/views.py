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
    from_number = request.POST.get("From")
    if from_number == PERSONAL_NUMBER:
        return HttpResponse(personal(request))
    response = twilio.twiml.Response()
    response.message(str(random.randint(1, 2)))
    return HttpResponse(response)


def personal(request):
    body = request.POST.get("Body")
    if body == "numbers":
        allnumbers = client.phone_numbers.list()
        numbers = ""
        for number in allnumbers:
            numbers += number.phone_number + "\n"
        response = twilio.twiml.Response()
        response.message(numbers)
        return response
    elif body == "last":
        allnumbers = client.phone_numbers.list()
        latest = client.messages.list(to=allnumbers[0].phone_number)[0]
        for number in allnumbers:
            messages = client.messages.list(to=number.phone_number)
            for message in messages:
                if message.date_sent > latest.date_sent:
                    latest = message
        response = twilio.twiml.Response()
        message = "From: %s To: %s Message: %s" % (latest.from_,
                                                   latest.to,
                                                   latest.message)
        response.message(message)
        return response


'''def forward(request):'''
