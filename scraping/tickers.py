import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def _get_tickers_from_url(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    tickers = []
    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if cols:
            ticker = cols[0].get_text(strip=True)
            if ticker:
                tickers.append(ticker)

    return sorted(set(tickers))


def get_all_tickers():
    """
    Retorna todos os tickers válidos do Fundamentus
    separados em AÇÕES e FIIs
    """
    return {
        "ACAO": _get_tickers_from_url(
            "https://www.fundamentus.com.br/resultado.php"
        ),
        "FII": _get_tickers_from_url(
            "https://www.fundamentus.com.br/fii_resultado.php"
        )
    }
