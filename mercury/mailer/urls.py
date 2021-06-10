from django.conf.urls import url

from . import views

app_name = "mailer"

urlpatterns = [
    url(r"^get_image_url$", views.GetUrlView.as_view(), name="get_image_url"),
    url(r"^send$", views.SendEmailView.as_view(), name="send_email"),
    url(r"^send_test$", views.SendTestEmailView.as_view(), name="send_test_email"),
]
