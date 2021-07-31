from typing import Optional, Union

from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import (HttpResponse,
                              HttpResponsePermanentRedirect,
                              HttpResponseRedirect,
                              get_object_or_404,
                              redirect,
                              render)
from django.urls import reverse, reverse_lazy
from django.views.generic import (DetailView,
                                  ListView,
                                  View,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  FormView)

from .forms import (ImageForm, ImageUpdateForm, CustomAuthenticationForm, 
                    CustomUserCreationForm)
from .models import ImageWithContent


def user_logout(request: HttpRequest) -> Union[HttpResponseRedirect, 
                                               HttpResponsePermanentRedirect]:
    """ Функция-обработчик logout'а пользователя.

    Изначально планировалось всё написать в парадигме ООП (class-based view),
    но возникли проблемы с переадресацией пользователя на домашнюю страницу,
    которую я решил, но функцию переписывать не стал. И так работает и не 
    требует доработки.

    Args:
        request (HttpRequest): базовый request, кои используются везде в Django.

    Returns:
        Union[HttpResponseRedirect, HttpResponsePermanentRedirect]: стандартный
            return из redirect-функции.
    """
    logout(request)
    return redirect('imagesApp.homePage')


class UserLogin(LoginView):
    """ Класс обработки входа пользователя в систему.
    
    Практически не переопределялись никакие поля, кроме template_name (по 
    понятной причине) и authentication_form (для более красивого вывода формы).
    """
    template_name = 'imagesApp/login.html'
    authentication_form = CustomAuthenticationForm


class UserRegister(CreateView, FormView):
    """ Класс обработки регистрации пользователя в системе.
    
    Практически не переопределялись никакие поля, кроме template_name (по 
    понятной причине), form_class (для более красивого вывода формы) и 
    success_url.
    """
    template_name = 'imagesApp/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('imagesApp.login')


class HomePage(ListView):
    """ Класс обработки домашней страницы.
    
    Имеется пагинация по 12 элементов, вывод фото по дате их создания и тому,
    являются ли они опубликованными.
    """
    template_name = "imagesApp/homePage.html"
    queryset = ImageWithContent.objects.filter(is_published=True).order_by('created_at').all()
    context_object_name = 'images'
    paginate_by = 12
    
    def post(self, request: HttpRequest) -> HttpResponse:
        """ Переопределенный метод класса ListView для обработки поиска по
        названию фото и тэгам.
        """
        search = request.POST.get('search')
        query = ImageWithContent.objects.filter(
            Q(is_published=True),
            Q(title__icontains=search) | Q(tags__name=search)
        )

        return render(request, self.template_name, context={'images': query})


class AddImage(LoginRequiredMixin, CreateView):
    """ Класс обработки добавления пользователем картинки с контекстом. """
    form_class = ImageForm
    template_name = 'imagesApp/addImage.html'
    
    def form_valid(self, form: ImageForm) -> HttpResponseRedirect:
        """ Переопределенный метод класса CreateView для добавление автора
        на этапе, когда форма провалидировалась. 
        """
        form.instance.publisher = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.object.get_absolute_url())
    
    def post(self, request, *args, **kwargs):
        """ Переопределенный метод клааса CreateView для отправки сообщения об
        ошибки валидации формы.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error('Некорректные данные в форме!')
            return self.form_invalid(form)


class ImageDetail(DetailView):
    """ Класс отображения подробной информации о картинке. """
    model = ImageWithContent
    template_name = "imagesApp/imageDetail.html"
    context_object_name = 'image'
    
    def get_object(self, queryset=None):
        """ Переопределенный метод клааса DetailView для увеличения числа просмотра записи """
        item = super().get_object(queryset=queryset)
        if self.request.user.username != item.publisher.username:
            item.statistic.incrementViews()
        return item


class UserIsPublisher(UserPassesTestMixin):
    """ Класс проверки принадлежности пользователя к посту с картинкой. """
    def get_image(self):
        """ Метод, возвращающий объект картинки по id. """
        return get_object_or_404(ImageWithContent, pk=self.kwargs.get('pk'))

    def test_func(self) -> Optional[bool]:
        """ Метод, проверяющий пользователя на авторство в посте с картинкой.  """
        if self.request.user.is_authenticated:
            return self.request.user == self.get_image().publisher
        else:
            raise PermissionDenied('Извините, у вас нет доступа к этому разделу')


class ImageUpdate(UserIsPublisher, UpdateView):
    """Класс обновления информации о картинке. """
    model = ImageWithContent
    form_class = ImageUpdateForm
    template_name = 'imagesApp/imageUpdate.html'
    context_object_name = 'image'


class ImageDelete(UserIsPublisher, DeleteView):
    """Класс удаления картинки. """
    model = ImageWithContent
    template_name = 'imagesApp/imageDelete.html'
    context_object_name = 'image'
    success_url = '/'


class Account(ListView):
    model = ImageWithContent
    template_name = "imagesApp/userAccount.html"
    context_object_name = 'user'
    paginate_by = 24

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        UserModel = get_user_model()
        user = UserModel.objects.get(username=self.kwargs['username'])
        images = ImageWithContent.objects.filter(publisher__username=self.kwargs['username']).order_by('created_at').all()
        context['user'] = user
        context['images'] = images
        return context