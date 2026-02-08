from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": "https://www.fundamentus.com.br/"
}

URL_ACOES = "https://www.fundamentus.com.br/resultado.php"

def get_acoes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(extra_http_headers=HEADERS)

        page.goto(URL_ACOES, timeout=60000)

        # espera a table FINAL renderizada via JS
        page.wait_for_selector(
            "xpath=/html/body/div[1]/div[2]/table",
            timeout=60000
        )

        # debug (fundamental no GitHub Actions)
        with open("debug_acoes.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        table = page.query_selector(
            "xpath=/html/body/div[1]/div[2]/table"
        )

        headers = [
            th.inner_text().strip()
            for th in table.query_selector_all("thead th")
        ]

        if headers:
            headers[0] = "Ação"

        dados = []

        for row in table.query_selector_all("tbody tr"):
            cols = [
                td.inner_text().strip()
                for td in row.query_selector_all("td")
            ]
            if cols:
                dados.append(dict(zip(headers, cols)))

        browser.close()
        return dados
