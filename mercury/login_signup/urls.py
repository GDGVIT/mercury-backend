from django.conf.urls import url
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    url(r'^register', views.registration_view, name="register"),
    url(r'^login/$', TokenObtainPairView.as_view(), name="token_obtain"),
    url(r'^login/refresh', TokenRefreshView.as_view(), name="token_refresh"),
]
