# fiis.py
from playwright.sync_api import sync_playwright

URL = "https://www.fundamentus.com.br/fii_resultado.php"

def get_fiis():
    resultados = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_selector("table", timeout=60000)  # a tabela dos FIIs não tem id

        rows = page.query_selector_all("table tbody tr")
        headers = [th.inner_text().strip() for th in page.query_selector_all("table thead th")]
        if headers:
            headers[0] = "Fii"

        for row in rows:
            cols = row.query_selector_all("td")
            if cols:
                resultados.append({headers[i]: cols[i].inner_text().strip() for i in range(len(cols))})

        browser.close()
    return resultados
