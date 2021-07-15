from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    # url(r"^register", views.registration_view, name="register"),
    url(r"^login", TokenObtainPairView.as_view(), name="token_obtain"),
    url(r"^login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
