import sys

import requests
from urllib.request import urlopen
from lxml import etree
from .models import Parser, XPath, Url
import json


class ParserGenerator:
    def get_instruction(xpaths, urls, parser):
        instruction = '{\n'
        instruction += '    "instruction": [\n'
        xpath_len = len(xpaths)
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
        instruction += '    "metadata": [{\n'
        instruction += '        "org_type": "media",\n'
        instruction += '        "parser_author": "' + str(parser.author) + '",\n'
        instruction += '        "parser_name": "' + parser.parser_name + '",\n'
        instruction += '        "topic_en": "everything"\n'
        instruction += '    }],\n'
        instruction += '    "parse": [{\n'
        instruction += '        "index": "md_thematic",\n'
        instruction += '        "link": [\n'
        url_len = len(urls)
        counter_u = 0
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

    def parse_instruction(instruction):
        results = []

        text = json.loads(instruction)
        xpaths = text['instruction']
        res = []
        for xpath in xpaths:
            res.append(xpath['name'])
        parse = text['parse']

        urls = []
        for par in parse:
            links = par['link']
            for link in links:
                urls.append(link)

        if not urls:
            tmp = ['Please add URL!', '']
            results.append(tmp)
            return results

        if not xpaths:
            tmp = ['Please add XPath!', '']
            results.append(tmp)
            return results

        responses = []
        for url in urls:
            response = urlopen(url)
            responses.append(response)

        htmlparser = etree.HTMLParser(encoding='utf-8')

        trees = []
        for response in responses:
            tree = etree.parse(response, htmlparser)
            trees.append(tree)


        for xpath in xpaths:
            parsed_text = []
            for tree in trees:
                try:
                    parsed_text.append(tree.xpath(bytes(xpath['xpath'], 'utf-8').decode("unicode_escape")))
                except:
                    txt = ['xpath incorrect']
                    parsed_text.append(txt)
            tmp = [xpath['name'], parsed_text]
            results.append(tmp)

        return results
