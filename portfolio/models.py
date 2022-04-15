from django.db import models
from django.urls import reverse_lazy


class Projects(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='portfolio/images/%Y/%m/', blank=True,
                              verbose_name='Фото')
    url = models.URLField(blank=True, verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано?')
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 verbose_name='Категория')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        # the same as {$ url 'portfolio:view_project' object.pk $} in templates
        return reverse_lazy('portfolio:view_project', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, db_index=True,
                             verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse_lazy('portfolio:get_category',
                            kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)
