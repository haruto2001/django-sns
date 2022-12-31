from django import forms
from accounts.models import User
from .models import Post


class PostForm(forms.ModelForm):
    """
    新規投稿フォーム
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'url']


class ProfileForm(forms.ModelForm):
    """
    プロフィール更新フォーム
    """
    class Meta:
        model = User
        fields = ['nickname', 'image', 'introduction', 'url']