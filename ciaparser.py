#!/usr/bin/env python
import json
import os
from collections import Counter
import pycountry

import bs4

NUMERIC_PROPS = {
    'Labor force',
    'Population',
    'Area',
    'Crude oil - proved reserves',
    'Railways',
    'HIV/AIDS - people living with HIV/AIDS',
}
PERCENTAGE_PROPS = {'Land use': 'Area'}


def strip_brackets(value):
    p = value.find('(')
    if p > -1:
        value = value[:p].strip()
    return value


def parse_number(property_value):
    value = strip_brackets(property_value)
    value = value.replace(',', '')
    value = value.lower()
    multipliers = {'thousand': 3, 'million': 6, 'billion': 9, 'trillion': 12}
    words = [x.strip() for x in value.split()]
    words = [
        word for word in words if word and not word in ('approximately', 'km')
    ]
    if words[0] == 'na':
        return 0
    try:
        value = float(words[0])
    except ValueError:
        return 0
    for word in words[1:]:
        zeroes = multipliers.get(word, 0)
        value *= 10 ** zeroes
    return value


def make_dollars(property_value):
    return parse_number(property_value[1:])


def parse_country(html):
    res = {}
    soup = bs4.BeautifulSoup(html, 'html.parser')
    property_name = None
    for tr in soup.find_all('tr'):
        div_1 = tr.find('div', class_='category')
        if div_1:
            note = div_1.find('em')
            if note:
                if note.get_text().strip(' :') == 'note':
                    div_1 = None
        if div_1:
            anchor = div_1.find('a')
            if anchor:
                property_name = str(anchor.contents[0]).strip(' :')
                property_value = None
            else:
                span = div_1.find('span', class_='category_data')
                if span:
                    property_value = span.get_text().strip()
        else:
            div_2 = tr.find('div', class_='category_data')
            if div_2:
                if property_name:
                    property_value = div_2.get_text().strip()
        if property_name and property_value:
            if property_name == 'Area':
                property_value = property_value.replace('sq km', '').strip()
            if property_name == 'Crude oil - proved reserves':
                property_value = property_value.replace('bbl', '').strip()
            if property_value.startswith('$'):
                property_value = make_dollars(property_value)
            elif property_name in NUMERIC_PROPS:
                if property_value.strip().lower() == 'uninhabited':
                    property_value = 0
                else:
                    property_value = parse_number(property_value)
            elif property_name in PERCENTAGE_PROPS:
                property_value = property_value.strip(' %')
                property_value = parse_number(property_value)
            elif len(property_value) > 50:
                continue
            res[property_name] = property_value
            property_name = None
    for k, v in PERCENTAGE_PROPS.items():
        if k in res:
            if v in res:
                res[k] = res[v] * res[k]
            else:
                del res[k]
    return res


def parse_id_table(html):
    res = {}
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for li in soup.find_all('li', class_='category'):
        td_texts = [td.get_text().strip() for td in li.find_all('td')]
        res[td_texts[1].lower()] = td_texts[3].lower()
    return res


def main():
    with open('data/appendix-d.html', 'rb') as fin:
        id_table = parse_id_table(fin.read())

    counts = Counter()
    countries = {}
    for fn in os.listdir('data/geos'):
        if fn.endswith('.html'):
            cia_id = fn[:2]
            if cia_id in ('ee', 'oo', 'sk', 'um', 'xo', 'xq', 'xx', 'zh', 'zn'):
                # various oceans and other entities
                continue
            if cia_id == 'cc':  # huh?
                cia_id = 'uc'
            cc = id_table[cia_id]
            #print(cia_id, cc)
            if cc == '-':
                continue
            with open(os.path.join('data/geos', fn), 'rb') as fin:
                countries[cc] = parse_country(fin.read())
                for k in countries[cc]:
                    counts[k] += 1
    with open('data/cia_data.js', 'w') as fout:
        fout.write(json.dumps(countries, indent=2))

    print('Countries:', len(countries))
    for k, v in counts.most_common():
        print(k, 100 * v / len(countries))


if __name__ == '__main__':
    main()
