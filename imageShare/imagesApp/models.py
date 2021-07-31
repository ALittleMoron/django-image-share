from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager


class ImageStatistic(models.Model):
    """Класс статистики для изображений"""

    views = models.PositiveBigIntegerField(default=0, verbose_name="Число просмотров")
    likes = models.PositiveBigIntegerField(default=0, verbose_name="Число лайков")
    dislikes = models.PositiveBigIntegerField(default=0, verbose_name="Число дизлайков")

    def __str__(self):
        return f"{self.views} v, {self.likes} l, {self.dislikes} d"

    def incrementViews(self):
        self.views = models.F('views') + 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
        ordering = ["-views"]


class ImageWithContent(models.Model):
    """Класс модели изображения с содержимым."""

    title = models.CharField(max_length=100, unique=True, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено в")
    image = models.ImageField(upload_to="uploads/%Y/%m/%d", verbose_name="Изображение")

    publisher = models.ForeignKey(
        get_user_model(),
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано?")

    tags = TaggableManager()
    statistic = models.OneToOneField(
        ImageStatistic, on_delete=models.CASCADE, null=True
    )

    def __str__(self) -> str:
        return str(self.publisher) + " - " + (self.title or "None title")

    def get_absolute_url(self):
        return reverse("imagesApp.detail", kwargs={"pk": self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        statistic = ImageStatistic()
        statistic.save()
        self.statistic = statistic
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    class Meta:
        verbose_name = "Изображение с содержимым"
        verbose_name_plural = "Изображения с содержимым"
        ordering = ["-created_at"]
