import requests
from bs4 import BeautifulSoup

URL = "https://www.fundamentus.com.br/resultado.php"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_acoes():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    r.encoding = "ISO-8859-1"

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "resultado"})  # tabela principal

    # pega os cabeçalhos e renomeia a primeira coluna
    colunas = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
    if colunas:
        colunas[0] = "Ação"  # renomeia a primeira coluna

    linhas = table.find("tbody").find_all("tr")

    dados = []
    for tr in linhas:
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            dados.append(dict(zip(colunas, cols)))

    return dados
