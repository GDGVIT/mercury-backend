from django.shortcuts import render
from .serializers import RegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)

    context = {}

    if serializer.is_valid():
        account = serializer.save()

        context['response'] = "Account created successfully"
        context['email'] = account.email
        context['username'] = account.username

    else:
        context = serializer.errors

    return Response(context)
