from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.HomeProjects.as_view(), name='home'),
    path('category/<int:category_id>/', views.CategoryProjects.as_view(), name='get_category'),
    path('project/<int:pk>/', views.ViewProject.as_view(), name='view_project'),
    path('project/add_project', views.CreateProject.as_view(), name='add_project'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('test/', views.contact, name='contact'),
]
