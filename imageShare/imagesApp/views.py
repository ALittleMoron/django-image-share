from typing import Union

from django.http import HttpRequest
from django.shortcuts import (HttpResponse,
                              HttpResponseRedirect,
                              HttpResponsePermanentRedirect,
                              redirect,
                              render)
from django.views.generic import (DetailView,
                                  ListView,
                                  View,
                                  CreateView,
                                  FormView)
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ImageForm, CustomAuthenticationForm, CustomUserCreationForm
from .models import ImageWithContent


def user_logout(request: HttpRequest) -> Union[HttpResponseRedirect, 
                                               HttpResponsePermanentRedirect]:
    logout(request)
    return redirect('imagesApp.homePage')


class UserLogin(LoginView):
    template_name = 'imagesApp/login.html'
    authentication_form = CustomAuthenticationForm


class UserRegister(CreateView, FormView):
    template_name = 'imagesApp/register.html'
    form_class = CustomUserCreationForm
    success_url = '/'


class HomePage(ListView):
    template_name = "imagesApp/homePage.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        query = ImageWithContent.objects.filter(is_published=True).all()
        return render(request, self.template_name, context={'images': query})

    def post(self, request: HttpRequest):
        search = request.POST.get('search')
        query = ImageWithContent.objects.filter(is_published=True,
                                                title__icontains=search).all()
        return render(request, self.template_name, context={'images': query})


class AddImage(CreateView):
    form_class = ImageForm
    template_name = 'imagesApp/addImage.html'


class Account(LoginRequiredMixin, View):
    pass
