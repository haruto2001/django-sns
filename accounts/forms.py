from allauth.account.forms import SignupForm
from django import forms


class SignupForm(SignupForm):
    nickname = forms.CharField(max_length=25, label='ニックネーム')

    def signup(self, request, user):
        user.nickname = self.cleaned_data['nickname']
        return user