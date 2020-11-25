import requests
from bs4 import BeautifulSoup
import re
import json
# import urllib
# import urllib2

# def fill_str(string):
#     start = s.find(">") + len(">")
#     end = s.find("<")
#     substring = s[start:end]
#     return substring

# def find_between_r(s, first, last ):
#     # try:
#         start = s.rindex( first ) + len( first )
#         end = s.rindex( last, start )
#         return s[start:end]
#     # except ValueError:
#         # return ""

# res = requests.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select")
res = requests.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm")
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# all_posts = soup.find_all(class_ = "sbib_b")
# print(all_posts)
# contents = [str(x.text) for x in soup.find(class_ = "f1col").find_all("option")]

# Array UFs
ufs = []
select = soup.find("select", class_ = "f1col")
for value in select.stripped_strings:
    ufs.append(value)
# list_ufs = list(select.stripped_strings)
# print(ufs)
# print(list_ufs)
# print(soup.option)

# Dicionário
# dict_ufs = {i : ufs[i] for i in range(0, len(ufs))}
# print(dict_ufs)

# response = requests.post(url, data = post_params)
# soup = BeautifulSoup(response.text, 'html.parser')

# Requisição POST com um elemento do dicionário
all_records = []
for index in range(len(ufs)):
    payload = {"UF": ufs[index]}
    url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
    # page = requests.get(url)
    # json_data = {"value": dict_ufs[0]}
    r = requests.post(url, data = payload)
    # r_dict = r.json()
    # print(r)
    s = BeautifulSoup(r.content, "html.parser")
    # print(s)

    # links = s.find(class_ = "column2").find_all("a")

    # Array de informações
    # r.encoding = "utf-8"
    # s = BeautifulSoup(r.text, "html.parser")
    # # print(s)
    # records = s.find_all("div", class_ = "column2")
    records = s.find_all("tr")
    # print(records)
    count = 0
    for record in records:
        info = record.find_all("td")
        # print(record.find("tr").text)
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
                # print(info)
                # print(str(info))
            count += 1
        # "localidade"
        # "faixa de cep"
        # "Situação"
        # "Tipo de Faixa"
        # "id" = count
    # print(phrase)
    # str_prov = phrase[0]
    # a = re.search(r'>(.*?)<', phrase[0]).group(1)
    # find_between_r(str_prov, ">", "<")
# print(all_records)
# teste_string = str(links)
# teste_string = teste_string.split(",")
# href = re.search(r'"(.*?)"', teste_string[1]).group(1)
# print(href)


# Salvando arquivo JSON
with open('records.json', 'w') as json_file:
    json.dump(all_records, json_file, indent = 3, ensure_ascii = False)

# print(records[0])