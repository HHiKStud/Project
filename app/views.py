"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import BlogForm, FeedbackForm

from django.contrib.auth.forms import UserCreationForm ##lab 6
from django.shortcuts import render, redirect ##lab 6

from django.db import models ## lab 8
from .models import Blog ## lab 8

# lab 8.2
from .models import Comment # ������������� ������ ������������
from .forms import CommentForm # ������������� ����� ����� �����������

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html'
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html'
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html'
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html'
    )

def get_feedback(request): ## lab 5
    """Renders the feedback page. """
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # �������� ��������� ������
            feedback_data = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'site_rating': dict(form.fields['site_rating'].choices)[int(form.cleaned_data['site_rating'])],
                'liked_features':[ dict(form.fields['liked_features'].choices).get(int(value), 'liked_features')
                    for value in form.cleaned_data['liked_features']],
                'visit_frequency': dict(form.fields['visit_frequency'].choices)[form.cleaned_data['visit_frequency']],
                'age': form.cleaned_data['age'],
                'suggestions': form.cleaned_data['suggestions'],
            }
            
            return render(request, 'app/pool.html', {
                'form': form,
                'fb_data': feedback_data
            })
        else:
            render(request, 'app/pool.html', {'form': form})
    else:
        form = FeedbackForm()
        return render(request, 'app/pool.html', {'form': form})

class User: UserCreationForm ## lab 6

def registration(request):
    """Renders the registration page."""

    assert isinstance(request, HttpRequest)

    if request.method == "POST": # ����� �������� �����
        regform = UserCreationForm (request.POST)

        if regform.is_valid(): #��������� ����� �����
            regform = regform.save(commit=False) # �� ��������� ������������� ������ �����
            regform.is_staff = False # �������� ���� � ���������������� ������
            regform.is_active = True # �������� ������������
            regform.is_superuser = False # �� �������� ������������������
            regform.date_joined = datetime.now() # ���� �����������
            regform.last_login = datetime.now() # ���� ��������� �����������
            regform.save() # ��������� ��������� ����� ���������� ������

            return redirect('home') # ������������� �� ������� �������� ����� �����������
    else:
        regform = UserCreationForm() # �������� ������� ����� ��� ����� ������ ������ ������������

    return render(
        request,
        'app/registration.html',
        {
        'regform': regform, # �������� ����� � ������ ���-��������
        'year':datetime.now().year,
        }
    ) #lab 6

def blog(request): # lab 8
    """Renders the blog page."""

    assert isinstance(request, HttpRequest)

    posts = Blog.objects.all() # ������ �� ����� ���� ������ ����� �� ������
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Blog',
            'posts': posts, # �������� ������ ������ � ������ ���-��������
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr): # lab 8
    """Renders the blogpost page."""

    assert isinstance(request, HttpRequest)

    post = Blog.objects.get(id=parametr) # ������ �� ����� ���������� ������ �� ���������
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # ����� �������� ������ ����� �� ������ ������� POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # ��������� (��� ��� ����� ���� ��� � �����) � ������ ����������� (Comment) � ���� ����� ��������������� ������������
            comment_f.date = datetime.now() # ��������� � ������ ����������� (Comment) ������� ����
            comment_f.post = Blog.objects.get(id=parametr) # ��������� � ������ ����������� (Comment) ������, ��� ������� ������ �����������
            comment_f.save() # ��������� ��������� ����� ���������� �����
            return redirect('blogpost', parametr=post.id) # ������������� �� �� �� �������� ������ ����� �������� �����������
    else:
        form = CommentForm() # �������� ����� ��� ����� �����������

    return render(
        request,
        'app/blogpost.html',
        {
            'post': post, # �������� ���������� ������ � ������ ���-��������
            'comments': comments, # �������� ���� ������������ � ������ ������ � ������ ���-��������
            'form': form, # �������� ����� ���������� ����������� � ������ ���-��������
            'year':datetime.now().year,
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit = False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()
            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'add blog',
            'year': datetime.now().year,
            }
        )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html'
    )