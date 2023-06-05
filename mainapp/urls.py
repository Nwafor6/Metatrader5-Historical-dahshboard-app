from django.urls import path
from . import views

urlpatterns=[
    path("", views.bgtransaction),
    path("account/", views.account_dashboard)
]