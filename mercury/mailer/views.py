from django.shortcuts import render
from rest_framework import decorators
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

import csv
import io

from .serializers import EmailSerializer
from .utilities import send_email, render_templates


class SendEmailView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        context = {}
        c = 1
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data["recipients"]

            recipient_data = csv.DictReader(io.StringIO(file.read().decode()))

            for data in recipient_data:

                body_html = render_templates(
                    serializer.validated_data["body_mjml"], data
                )

                context[c] = send_email(
                    sender_name=serializer.validated_data["sender_name"],
                    sender_email=serializer.validated_data["sender_email"],
                    recipient_email=data["email"],
                    subject=serializer.validated_data["subject"],
                    body_text=serializer.validated_data["body_text"],
                    body_html=body_html,
                    aws_region=serializer.validated_data["aws_region"],
                )
                c += 1

        else:
            context = serializer.errors

        return Response(context)