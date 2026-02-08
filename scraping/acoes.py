# acoes.py
from playwright.sync_api import sync_playwright

URL = "https://www.fundamentus.com.br/resultado.php"

def get_acoes():
    resultados = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless para rodar no GitHub
        page = browser.new_page()
        page.goto(URL, timeout=60000)  # espera até 60s para carregar
        page.wait_for_selector("table#resultado", timeout=60000)  # espera a tabela

        # coleta os dados
        rows = page.query_selector_all("table#resultado tbody tr")
        headers = [th.inner_text().strip() for th in page.query_selector_all("table#resultado thead th")]
        if headers:
            headers[0] = "Ação"

        for row in rows:
            cols = row.query_selector_all("td")
            if cols:
                resultados.append({headers[i]: cols[i].inner_text().strip() for i in range(len(cols))})

        browser.close()
    return resultados
