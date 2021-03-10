from django.conf.urls import url
from . import views

app_name = 'mailer'

urlpatterns = [
    url(r'^send', views.SendEmailView.as_view(), name="send_email"),
]