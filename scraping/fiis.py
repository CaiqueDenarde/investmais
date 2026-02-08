from playwright.sync_api import sync_playwright

URL_FII = "https://www.fundamentus.com.br/fii_resultado.php"

def get_fiis():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        context.route(
            "**/*",
            lambda route, request: route.abort()
            if request.resource_type in ["image", "font", "media"]
            else route.continue_()
        )

        page = context.new_page()
        page.goto(URL_FII, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_selector("table", timeout=120000)

        with open("debug_fiis.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        tabela = page.query_selector("table")
        headers = [th.inner_text().strip() for th in tabela.query_selector_all("thead th")]
        if headers:
            headers[0] = "Fii"

        dados = []
        for row in tabela.query_selector_all("tbody tr"):
            cols = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if len(cols) == len(headers):
                dados.append(dict(zip(headers, cols)))

        browser.close()
        return dados
