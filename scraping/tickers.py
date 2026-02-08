# tickers.py
import requests
from bs4 import BeautifulSoup
import os

# ======== Headers ========
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.fundamentus.com.br/"
}

# ======== URLs e payloads ========
URL_ACAO = "https://www.fundamentus.com.br/resultado.php"
URL_FII = "https://www.fundamentus.com.br/fii_resultado.php"

PAYLOAD_ACAO = {
    "pl_min": "", "pl_max": "", "pvp_min": "", "pvp_max": "",
    "psr_min": "", "psr_max": "", "divy_min": "", "divy_max": "",
    "pativ_min": "", "pativ_max": "", "pcapgiro_min": "", "pcapgiro_max": "",
    "pebit_min": "", "pebit_max": "", "fgrau_min": "", "fgrau_max": "",
    "cresc_rec_min": "", "cresc_rec_max": ""
}

PAYLOAD_FII = {
    "dividendo_min": "", "dividendo_max": "", "pl_min": "", "pl_max": "",
    "pvp_min": "", "pvp_max": "", "dy_min": "", "dy_max": ""
}

# ======== Função interna para buscar tickers ========
def _get_tickers_from_url(url: str, payload: dict, debug_file: str):
    r = requests.post(url, headers=HEADERS, data=payload, timeout=20)
    r.encoding = "ISO-8859-1"
    r.raise_for_status()

    # ======== Salva HTML de debug ========
    """""
    with open(debug_file, "w", encoding="ISO-8859-1") as f:
        f.write(r.text)
    print(f"HTML salvo para debug em {os.path.abspath(debug_file)}")
    """
    soup = BeautifulSoup(r.text, "html.parser")
    tickers = []

    table = soup.find("table")
    if not table:
        print("⚠️ Nenhuma tabela encontrada na página.")
        return []

    tbody = table.find("tbody")
    if not tbody:
        print("⚠️ Nenhum tbody encontrado na tabela.")
        return []

    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if cols:
            ticker = cols[0].get_text(strip=True)
            if ticker:
                tickers.append(ticker)

    return sorted(set(tickers))

# ======== Função pública ========
def get_all_tickers():
    return {
        "ACAO": _get_tickers_from_url(URL_ACAO, PAYLOAD_ACAO, "debug_tickers_acoes.html"),
        "FII": _get_tickers_from_url(URL_FII, PAYLOAD_FII, "debug_tickers_fiis.html")
    }

# ======== Teste rápido ========
if __name__ == "__main__":
    tickers = get_all_tickers()
    print("ACAO:", tickers["ACAO"][:10], "...")
    print("FII:", tickers["FII"][:10], "...")
