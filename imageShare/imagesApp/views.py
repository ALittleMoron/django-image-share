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
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
        query = ImageWithContent.objects.filter(is_published=True).order_by('?').all()
        return render(request, self.template_name, context={'images': query})

    def post(self, request: HttpRequest) -> HttpResponse:
        search = request.POST.get('search')
        query = ImageWithContent.objects.filter(is_published=True,
                                                title__icontains=search).all()
        return render(request, self.template_name, context={'images': query})


class AddImage(LoginRequiredMixin, CreateView):
    form_class = ImageForm
    template_name = 'imagesApp/addImage.html'
    
    def form_valid(self, form):
        form.instance.publisher = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.object.get_absolute_url())
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error('Некорректные данные в форме!')
            return self.form_invalid(form)


class ImageDetail(DetailView):
    model = ImageWithContent
    template_name = "imagesApp/imageDetail.html"
    context_object_name = 'image'


class Account(LoginRequiredMixin, View):
    pass
