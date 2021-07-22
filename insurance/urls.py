from django.urls import path,re_path, include

from project import settings
from .views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = []
urlpatterns += staticfiles_urlpatterns()
urlpatterns = [
    path("", main.as_view(), name = "main_insurance"),
    path("add_request_for_a_call/", add_request_for_a_call),
    path("register/", register.as_view(), name = "register"),
    path("logout/", user_logout, name="logout"),
]
