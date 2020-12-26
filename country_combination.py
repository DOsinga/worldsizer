import json

import pycountry

PROPERTIES = {
    'Area',
    'Population',
    'GDP (official exchange rate)',
    'HIV/AIDS - people living with HIV/AIDS',
    'Crude oil - proved reserves',
    'Exports',
    'Land use',
    'Labor force',
}


def main():
    with open('data/cia_data.js') as fin:
        cia_data = json.load(fin)

    country_name_to_code = {
        'united states': 'us',
        'soviet union': 'ru',
        'great britain': 'gb',
        'east germany': 'de',
        'czechoslovakia': 'cz',
        'yugoslavia': 'rs',
        'north korea': 'kp',
        'south korea': 'kr',
        'iran': 'ir',
        'serbia and montenegro': 'rs',
        'syria': 'sy',
        'vietnam': 'vn',
        'venezuela': 've',
        'taiwan': 'tw',
        'tanzania': 'tz',
        'macedonia': 'mk',
        'virgin islands': 'vi',
        'kosovo': 'xk',
    }

    def ensure_float(v):
        try:
            return float(v)
        except ValueError:
            return 0

    data = {
        cc: {kk: ensure_float(vv) for kk, vv in rec.items() if kk in PROPERTIES}
        for cc, rec in cia_data.items()
    }
    with open('data/country_info.json') as fin:
        for cc in json.load(fin):
            key = cc['alpha-2'].lower()
            if key in data:
                data[key]['name'] = cc['name']
                country_name_to_code[cc['name'].lower()] = key
            else:
                print(key)

    for key in data:
        data[key]['medals'] = 0.1

    with open('data/medals.txt', encoding='utf8') as fin:
        for line in fin:
            _, country_name, count = line.strip().split('\t')
            key = country_name_to_code.get(country_name.lower())
            if key:
                data[key]['medals'] += int(count)
            else:
                print(country_name)

    with open('data/owid-covid-latest.json') as fin:
        IGNORE = {'nan', 'OWID_KOS', 'OWID_WRL'}
        covid = json.load(fin)
        three_to_two = {c.alpha_3: c.alpha_2 for c in pycountry.countries}
        covid = {three_to_two[k]: v for k, v in covid.items() if k not in IGNORE}

    for cc in data:
        cc_upper = cc.upper()
        if cc_upper not in covid:
            print('**', cc_upper)
            data[cc]['covid_cases'] = 1
            data[cc]['covid_deaths'] = 1
        else:
            data[cc]['covid_cases'] = covid[cc_upper]['total_cases']
            data[cc]['covid_deaths'] = covid[cc_upper]['total_deaths']

    with open('data/country_data.js', 'w') as fout:
        fout.write('COUNTRY_DATA = ' + json.dumps(data, indent=2))



if __name__ == '__main__':
    main()
