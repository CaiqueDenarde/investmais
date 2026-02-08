# acoes.py
import requests
from bs4 import BeautifulSoup
import time
import os

# ======== Headers completos ========
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

# ======== URL do Fundamentus para ações ========
URL_ACAO = "https://www.fundamentus.com.br/resultado.php"

# ======== Payload vazio para POST ========
PAYLOAD_ACAO = {
    "pl_min": "",
    "pl_max": "",
    "pvp_min": "",
    "pvp_max": "",
    "psr_min": "",
    "psr_max": "",
    "divy_min": "",
    "divy_max": "",
    "pativ_min": "",
    "pativ_max": "",
    "pcapgiro_min": "",
    "pcapgiro_max": "",
    "pebit_min": "",
    "pebit_max": "",
    "fgrau_min": "",
    "fgrau_max": "",
    "cresc_rec_min": "",
    "cresc_rec_max": "",
}

def get_acoes(retries=3, delay=5):
    last_exception = None

    for attempt in range(retries):
        try:
            print(f"Buscando ações... tentativa {attempt+1}")
            r = requests.post(URL_ACAO, headers=HEADERS, data=PAYLOAD_ACAO, timeout=20)
            r.encoding = "ISO-8859-1"

            # Salva HTML para debug
            """"
            debug_file = os.path.join(os.path.dirname(__file__), "debug_acoes.html")
            with open(debug_file, "w", encoding="ISO-8859-1") as f:
                f.write(r.text)
            print(f"HTML salvo em {debug_file}")
            """
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find("table", {"id": "resultado"})
            if table is None:
                print("⚠️ Tabela com id='resultado' não encontrada.")
                return []

            thead = table.find("thead")
            tbody = table.find("tbody")
            if thead is None or tbody is None:
                print("⚠️ Estrutura da tabela incompleta (thead/tbody).")
                return []

            colunas = [th.get_text(strip=True) for th in thead.find_all("th")]
            if colunas:
                colunas[0] = "Ação"

            dados = []
            for tr in tbody.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    dados.append(dict(zip(colunas, cols)))

            print(f"Quantidade de Ações Encontradas: {len(dados)}")
            return dados

        except Exception as e:
            print(f"Tentativa {attempt+1}/{retries} falhou: {e}")
            last_exception = e
            time.sleep(delay)

    print("❌ Falha ao buscar ações após várias tentativas.")
    raise last_exception


if __name__ == "__main__":
    acoes = get_acoes()
    if acoes:
        print("Exemplo de ações:", acoes[:5])
    else:
        print("Nenhum dado de ações foi retornado.")
