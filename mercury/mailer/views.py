import csv
import io

import boto3
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, GetUrlSerializer, TestEmailSerializer
from .utilities import check_email_validity, render_templates, send_email


class GetCSVView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permissions = (IsAuthenticated,)

    def get(self, request):
        response = {}

        object_url = "https://mercury-mailer.s3.ap-south-1.amazonaws.com/mercury.csv"

        response["url"] = object_url

        return Response(response, status=status.HTTP_200_OK)


class GetUrlView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = GetUrlSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data["image"]
        file_name = serializer.validated_data["file_name"]

        c = 1
        response = {
            "data": [],
        }

        s3_resource = boto3.resource("s3")
        bucket_name = "mercury-mailer"

        s3_resource.Bucket(bucket_name).put_object(
            Key=f"{file_name}.png",
            Body=image,
            ACL="public-read",
            ContentType="image/png",
            ContentDisposition="inline",
        )

        response["data"].append(
            f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{file_name}.png"
        )
        c += 1

        return Response(response, status=status.HTTP_200_OK)


class SendEmailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {}
        c = 1
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():

            file = serializer.validated_data["recipients"]

            s3_resource = boto3.resource("s3")
            bucket_name = "mercury-mailer"

            s3_resource.Bucket(bucket_name).put_object(
                Key="mercury.csv",
                Body=file,
                ACL="public-read",
                ContentType="text/csv",
                ContentDisposition="attachment",
            )

            file.seek(0)

            rejected = ""

            recipient_data = csv.DictReader(io.StringIO(file.read().decode()))
            data = next(recipient_data)
            for i in data:
                rejected += str(i) + ","
            rejected += "\n"

            file.seek(0)
            recipient_data = csv.DictReader(io.StringIO(file.read().decode()))

            for data in recipient_data:

                body_html = render_templates(
                    serializer.validated_data["body_mjml"], data
                )

                is_valid = check_email_validity(data["email"])

                if is_valid:

                    response[c] = send_email(
                        sender_name=serializer.validated_data["sender_name"],
                        sender_email=serializer.validated_data["sender_email"],
                        recipient_email=data["email"],
                        subject=serializer.validated_data["subject"],
                        body_text=serializer.validated_data["body_text"],
                        body_html=body_html,
                        aws_region=serializer.validated_data["aws_region"],
                    )

                else:
                    response[c] = "Not delivered"
                    for i in data:
                        rejected += data[i] + ","
                    rejected += "\n"

                c += 1

            s3_resource.Bucket(bucket_name).put_object(
                Key="mercury-rejected.csv",
                Body=bytes(rejected, "utf-8"),
                ACL="public-read",
                ContentType="text/csv",
                ContentDisposition="attachment",
            )

            response[
                "rejected_emails"
            ] = "https://mercury-mailer.s3.ap-south-1.amazonaws.com/mercury-rejected.csv"

            return Response(response, status=status.HTTP_200_OK)

        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class SendTestEmailView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {}
        c = 1
        serializer = TestEmailSerializer(data=request.data)

        rejected = ""

        if serializer.is_valid():

            file = serializer.validated_data["recipients"]

            s3_resource = boto3.resource("s3")
            bucket_name = "mercury-mailer"

            s3_resource.Bucket(bucket_name).put_object(
                Key="mercury.csv",
                Body=file,
                ACL="public-read",
                ContentType="text/csv",
                ContentDisposition="attachment",
            )

            rejected += "email" + "\n"

            file.seek(0)

            recipient_data = csv.DictReader(io.StringIO(file.read().decode()))
            data = [i for i in recipient_data]

            test_recipient_emails = serializer.validated_data[
                "test_recipient_emails"
            ] + [serializer.validated_data["sender_email"]]

            for email in test_recipient_emails:

                body_html = render_templates(
                    serializer.validated_data["body_mjml"], data[0]
                )

                is_valid = check_email_validity(email)

                if is_valid:
                    response[c] = send_email(
                        sender_name=serializer.validated_data["sender_name"],
                        sender_email=serializer.validated_data["sender_email"],
                        recipient_email=email,
                        subject=serializer.validated_data["subject"],
                        body_text=serializer.validated_data["body_text"],
                        body_html=body_html,
                        aws_region=serializer.validated_data["aws_region"],
                    )

                else:
                    response[c] = "Not delivered"
                    rejected += email + "\n"

                c += 1

            s3_resource.Bucket(bucket_name).put_object(
                Key="mercury-rejected-test.csv",
                Body=bytes(rejected, "utf-8"),
                ACL="public-read",
                ContentType="text/csv",
                ContentDisposition="attachment",
            )

            response[
                "rejected_emails"
            ] = "https://mercury-mailer.s3.ap-south-1.amazonaws.com/mercury-rejected-test.csv"

            return Response(response, status=status.HTTP_200_OK)

        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_404_NOT_FOUND)
