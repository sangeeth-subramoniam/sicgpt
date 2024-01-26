from django import forms
from django.contrib.auth.models import User
from .models import user_profile


class User_form(forms.ModelForm):


    password = forms.CharField(widget=forms.PasswordInput(), label="パスワード*")
    
    class Meta:
        model = User
        fields = ("username", "email" , "password")
        
        labels = {
        "username": "ユーザー名*",
        "email" : "メル*",
        }

        help_texts = {
            'username': "150 文字以内。 文字、数字、@/./+/-/_ のみ。",
        }




class user_profile_form(forms.ModelForm):
    
    class Meta:
        model = user_profile
        # fields = ("profile_picture", "website" , "bio")
        fields = ("profile_picture",)
        labels={
            "profile_picture":"画像"
        }