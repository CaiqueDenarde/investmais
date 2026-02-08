import requests
from bs4 import BeautifulSoup

URL = "https://www.fundamentus.com.br/fii_resultado.php"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_fiis():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    r.encoding = "ISO-8859-1"

    soup = BeautifulSoup(r.text, "html.parser")

    # pega a primeira tabela do body
    table = soup.find("table")
    if not table:
        raise Exception("Não encontrei nenhuma tabela na página de FIIs")

    # cabeçalhos
    thead = table.find("thead")
    if not thead:
        raise Exception("Não encontrei o thead na tabela de FIIs")

    colunas = [th.get_text(strip=True) for th in thead.find_all("th")]

    # renomeia a primeira coluna para 'Fii'
    if colunas:
        colunas[0] = "Fii"

    # linhas
    tbody = table.find("tbody")
    if not tbody:
        raise Exception("Não encontrei tbody na tabela de FIIs")

    dados = []
    for tr in tbody.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            dados.append(dict(zip(colunas, cols)))

    return dados
