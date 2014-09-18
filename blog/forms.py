from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from blog.models import Post, Comment

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)

    def __init__(self, *args, **kwargs):
      super(MyRegistrationForm, self).__init__(*args, **kwargs)
      for myField in self.fields:
        self.fields[myField].widget.attrs['class'] = 'form-control'
        self.fields[myField].widget.attrs['placeholder'] = self.fields[myField].label or myField
        
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()

        return user

class PostForm(forms.ModelForm):
    title = forms.CharField(required = True)
    body = forms.CharField(widget=forms.Textarea, required = True)
    docfile = forms.FileField(label='Select a file', required = False)

    def __init__(self, *args, **kwargs):
      super(PostForm, self).__init__(*args, **kwargs)
      for myField in self.fields:
        self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        exclude = ['author']
        fields = ['title', 'body', 'docfile', 'published_date']

class CommentForm(forms.ModelForm):
    body = forms.CharField(required = True, label='Comment')

    def __init__(self, *args, **kwargs):
      super(CommentForm, self).__init__(*args, **kwargs)
      for myField in self.fields:
        self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        exclude = ['post']
        fields = ['body']
