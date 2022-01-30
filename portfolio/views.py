from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import Projects, Category
from .forms import ProjectForm, UserRegisterForm, UserLoginForm, ContactForm


class HomeProjects(ListView):
    model = Projects
    template_name = 'portfolio/home.html'
    context_object_name = 'projects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Alexander's Portfolio"
        return context

    def get_queryset(self):
        return Projects.objects.filter(is_published=True).select_related('category')


class CategoryProjects(ListView):
    model = Projects
    template_name = 'portfolio/home.html'
    context_object_name = 'projects'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Projects.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewProject(DetailView):
    model = Projects
    template_name = 'portfolio/view_project.html'
    context_object_name = 'project'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Projects.objects.get(pk=self.kwargs['pk'])
        return context


class CreateProject(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'portfolio/add_project.html'
    login_url = '/admin/'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('portfolio:home')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'portfolio/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('portfolio:home')
    else:
        form = UserLoginForm
    return render(request, 'portfolio/user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('portfolio:user_login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'django_smtp_mail@mail.ru', ['sv88800@mail.ru'],
                             fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('portfolio:contact')
            else:
                messages.error(request, 'Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка валидации!')
    else:
        form = ContactForm()
    return render(request, 'portfolio/test.html', {'form': form})


# def add_project(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save()
#             return redirect(project)
#     else:
#         form = ProjectForm()
#     return render(request, 'portfolio/add_project.html', {'form': form})
