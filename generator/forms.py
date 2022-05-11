from .models import Parser, XPath, Url
from django import forms


# Форма для XPath
class XPathForm(forms.ModelForm):
    class Meta:
        model = XPath
        fields = ['section_name', 'xpath_url', 'xpath_method']


# Форма для парсера
class ParserForm(forms.ModelForm):
    class Meta:
        model = Parser
        fields = ['parser_name']


# Форма для ссылки на сайт
class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['url_name']
