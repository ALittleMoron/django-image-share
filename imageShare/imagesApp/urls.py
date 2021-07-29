from django.urls import path

from .views import (HomePage, Account, AddImage, UserLogin, user_logout,
                    UserRegister, ImageDetail, ImageDelete, ImageUpdate)


urlpatterns = [
    path('', HomePage.as_view(), name='imagesApp.homePage'),
    path('account/<str:username>', Account.as_view(), name='imagesApp.account'),
    path('image/<int:pk>', ImageDetail.as_view(), name='imagesApp.detail'),
    path('add-image', AddImage.as_view(), name='imagesApp.addImage'),
    path('image/<int:pk>/update', ImageUpdate.as_view(), name='imagesApp.update'),
    path('image/<int:pk>/delete', ImageDelete.as_view(), name='imagesApp.delete'),
    path('register', UserRegister.as_view(), name='imagesApp.register'),
    path('login', UserLogin.as_view(), name='imagesApp.login'),
    path('logout', user_logout, name='imagesApp.logout'),
]