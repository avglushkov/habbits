from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import User

# class UserRegisterForm(StyleFormMixin, UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2')
#
# class UserProfileForm(StyleFormMixin, forms.ModelForm):
#
#     class Meta:
#         model =User
#         fields = ('email', 'first_name', 'last_name', 'avatar',)
#
#
# class UserPasswordRecoveryForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('email',)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs["class"] = "form-control"
#
# class UserUpdateForm(StyleFormMixin,forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("is_active",)


#
