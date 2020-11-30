import requests
from bs4 import BeautifulSoup
import re
import json

def search_text(string):
    return re.search(r'>(.*?)<', string).group(1)

# GET request
res_get = requests.get('http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm')
if res_get.status_code == 200:
    print('GET Success!')
elif res_get.status_code == 404:
    print('Page Not Found')
res_get.encoding = 'utf-8'
soup = BeautifulSoup(res_get.text, 'html.parser')

# UFs array
ufs = []
select = soup.find('select', class_ = 'f1col')
for value in select.stripped_strings:
    ufs.append(value)

# POST request
print(' ')
print('Access UF Pages')
print(' ')
all_records = []
for index in range(len(ufs)):
    payload = {'UF': ufs[index]}
    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
    res_post = requests.post(url, data = payload)
    if res_post.status_code == 200:
        print(f'POST Success! UF: {ufs[index]}')
    elif res_post.status_code == 404:
        print(f'Page Not Accessed. UF: {ufs[index]}')
    res_post.encoding = 'utf-8'
    soup = BeautifulSoup(res_post.content, 'html.parser')

    # Information array
    records = soup.find_all('tr')
    count = 0
    for record in records:
        info = record.find_all('td')
        if info:
            if count != 0:
                phrase = str(info)
                phrase = phrase.split(',')
                all_records.append({
                    'uf': ufs[index],
                    'localidade': search_text(phrase[0]),
                    'faixa de cep': search_text(phrase[1]),
                    'situacao': search_text(phrase[2]),
                    'tipo de faixa': search_text(phrase[3]),
                    'id': count
                })
            count += 1

# Save JSON file
with open('records.json', 'w') as json_file:
    json.dump(all_records, json_file, indent = 3, ensure_ascii = False)