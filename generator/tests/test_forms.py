from django.test import TestCase
from generator.forms import XPathForm, XPathGenerateForm, UrlForm, ParserForm, UserRegistrationForm


class XPathFormTest(TestCase):

    def test_section_name_label(self):
        form = XPathForm()
        self.assertTrue(form.fields['section_name'].label is None or
                        form.fields['section_name'].label == 'section name')

    def test_xpath_url_label(self):
        form = XPathForm()
        self.assertTrue(form.fields['xpath_url'].label is None or
                        form.fields['xpath_url'].label == 'xpath url')

    def test_xpath_method_label(self):
        form = XPathForm()
        self.assertTrue(form.fields['xpath_method'].label is None or
                        form.fields['xpath_method'].label == 'xpath method')


class XPathGenerateFormTest(TestCase):

    def test_xpath_method_label(self):
        form = XPathGenerateForm()
        self.assertTrue(form.fields['xpath_method'].label is None or
                        form.fields['xpath_method'].label == 'xpath method')

    def test_xpath_class_label(self):
        form = XPathGenerateForm()
        self.assertTrue(form.fields['xpath_class'].label is None or
                        form.fields['xpath_class'].label == 'xpath class')

    def test_xpath_additions_label(self):
        form = XPathGenerateForm()
        self.assertTrue(form.fields['xpath_additions'].label is None or
                        form.fields['xpath_additions'].label == 'xpath additions')


class UrlFormTest(TestCase):

    def test_url_name_label(self):
        form = UrlForm()
        self.assertTrue(form.fields['url_name'].label is None or
                        form.fields['url_name'].label == 'url name')


class ParserFormTest(TestCase):

    def test_parser_name_label(self):
        form = ParserForm()
        self.assertTrue(form.fields['parser_name'].label is None or
                        form.fields['parser_name'].label == 'parser name')


class UserRegistrationFormTest(TestCase):

    def test_password_label(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields['password'].label is None or
                        form.fields['password'].label == 'Password')

    def test_password2_label(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields['password2'].label is None or
                        form.fields['password2'].label == 'Repeat password')

    def test_username_label(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields['username'].label is None or
                        form.fields['username'].label == 'Username')

    def test_different_passwords(self):
        form_data = {'username': 'user', 'password': 'pas', 'password2': 'pas2'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_same_passwords(self):
        form_data = {'username': 'user', 'password': 'pas', 'password2': 'pas'}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
