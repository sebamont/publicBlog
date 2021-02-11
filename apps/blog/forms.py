from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Suggestion
from ckeditor.widgets import CKEditorWidget


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Email')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

#Class dateInput to use input_type = 'date'
class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['alias','birthday']
        labels = {
            'alias' : 'Alias or Nick:',
            'birthday' : 'Select your birthday',
        }
        widgets = {
            'alias':forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder': 'The nick will be displayed on your suggestions'
                }
            ),
            'birthday':DateInput(
                format=('%d-%m-%Y'),
                attrs={
                    'class':'form-control',
                    'placeholder':'Select a date',
                }
            ),
        }

class SuggestionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget)
    class Meta:
        model = Suggestion
        fields = ['title', 'image', 'content', 'type', 'category', 'tag']
        labels = {
            'title' : 'Suggestion title',
            'image' : 'Insert a valid image url (.jpg or .png)',
            'type' : 'Suggestion Type',
            'category': 'Suggestion Category',
            'tag': 'Suggestion Tag/s'
        }
        widgets = {
            'title':forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder': 'e.g. Movie Name - 2011'
                }
            ),
            'image':forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder': 'eg. https://via.placeholder.com/1900x1200'
                }
            ),
            # 'type':forms.ChoiceField(
            #     attrs = {
            #         'class' : 'form-control',
            #     }
            # ),
            # 'category':forms.ChoiceWidget(
            #     attrs = {
            #         'class' : 'form-control',
            #     }
            # ),
            # 'tag':forms.CheckboxSelectMultiple(
            #     attrs = {
            #         'class' : 'form-control',
            #     }
            #),

        }