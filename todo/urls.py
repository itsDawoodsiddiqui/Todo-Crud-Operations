from . import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),

    # User Authetication Routes
    path('signup/', views.signup),
    path('login/', views.user_login),

    # Todo CRUD Routes
    path('todos/', views.listTodo, name='listTodo'),
    path('new/todo/', views.createTodo, name='createTodo'),
    path('delete/todo/<int:srno>/', views.deleteTodo, name='deleteTodo'),
    path('update/todo/<int:srno>/', views.updateTodo, name='updateTodo')
]
    

