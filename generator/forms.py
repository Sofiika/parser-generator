from .models import Parser, XPath, Url
from django import forms


# Форма для XPath
class XPathForm(forms.ModelForm):
    xpath_url = forms.CharField(required=False)

    class Meta:
        model = XPath
        fields = ['section_name', 'xpath_url']


class XPathGenerateForm(forms.ModelForm):
    class Meta:
        model = XPath
        fields = ['xpath_method', 'xpath_class', 'xpath_additions']

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
