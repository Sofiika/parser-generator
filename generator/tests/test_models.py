from django.test import TestCase
from generator.models import XPath, Parser, Url


class XPathModelTest(TestCase):
    parser_id = ''

    @classmethod
    def setUpTestData(cls):
        parser = Parser.objects.create(parser_name='Parser')
        cls.parser_id = parser.id
        XPath.objects.create(section_name='Sec', xpath_url='//*[@class="section"]/p//text()',
                             xpath_method='article_text', parser=parser)

    def test_section_name_label(self):
        xpath = XPath.objects.get(id=1)
        field_label = xpath._meta.get_field('section_name').verbose_name
        self.assertEquals(field_label, 'section name')

    def test_xpath_url_label(self):
        xpath = XPath.objects.get(id=1)
        field_label = xpath._meta.get_field('xpath_url').verbose_name
        self.assertEquals(field_label, 'xpath url')

    def test_xpath_method_label(self):
        xpath = XPath.objects.get(id=1)
        field_label = xpath._meta.get_field('xpath_method').verbose_name
        self.assertEquals(field_label, 'xpath method')

    def test_xpath_class_label(self):
        xpath = XPath.objects.get(id=1)
        field_label = xpath._meta.get_field('xpath_class').verbose_name
        self.assertEquals(field_label, 'xpath class')

    def test_xpath_additions_label(self):
        xpath = XPath.objects.get(id=1)
        field_label = xpath._meta.get_field('xpath_additions').verbose_name
        self.assertEquals(field_label, 'xpath additions')

    def test_parser_label(self):
        xpath = XPath.objects.get(id=1)
        field_label = xpath._meta.get_field('parser').verbose_name
        self.assertEquals(field_label, 'parser')

    def test_xpath_method_max_length(self):
        xpath = XPath.objects.get(id=1)
        max_length = xpath._meta.get_field('xpath_method').max_length
        self.assertEquals(max_length, 22)

    def test_object_name(self):
        xpath = XPath.objects.get(id=1)
        expected_object_name = xpath.section_name + xpath.xpath_url
        self.assertEquals(expected_object_name, str(xpath))

    def test_absolute_url_update(self):
        xpath = XPath.objects.get(id=1)
        expected_url = '/generator/xpath/1/update'
        self.assertEquals(expected_url, xpath.get_absolute_url_update())

    def test_absolute_url_delete(self):
        xpath = XPath.objects.get(id=1)
        expected_url = '/generator/xpath/1/delete'
        self.assertEquals(expected_url, xpath.get_absolute_url_delete())

    def test_absolute_url(self):
        xpath = XPath.objects.get(id=1)
        expected_url = '/generator/parser_info/' + str(self.parser_id)
        self.assertEquals(expected_url, xpath.get_absolute_url())


class UrlModelTest(TestCase):
    parser_id = ''

    @classmethod
    def setUpTestData(cls):
        parser = Parser.objects.create(parser_name='Parser')
        cls.parser_id = parser.id
        Url.objects.create(url_name='https://stackoverflow.com/', parser=parser)

    def test_url_name_label(self):
        url = Url.objects.get(id=1)
        field_label = url._meta.get_field('url_name').verbose_name
        self.assertEquals(field_label, 'url name')

    def test_parser_label(self):
        url = Url.objects.get(id=1)
        field_label = url._meta.get_field('parser').verbose_name
        self.assertEquals(field_label, 'parser')

    def test_object_name(self):
        url = Url.objects.get(id=1)
        expected_object_name = url.url_name
        self.assertEquals(expected_object_name, str(url))

    def test_absolute_url_update(self):
        url = Url.objects.get(id=1)
        expected_url = '/generator/url/1/update'
        self.assertEquals(expected_url, url.get_absolute_url_update())

    def test_absolute_url_delete(self):
        url = Url.objects.get(id=1)
        expected_url = '/generator/url/1/delete'
        self.assertEquals(expected_url, url.get_absolute_url_delete())

    def test_absolute_url(self):
        url = Url.objects.get(id=1)
        expected_url = '/generator/parser_info/' + str(self.parser_id)
        self.assertEquals(expected_url, url.get_absolute_url())


class ParserModelTest(TestCase):
    parser_id = ''

    @classmethod
    def setUpTestData(cls):
        parser = Parser.objects.create(parser_name='Parser')
        cls.parser_id = parser.id

    def test_parser_name_label(self):
        parser = Parser.objects.get(id=self.parser_id)
        field_label = parser._meta.get_field('parser_name').verbose_name
        self.assertEquals(field_label, 'parser name')

    def test_id_label(self):
        parser = Parser.objects.get(id=self.parser_id)
        field_label = parser._meta.get_field('id').verbose_name
        self.assertEquals(field_label, 'id')

    def test_author_label(self):
        parser = Parser.objects.get(id=self.parser_id)
        field_label = parser._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_object_name(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_object_name = parser.parser_name
        self.assertEquals(expected_object_name, str(parser))

    def test_absolute_url(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/parser/' + str(self.parser_id)
        self.assertEquals(expected_url, parser.get_absolute_url())

    def test_absolute_url_info(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/parser_info/' + str(self.parser_id)
        self.assertEquals(expected_url, parser.get_absolute_url_info())

    def test_absolute_url_add_xpath(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/' + str(self.parser_id) + '/xpath/create'
        self.assertEquals(expected_url, parser.get_absolute_url_add_xpath())

    def test_absolute_url_add_url(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/' + str(self.parser_id) + '/url/create'
        self.assertEquals(expected_url, parser.get_absolute_url_add_url())

    def test_absolute_url_delete(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/parser/' + str(self.parser_id) + '/delete'
        self.assertEquals(expected_url, parser.get_absolute_url_delete())

    def test_absolute_url_download(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/download/' + str(self.parser_id)
        self.assertEquals(expected_url, parser.get_absolute_url_download())

    def test_absolute_url_download_text(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/download_text/' + str(self.parser_id)
        self.assertEquals(expected_url, parser.get_absolute_url_download_text())

    def test_absolute_url_download_pdf_text(self):
        parser = Parser.objects.get(id=self.parser_id)
        expected_url = '/generator/download_pdf_text/' + str(self.parser_id)
        self.assertEquals(expected_url, parser.get_absolute_url_download_pdf_text())
