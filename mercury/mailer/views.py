from django.shortcuts import render
from rest_framework import decorators

# Create your views here.


from rest_framework.views import APIView
from .serializers import EmailSerializer
from rest_framework.response import Response

class SendEmailView(APIView):

    context = {}

    def post(self, request):
        serializer = EmailSerializer(request.data)

        if serializer.is_valid():
            sender_name = serializer.validated_data['sender_name']
            sender_email = serializer.validated_data['sender_email']
            receipents = serializer.validated_data['receipents']
            subject = serializer.validated_data['subject']
            body_text = serializer.validated_data['body_text']
            body_html = serializer.validated_data['body_html']
            aws_region = serializer.validated_data['aws_region']



            context = {}
            c=1

            for recipient in receipents.split(";"):
                SENDER = f"{sender_name} <{sender_email}>"

                RECIPIENT = recipient

                # Specify a configuration set. If you do not want to use a configuration
                # set, comment the following variable, and the
                # ConfigurationSetName=CONFIGURATION_SET argument below.
                # CONFIGURATION_SET = "ConfigSet"

                AWS_REGION = aws_region

                SUBJECT = subject

                # The email body for recipients with non-HTML email clients.
                BODY_TEXT = body_text

                # The HTML body of the email.
                BODY_HTML = body_html

                # The character encoding for the email.
                CHARSET = "UTF-8"

                # Create a new SES resource and specify a region.
                client = boto3.client('ses',region_name=AWS_REGION)

                # Try to send the email.
                try:
                    #Provide the contents of the email.
                    response = client.send_email(
                        Destination={
                            'ToAddresses': [
                                RECIPIENT,
                            ],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Charset': CHARSET,
                                    'Data': BODY_HTML,
                                },
                                'Text': {
                                    'Charset': CHARSET,
                                    'Data': BODY_TEXT,
                                },
                            },
                            'Subject': {
                                'Charset': CHARSET,
                                'Data': SUBJECT,
                            },
                        },
                        Source=SENDER,
                        # If you are not using a configuration set, comment or delete the
                        # following line
                        # ConfigurationSetName=CONFIGURATION_SET,
                    )



                # Display an error if something goes wrong.
                except ClientError as e:
                    print(e.response['Error']['Message'])
                    context[c] = e.response['Error']['Message']
                else:
                    context[c] = f"Email sent! Message ID: {response['MessageId']}"

                c+=1
            
            return Response(context)