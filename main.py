import requests
from bs4 import BeautifulSoup
# import urllib
# import urllib2

# res = requests.get("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select")
res = requests.get("http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm")
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, "html.parser")

# all_posts = soup.find_all(class_ = "sbib_b")
# print(all_posts)
# contents = [str(x.text) for x in soup.find(class_ = "f1col").find_all("option")]

# Array de UF
ufs = []
select = soup.find("select", class_ = "f1col")
for value in select.stripped_strings:
    ufs.append(value)
# list_ufs = list(select.stripped_strings)
# print(ufs)
# print(list_ufs)
# print(soup.option)

# Dicionário
dict_ufs = {i : ufs[i] for i in range(0, len(ufs))}
# print(dict_ufs)

# response = requests.post(url, data = post_params)
# soup = BeautifulSoup(response.text, 'html.parser')

# Requisição POST com um elemento do dicionário
payload = {"UF": "AC"}
url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
# page = requests.get(url)
# json_data = {"value": dict_ufs[0]}
r = requests.post(url, data = payload)
# r_dict = r.json()
# print(r)
s = BeautifulSoup(r.text, "html.parser")
# print(s)

# Array de informações
# r.encoding = "utf-8"
# s = BeautifulSoup(r.text, "html.parser")
# # print(s)
records = s.find_all(class_ = "tmptabela")
# print(records)

all_records = []
count = 0
for record in records:
    # info = record.find(class_ = "node")
    # print(record.find("td").text)
    count += 1
#     print(count)
    # "localidade"
    # "faixa de cep"
    # "id" = count



# print(records[0])