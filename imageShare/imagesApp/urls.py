from django.urls import path

from .views import HomePage, Account


urlpatterns = [
    path('', HomePage.as_view(), name='homePage'),
    path('account/<str:user_name>', Account.as_view(), name='account'),
]