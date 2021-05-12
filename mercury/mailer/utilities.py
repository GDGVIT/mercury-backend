import boto3
import requests
from botocore.exceptions import ClientError
from jinja2 import Template
from mjml.mjml2html import mjml_to_html
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
            "6571d42e-8218-4aaa-8c6f-547c957e6b8d",
            "59bac571-8f7e-4af4-96cb-748b977af14d",
        ),
    )
    html = response.json()
    return html["html"]


def render_templates(mjml, recipient_info):
    html = toHTML(mjml)

    html = Template(html)

    final_html = html.render(recipient_info)

    return final_html
