from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    sender_name = serializers.CharField(max_length=50)
    sender_email = serializers.EmailField()
    receipents = serializers.CharField(max_length=1000)
    subject = serializers.CharField(max_length=1000)
    body_text = serializers.CharField(max_length=5000)
    body_html = serializers.CharField(max_length=5000)
    aws_region = serializers.CharField(max_length=20)


