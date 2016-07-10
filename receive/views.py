from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import twilio.twiml
import random

# Create your views here.


@csrf_exempt
def handle(request):
    response = twilio.twiml.Response()
    response.message(str(random.randint(1, 2)))
    return HttpResponse(response)
