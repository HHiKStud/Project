"""
Definition of forms.
"""

from xml.dom.minidom import Attr
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models # lab 8.2  
from .models import Comment # lab 8.2

from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class FeedbackForm(forms.Form):
    # Выпадающий список
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
        ('first_time', 'Впервые'),
    ]

    # Радиокнопки (оценка сайта)
    SITE_RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    # Чекбоксы (что понравилось)
    LIKED_FEATURES = [
        (1, 'Дизайн сайта'),
        (2, 'Скорость работы'),
        (3, 'Содержание'),
        (4, 'Навигация'),
    ]

    username = forms.CharField(
        label="Ваше имя",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Пожалуйста, укажите ваше имя'},
        required=True
    )
    
    email = forms.EmailField(
        label="Ваш email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={'invalid': 'Введите корректный email адрес'},
        required=True
    )
    
    # Радио кнопки
    site_rating = forms.ChoiceField(
        label="Общая оценка сайта",
        choices=SITE_RATING_CHOICES,
        widget=forms.RadioSelect,
        initial=5
    )
    
    # Чекбоксы
    liked_features = forms.MultipleChoiceField(
        label="Что вам понравилось? (отметьте все подходящие варианты)",
        choices=LIKED_FEATURES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    # Выпадающий список
    visit_frequency = forms.ChoiceField(
        label="Как часто вы посещаете наш сайт?",
        choices=FREQUENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Числовое поле с валидацией
    age = forms.IntegerField(
        label="Ваш возраст",
        min_value=12,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    # текстовое поле
    suggestions = forms.CharField(
        label="Ваши предложения по улучшению",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Расскажите нам ваши пожелания...'
        }),
        required=False
    )
    
    # Валидация длины имени
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username.strip()) < 2:
            raise forms.ValidationError("Имя слишком короткое")
        return username

# lab 8.2
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {'title':"Заголовок", 'description':"Краткое содержание", 'content':"Полное содержание", 'image':"Картинка"}