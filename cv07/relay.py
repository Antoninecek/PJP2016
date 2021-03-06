#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ukázka pár triků jak urychlit program
proc nektera jmena nebyla nalezena:
neexistuje záznam v competitors.json:
    Elisabeth Hohenwarter
    Nadya Mikryukova
    Juan Sancosmed
pravdepodobne preklep:
    [name <result.html> -> firstname, lastname <competitors.json>]
    Erik Skovgaard Knudsen -> Erik, Knudsen Skovgaard
    Lasse Brun Pedersen -> Lasse, Bruhn Pedersen (řešitelné)
    Jean Charles Lalevee -> Jean-Charles, Lalevee
    Keichi Tamaki -> Keiichi, Tamaki
jine:
    Miguel Ramo > "Miguel", "Angel Ramo Martin"
script ignoruje DSQ
    Israel DSQ (Gahl Cohn, Eran Lerner, Zohar Drori)
"""
import codecs
import inspect
import json
import re
from pprint import pprint
from bs4 import BeautifulSoup

HTML_RESULT = 'result.html'
JSON_COMPETITORS = 'competitors.json'


def name_hook(obj, dct={}):
    """
    Mutable typ jako defaultni hodnota může být nebezpečnej.
    pylint říká:
    Dangerous default value {} as argument
    Je to dirty trick ale občas se toho využívá.
    viz http://docs.python-guide.org/en/latest/writing/gotchas/
    Normálně by tato funkce měla něco vracet a kazdou navrácenou
    hodnotu pak json.load appendne do listu, ale pro rychlejsi hledání jmen
    použiju dict, tak proc ho negenerovat rovnou tady.
    """
    dct.update({obj["firstname"] + ' ' + obj["lastname"]: obj["id"]})
    lname = obj["lastname"].split(' ')
    if len(lname) == 2:
        dct.update({obj["firstname"] + ' ' + ' '.join(lname[::-1]): obj["id"]})


def relay():
    """
    extract data from html and json and concatenate them into new json file
    :return: json with result
    """

    def _bs4(html_file):
        # je-li libo BS4
        soup = BeautifulSoup(html_file, "lxml")
        return re.findall(
            r'(\d+)\) .+?(\d{0,2}:\d{0,2}:\d{0,2}) \(([\w ,]*)\)',
            str(soup.find('strong', text="Relay").parent.find_next_siblings('p')))

    def _iterate_lines(html_file):
        rec = []
        while 1:
            if html_file.__next__().strip() == '<p><strong>Relay</strong></p>':
                for _ in range(4):
                    rec += re.findall(
                        r'(\d+)\) .+?(\d{0,2}:\d{0,2}:\d{0,2}) \(([\w ,]*)\)'
                        , html_file.__next__().strip())
                break
        return rec

    # Load data from html
    with codecs.open(HTML_RESULT, 'r', encoding='utf-8') as html_file:
        records = _bs4(html_file)

    # Load data from jsonbobo
    with codecs.open(JSON_COMPETITORS, 'r', encoding='utf-8') as json_file:
        json.loads(re.sub(r'\\\'', '\'', json_file.read()), object_hook=name_hook)
    # získá dct z name_hook
    data = inspect.signature(name_hook).parameters['dct'].default
    # data = name_hook.__defaults__[0]
    # print([name for n in records for name in n[2].split(', ')
    #         if name in data])

    # parse to JSON
    with codecs.open("output.json", "w", encoding="utf-8") as fwrite:
        fwrite.write(
            json.dumps(
                [{"result": int(rec[0]), "time": rec[1], "id": int(data[name])}
                 for rec in records
                 for name in rec[2].split(', ')
                 if name in data]
                , sort_keys=True
                , indent=4
            ))

if __name__ == '__main__':
    relay()
