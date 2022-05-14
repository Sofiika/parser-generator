from urllib.request import urlopen
from lxml import etree
import json


# Класс для работы с инструкциями парсера
class ParserGenerator:

    # Метод для создания инструкции в формате json
    def get_instruction(xpaths, urls, parser):
        instruction = '{\n'
        instruction += '    "instruction": [\n'
        xpath_len = len(xpaths)

        # Добавление информации о всех XPath
        counter = 0
        for xpath in xpaths:
            instruction += '        {\n'
            instruction += '            "name": "' + xpath.section_name + '",\n'
            instruction += '            "function": "' + xpath.xpath_method + '",\n'
            xpath_url = xpath.xpath_url.replace('"', '\\"')
            instruction += '            "xpath": "' + xpath_url + '"\n'
            if counter < xpath_len - 1:
                instruction += '        },\n'
            else:
                instruction += '        }\n'
            counter += 1
        instruction += '    ],\n'

        # Добавление метаданных
        instruction += '    "metadata": [{\n'
        instruction += '        "org_type": "media",\n'
        instruction += '        "parser_author": "' + str(parser.author) + '",\n'
        instruction += '        "parser_name": "' + parser.parser_name + '",\n'
        instruction += '        "topic_en": "everything"\n'
        instruction += '    }],\n'

        # Добавлениии информации о парсере
        instruction += '    "parse": [{\n'
        instruction += '        "index": "md_thematic",\n'
        instruction += '        "link": [\n'
        url_len = len(urls)
        counter_u = 0

        # Добавление всех ссылок
        for url in urls:
            instruction += '            "' + url.url_name + '"'
            if counter_u < url_len - 1:
                instruction += ',\n'
            else:
                instruction += '\n'
            counter_u += 1
        instruction += '        ],\n'
        instruction += '        "parser_type": "sitemap"\n'
        instruction += '    }]\n'
        instruction += '}'
        return instruction

    # Метод для извлечения информации с сайтов по инструкции
    def parse_instruction(instruction):
        results = []

        # Загрузка текста в формате json в список
        text = json.loads(instruction)

        # Получение всех XPath
        xpaths = text['instruction']
        res = []
        for xpath in xpaths:
            res.append(xpath['name'])

        # Получение всех ссылок на сайты
        parse = text['parse']
        urls = []
        for par in parse:
            links = par['link']
            for link in links:
                urls.append(link)

        # Если в парсере нет ссылки, пользователю выводится сообщение об этом
        if not urls:
            tmp = ['Please add URL!', '', '']
            results.append(tmp)
            return results

        # Если в парсере нет XPath, пользователю выводится сообщение об этом
        if not xpaths:
            tmp = ['Please add XPath!', '', '']
            results.append(tmp)
            return results

        # Создание подключений по всем ссылкам
        responses = []
        for url in urls:
            try:
                response = urlopen(url)
                responses.append(response)
            except:
                tmp = ['You can\'t parse this website: ' + url, '', '']
                results.append(tmp)
                return results

        # Получение деревьев кода страницы заданных сайтов
        htmlparser = etree.HTMLParser(encoding='utf-8')
        trees = []
        for response in responses:
            tree = etree.parse(response, htmlparser)
            trees.append(tree)

        # Для каждого XPath собирается информация по каждому дереву сайта
        for xpath in xpaths:
            parsed_text = []
            for tree in trees:
                try:
                    string = tree.xpath(bytes(xpath['xpath'], 'utf-8').decode("unicode_escape"))
                    string_strip = []
                    for s in string:
                        string_strip.append(s.strip())
                    if string_strip is not None:
                        parsed_text.append(string_strip)
                except:
                    txt = ['xpath incorrect']
                    parsed_text.append(txt)
            tmp = [xpath['name'], parsed_text, xpath['function']]
            results.append(tmp)

        return results
