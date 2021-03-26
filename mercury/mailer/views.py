from django.shortcuts import render
from rest_framework import decorators

# Create your views here.


from rest_framework.views import APIView
from .serializers import EmailSerializer
from rest_framework.response import Response


from .utilities import send_email, render_templates


class SendEmailView(APIView):
    def post(self, request):
        context = {}
        c = 1
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            recipients = (serializer.validated_data["recipients"],)

            body_html = render_templates(serializer.validated_data["body_mjml"])

            for recipient in recipients:

                context[c] = send_email(
                    sender_name=serializer.validated_data["sender_name"],
                    sender_email=serializer.validated_data["sender_email"],
                    recipient=recipient,
                    subject=serializer.validated_data["subject"],
                    body_text=serializer.validated_data["body_text"],
                    body_html=body_html,
                    aws_region=serializer.validated_data["aws_region"],
                )
                c += 1

        else:
            context = serializer.errors

        return Response(context)