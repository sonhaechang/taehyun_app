from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
    SetPasswordForm
)
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

from accounts.models import SearchTagList, SearchAccountList

User = get_user_model()

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = _('아이디 또는 비밀번호가 올바르지 않습니다')
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Email')
        })
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })


class SignupForm(UserCreationForm):
	instagram_pw = forms.CharField(widget=forms.PasswordInput())

	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('instagram_id', 'instagram_pw',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		class_update_fields = ['username', 'password1', 'password2', 'instagram_id', 'instagram_pw']
		for field_name in class_update_fields:
			self.fields[field_name].label = ''
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control',
			})
		self.fields['username'].validators = [validate_email]
		self.fields['username'].help_text = _('이메일 형식으로 입력해주세요.')
		self.fields['username'].widget.attrs.update({'placeholder': _('Email')})
		self.fields['password1'].widget.attrs.update({'placeholder': _('password')})
		self.fields['password2'].widget.attrs.update({'placeholder': _('비밀번호 확인')})
		self.fields['instagram_id'].widget.attrs.update({'placeholder': _('인스타그램 아이디')})
		self.fields['instagram_pw'].widget.attrs.update({'placeholder': _('인스타그램 비밀번호')})
		self.fields['instagram_pw'].help_text = _('인스타그램 비밀번호를 입력해주세요.')


class PasswordChangeForm(AuthPasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		class_update_fields = ['old_password', 'new_password1', 'new_password2']
		self.fields['old_password'].widget.attrs.pop("autofocus", None)
		for field_name in class_update_fields:
			self.fields[field_name].widget.attrs.update({'class': 'form-control',})

		self.fields['old_password'].widget.attrs.update({'placeholder': _('이전 비밀번호')})
		self.fields['new_password1'].widget.attrs.update({'placeholder': _('새 비밀번호')})
		self.fields['new_password2'].widget.attrs.update({'placeholder': _('새 비밀번호 확인')})


class EditInstaAccountsInfoForm(forms.ModelForm):
	instagram_pw = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ['instagram_id', 'instagram_pw']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		class_update_fields = ['instagram_id', 'instagram_pw']
		self.fields['instagram_id'].widget.attrs.update({'placeholder': _('인스타그램 아이디')})
		self.fields['instagram_pw'].widget.attrs.update({'placeholder': _('인스타그램 비밀번호')})
		self.fields['instagram_pw'].help_text = _('인스타그램 비밀번호를 입력해주세요.')


class SearchTagForm(forms.ModelForm):
	class Meta:
		model = SearchTagList
		fields = ['name']


class SearchAccountForm(forms.ModelForm):
	class Meta:
			model = SearchAccountList
			fields = ['name']