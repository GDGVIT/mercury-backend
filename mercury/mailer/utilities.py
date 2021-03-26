import boto3
from botocore.exceptions import ClientError
from mjml.mjml2html import mjml_to_html
from jinja2 import Template


def send_email(**info):
    SENDER = f"{info['sender_name']} <{info['sender_email']}>"

    RECIPIENT = info["recipient"]

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
    html = mjml_to_html(mjml)
    return html["html"]


def render_templates(mjml):
    html = toHTML(mjml)

    html = Template(html)

    final_html = html.render(
        {
            "name": "Abhiram",
        }
    )

    return final_html
