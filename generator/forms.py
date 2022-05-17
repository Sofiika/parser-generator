from .models import Parser, XPath, Url
from django import forms
from django.contrib.auth.models import User


# Форма для XPath
class XPathForm(forms.ModelForm):
    section_name = forms.CharField(help_text=XPath._meta.get_field('section_name').help_text)
    xpath_url = forms.CharField(required=False, help_text=XPath._meta.get_field('xpath_url').help_text)
    xpath_method = forms.ChoiceField(help_text=XPath._meta.get_field('xpath_method').help_text,
                                     choices=XPath.LOAN_METHOD)

    class Meta:
        model = XPath
        fields = ['section_name', 'xpath_url', 'xpath_method']


# Форма для генерации XPath
class XPathGenerateForm(forms.ModelForm):
    xpath_method = forms.ChoiceField(help_text=XPath._meta.get_field('xpath_method').help_text,
                                     choices=XPath.LOAN_METHOD)
    xpath_class = forms.CharField(help_text=XPath._meta.get_field('xpath_class').help_text)
    xpath_additions = forms.CharField(required=False, help_text=XPath._meta.get_field('xpath_additions').help_text)

    class Meta:
        model = XPath
        fields = ['xpath_method', 'xpath_class', 'xpath_additions']


# Форма для парсера
class ParserForm(forms.ModelForm):
    parser_name = forms.CharField(help_text=Parser._meta.get_field('parser_name').help_text)

    class Meta:
        model = Parser
        fields = ['parser_name']


# Форма для ссылки на сайт
class UrlForm(forms.ModelForm):
    url_name = forms.CharField(help_text=Url._meta.get_field('url_name').help_text)

    class Meta:
        model = Url
        fields = ['url_name']


# Форма для регистрации пользователя
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
