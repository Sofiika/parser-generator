from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse


# Модель XPath
class XPath(models.Model):
    # Словарь методов обработки XPath
    LOAN_METHOD = (
        ("article_text", "process_article_text"),
        ("singular_item", "process_singular_item"),
        ("date_item", "process_date_item"),
        ("plural_texts", "process_plural_texts"),
        ("external_links", "process_external_links"),
        ("array_item", "process_array_item"),
        ("text_array_from_string", "process_text_array_from_string"),
    )
    section_name = models.TextField(null=True, default='section 1')  # Название раздела для пользователя
    xpath_url = models.TextField()  # Формула XPath
    xpath_method = models.CharField(max_length=22, choices=LOAN_METHOD, default="article_text") # Метод обработки XPath
    xpath_class = models.TextField(default='section')
    xpath_additions = models.TextField(default='')
    parser = models.ForeignKey('Parser', to_field='id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.section_name + self.xpath_url

    def get_absolute_url_update(self):
        return reverse('xpath-update', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('xpath-delete', args=[str(self.id)])

    def get_absolute_url(self):
        return reverse('parser-info', args=[str(self.parser.id)])


class Url(models.Model):
    url_name = models.TextField()
    parser = models.ForeignKey('Parser', to_field='id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.url_name

    def get_absolute_url_update(self):
        return reverse('url-update', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('url-delete', args=[str(self.id)])

    def get_absolute_url(self):
        return reverse('parser-info', args=[str(self.parser.id)])


class Parser(models.Model):
    parser_name = models.TextField(null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.parser_name

    def get_absolute_url(self):
        return reverse('parser-detail', args=[str(self.id)])

    def get_absolute_url_info(self):
        return reverse('parser-info', args=[str(self.id)])

    def get_absolute_url_add_xpath(self):
        return reverse('xpath-create', args=[str(self.id)])

    def get_absolute_url_add_url(self):
        return reverse('url-create', args=[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('parser-delete', args=[str(self.id)])

    def get_absolute_url_download(self):
        return reverse('download-instruction', args=[str(self.id)])

    def get_absolute_url_download_text(self):
        return reverse('download-text', args=[str(self.id)])
