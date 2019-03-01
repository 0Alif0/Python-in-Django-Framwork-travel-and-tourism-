
from django.urls import path
from . import views
app_name="blogapp"

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('author/<name>', views.getauthor.as_view(), name="author"),
    path('article/<int:id>', views.getsingle.as_view(), name="single_post"),
    path('topic/<name>', views.getTopic, name="topic"),
    path('login', views.getLogin.as_view(), name="login"),
    path('logout', views.getlogout, name="logout"),
    path('create', views.getcreate, name="create"),
    path('profile', views.getProfile, name="profile"),
    path('update/<int:pid>', views.getUpdate, name="update"),
    path('delete/<int:pid>', views.getDelete, name="delete"),
    path('register', views.getRegister, name="register"),
    path('topics', views.getCategory, name="category"),
    path('create/topic', views.createTopic, name="createTopic")
]
