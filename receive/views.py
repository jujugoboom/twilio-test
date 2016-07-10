from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import twilio.twiml
from twilio.rest import TwilioRestClient
import random
import os
import phonenumbers

# Create your views here.

PERSONAL_NUMBER = os.environ.get("PERSONAL_NUMBER")

client = TwilioRestClient()


@csrf_exempt
def handle(request):
    from_number = request.POST.get("From")
    if from_number == PERSONAL_NUMBER:
        return HttpResponse(personal(request))
    else:
        return HttpResponse(forward(request))
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
        messages = client.messages.list(to=request.POST.get("To"))
        print messages
        latest = messages[0]
        print latest
        print latest.body
        print latest.date_sent
        for message in messages:
            if message.date_sent > latest.date_sent:
                latest = message
        response = twilio.twiml.Response()
        message = "From: %s To: %s Message: %s" % (latest.from_,
                                                   latest.to,
                                                   latest.message)
        response.message(message)
        return response
    else:
        total = body.split()
        to = convert_to_e164(total[0])
        from_number = request.POST.get("To")
        client.messages.create(from_=from_number, to=to, body=total[1:])
        response = twilio.twiml.Response()
        message = "Sent message \"%s\" to %s from %s" % (total[1:],
                                                         to,
                                                         from_number)
        response.message(message)
        return response


def forward(request):
    body = request.POST.get("Body")
    message_from = request.POST.get("From")
    message_to = request.POST.get("To")
    message = "Got message \"%s\" from %s" (body, message_from)
    client.messages.create(from_=message_to, to=PERSONAL_NUMBER, body=message)
    return twilio.twiml.Response()


def convert_to_e164(raw_phone):
    if not raw_phone:
        return

    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    phone_representation = phonenumbers.parse(raw_phone, parse_type)
    return phonenumbers.format_number(phone_representation,
                                      phonenumbers.PhoneNumberFormat.E164)
