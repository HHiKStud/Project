"""
Definition of models.
"""

from tabnanny import verbose
from turtle import mode
from typing import Self
from django.db import models
from django.contrib import admin ## lab 7
from datetime import datetime ## lab 7
from django.urls import reverse ## lab 7

from django.contrib.auth.models import User ## lab 7

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Опубликовано")
    image = models.FileField(default="temp.svg", verbose_name="Путь к картинке")

    # Методы
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"

admin.site.register(Blog)

# lab 8.2
class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")

    # Methods
    def __str__(self): #returns title
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    # Meta
    class Meta:
        db_table="Comment"
        ordering=["-date"]
        verbose_name="Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"

admin.site.register(Comment)