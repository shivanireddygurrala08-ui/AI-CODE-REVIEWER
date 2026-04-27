"""Forms for AI Code Reviewer."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CodeReview, CodeSnippet


class UserRegisterForm(UserCreationForm):
    """User registration form."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})


class UserLoginForm(AuthenticationForm):
    """User login form."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password'
        })
    )


class CodeReviewForm(forms.ModelForm):
    """Form for submitting code for review."""
    code_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'code-input',
            'placeholder': 'Paste your code here for review...',
            'rows': 15
        })
    )
    language = forms.ChoiceField(
        choices=[
            ('python', 'Python'),
            ('javascript', 'JavaScript'),
            ('java', 'Java'),
            ('cpp', 'C++'),
            ('csharp', 'C#'),
            ('go', 'Go'),
            ('rust', 'Rust'),
            ('ruby', 'Ruby'),
            ('php', 'PHP'),
            ('swift', 'Swift'),
            ('kotlin', 'Kotlin'),
            ('typescript', 'TypeScript'),
        ],
        widget=forms.Select(attrs={
            'class': 'language-select'
        })
    )
    
    class Meta:
        model = CodeReview
        fields = ['code_content', 'language']


class CodeSnippetForm(forms.ModelForm):
    """Form for creating code snippets."""
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Snippet title'
        })
    )
    code = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'code-input',
            'placeholder': 'Your code snippet',
            'rows': 10
        })
    )
    language = forms.ChoiceField(
        choices=[
            ('python', 'Python'),
            ('javascript', 'JavaScript'),
            ('java', 'Java'),
            ('cpp', 'C++'),
            ('csharp', 'C#'),
            ('go', 'Go'),
            ('rust', 'Rust'),
            ('ruby', 'Ruby'),
            ('php', 'PHP'),
        ],
        widget=forms.Select(attrs={
            'class': 'language-select'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Description (optional)',
            'rows': 3
        }),
        required=False
    )
    
    class Meta:
        model = CodeSnippet
        fields = ['title', 'code', 'language', 'description']