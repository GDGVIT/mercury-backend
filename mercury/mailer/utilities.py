import boto3
from botocore.exceptions import ClientError
from jinja2 import Template
from mjml.mjml2html import mjml_to_html


def send_email(**info):
    """ Sends email """

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
    """ Converts MJML to HTML """

    html = mjml_to_html(mjml)
    return html["html"]


def render_templates(mjml, recipient_info):
    """ Converts MJML to HTML and returns after rendering values in the template tags """

    html = toHTML(mjml)

    html = Template(html)

    final_html = html.render(recipient_info)

    return final_html
