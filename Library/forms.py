
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Book


# Registration Form
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit(
                'submit',
                'Register',
                css_class='btn btn-primary w-100'
            )
        )


# Book Management Form
class BookForm(forms.ModelForm):

    class Meta:
        model = Book

        fields = [
            'title',
            'author',
            'category',
            'isbn',
            'quantity'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit(
                'submit',
                'Save Book',
                css_class='btn btn-success'
            )
        )
