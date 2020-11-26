import requests
from bs4 import BeautifulSoup
import re
import json

# GET request
res = requests.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm")
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# UFs array
ufs = []
select = soup.find("select", class_ = "f1col")
for value in select.stripped_strings:
    ufs.append(value)

# POST request
all_records = []
for index in range(len(ufs)):
    payload = {"UF": ufs[index]}
    url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
    r = requests.post(url, data = payload)
    r.encoding = "utf-8"
    s = BeautifulSoup(r.content, "html.parser")

    # Information array
    records = s.find_all("tr")
    count = 0
    for record in records:
        info = record.find_all("td")
        if info:
            if count != 0:
                phrase = str(info)
                phrase = phrase.split(",")
                all_records.append({
                    'uf': ufs[index],
                    'localidade': re.search(r'>(.*?)<', phrase[0]).group(1),
                    'faixa de cep': re.search(r'>(.*?)<', phrase[1]).group(1),
                    'situacao': re.search(r'>(.*?)<', phrase[2]).group(1),
                    'tipo de faixa': re.search(r'>(.*?)<', phrase[3]).group(1),
                    'id': count
                })
            count += 1

# Save JSON file
with open('records.json', 'w') as json_file:
    json.dump(all_records, json_file, indent = 3, ensure_ascii = False)