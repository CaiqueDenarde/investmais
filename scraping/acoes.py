import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.fundamentus.com.br"
URL_ACAO = f"{BASE_URL}/resultado.php"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": BASE_URL,
    "Connection": "keep-alive",
}

def get_acoes():
    session = requests.Session()
    session.headers.update(HEADERS)

    # 1️⃣ Visita a home (gera cookies válidos)
    home = session.get(BASE_URL, timeout=30)
    home.raise_for_status()

    # 2️⃣ Agora acessa a página de resultado
    resp = session.get(URL_ACAO, timeout=30)
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
