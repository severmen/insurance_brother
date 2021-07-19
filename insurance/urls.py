from django.urls import path,re_path, include
from .views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("", main.as_view(), name = "main_insurance"),
    re_path("add_request_for_a_call/", add_request_for_a_call),
]
urlpatterns += staticfiles_urlpatterns()