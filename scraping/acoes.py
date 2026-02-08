import requests
from bs4 import BeautifulSoup

URL_ACAO = "https://www.fundamentus.com.br/resultado.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}

def get_acoes():
    resp = requests.get(URL_ACAO, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    table = soup.find("table")
    if not table:
        raise Exception("Tabela de ações não encontrada")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    if headers:
        headers[0] = "Ação"

    dados = []
    for row in table.find("tbody").find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) == len(headers):
            dados.append(dict(zip(headers, cols)))

    return dados
