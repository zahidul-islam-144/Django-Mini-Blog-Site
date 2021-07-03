from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile

# here i have created extra form for adding an extra field i want 
class SignUpForm(UserCreationForm): # here existing form inherits django built form
    email = forms.EmailField(label="Email Address", required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2') # extra field is 'email'

class UserProfileChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class ProfilePic(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic',]
        