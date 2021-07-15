import re

import boto3
import chevron
import requests
from botocore.exceptions import ClientError
from decouple import config
from requests.auth import HTTPBasicAuth


def send_email(**info):
    SENDER = f"{info['sender_name']} <{info['sender_email']}>"

    RECIPIENT = info["recipient_email"]

    AWS_REGION = info["aws_region"]

    SUBJECT = info["subject"]

    BODY_TEXT = info["body_text"]

    BODY_HTML = info["body_html"]

    CHARSET = "UTF-8"

    client = boto3.client("ses", region_name=AWS_REGION)

    try:

        response = client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": BODY_HTML,
                    },
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        return e.response["Error"]["Message"]
    else:
        return f"Email sent! Message ID: {response['MessageId']}"


def toHTML(mjml):
    response = requests.post(
        "https://api.mjml.io/v1/render",
        json={"mjml": mjml},
        auth=HTTPBasicAuth(
            config("MJML_API_USERNAME"),
            config("MJML_API_PASSWORD"),
        ),
    )
    html = response.json()
    return html["html"]


def render_templates(mjml, recipient_info):
    html = toHTML(mjml)

    final_html = chevron.render(html, recipient_info)

    return final_html


def check_email_validity(email):
    pattern = re.compile("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")

    is_valid = re.match(pattern, email)

    return is_valid
