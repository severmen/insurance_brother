from django.urls import path,re_path, include

from project import settings
from .views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = []
urlpatterns += staticfiles_urlpatterns()
urlpatterns = [
    path("", Main.as_view(), name = "main_insurance"),
    path("add_request_for_a_call/", add_request_for_a_call),
    path("register/", Register.as_view(), name = "register"),
    path("logout/", user_logout, name="logout"),
    path("password_recovery/",PasswordRecovery.as_view() , name="password_recovery"),
    re_path(r"registration_confirmations/([0-9]{1,10})/(.{10,160})",RegistrationConfirmations.as_view() )
]
