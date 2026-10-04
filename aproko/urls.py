"""
URL configuration for aproko project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from blogApp.views import (
    homeView, AboutView, singleBlogView, blogView,
    createBlog, editBlog, deleteBlog, addCategory,
    profileView, editProfileView, likeBlog, addComment, deleteComment
)
from accounts.views import signup_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homeView, name="home"),
    path("about/", AboutView, name="about"),
    path("single-blog/<str:slug>/", singleBlogView, name="single-blog"),
    path("blogs/", blogView, name="blogs"),
    path("create-blog/", createBlog, name="create-blog"),
    path("edit-blog/<str:slug>/", editBlog, name="edit-blog"),
    path("delete-blog/<str:slug>/", deleteBlog, name="delete-blog"),
    path("add-category/", addCategory, name="add-category"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", signup_view, name="signup"),
    path("profile/", profileView, name="profile"),
    path("profile/edit/", editProfileView, name="edit-profile"),
    path("like-blog/<str:slug>/", likeBlog, name="like-blog"),
    path("add-comment/<str:slug>/", addComment, name="add-comment"),
    path("delete-comment/<int:comment_id>/", deleteComment, name="delete-comment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
