from django.urls import path
from . import views

app_name="account"
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.account, name="account"),
    path('kyc-reg/', views.kyc_regisration, name="kyc-reg"),
]
