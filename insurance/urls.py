from django.urls import path,re_path, include

from project import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views
from .views import *


urlpatterns = []
urlpatterns += staticfiles_urlpatterns()
urlpatterns = [
    path("", Main.as_view(), name = "main_insurance"),

    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path("add_request_for_a_call/", add_request_for_a_call),

    path("register/", Register.as_view(), name = "register"),
    path("logout/", user_logout, name="logout"),
    path("search/", Search.as_view(),name = "search" ),
]
