from django.http import HttpRequest

from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView, View


class HomePage(ListView):
    template_name = 'imagesApp/homePage.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)


class Account(DetailView):
    pass
