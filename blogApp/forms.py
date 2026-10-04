from django import forms
from .models import Blog, Category, Profile, Comment
from django.contrib.auth.models import User


class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "category",
            "thumbnail",
            "is_published"
        ]


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["address", "profile_picture"]       


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]        




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }