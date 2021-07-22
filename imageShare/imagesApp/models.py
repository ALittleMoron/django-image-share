from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager


class ImageWithContent(models.Model):
    """ Класс модели изображения с содержимым. """
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано в')
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено в')
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d',
        verbose_name='Изображение'
    )
    publisher = models.ForeignKey(
        get_user_model(),
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано?"
    )
    tags = TaggableManager()

    def __str__(self) -> str:
        return str(self.publisher) + ' - ' + (self.title or 'None title')
    
    def get_absolute_url(self):
        return reverse("imagesApp.detail", kwargs={"pk": self.pk})
    
    
    class Meta:
        verbose_name = "Изображение с содержимым"
        verbose_name_plural = "Изображения с содержимым"
        ordering = ['-created_at']