import json


PROPERTIES = {'Area', 'Population', 'GDP (official exchange rate)', 'HIV/AIDS - people living with HIV/AIDS',
              'Crude oil - proved reserves', 'Exports', 'Land use', 'Labor force'}


def main():
  with open('data/cia_data.js') as fin:
    cia_data = json.load(fin)

  country_name_to_code = {'united states': 'us',
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
                          'kosovo': 'xk'}

  data = {cc: {kk: vv for kk, vv in rec.items() if kk in PROPERTIES} for cc, rec in cia_data.items()}
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

  with open('data/country_data.js', 'w') as fout:
    json.dump(data, fout, indent=2)

if __name__ == '__main__':
  main()





