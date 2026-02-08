# analyzer.py

def to_float(valor):
    if valor in (None, "N/A"):
        return None
    try:
        return float(
            valor.replace(".", "")
                 .replace(",", ".")
                 .replace("%", "")
                 .strip()
        )
    except Exception:
        return None


def analyze_asset(dados):
    """
    Decide automaticamente se é AÇÃO ou FII
    Retorna: BARATO | JUSTO | CARO
    """
    tipo = dados.get("Tipo")

    if tipo == "AÇÃO":
        return analyze_stock(dados)
    elif tipo == "FII":
        return analyze_fii(dados)

    return "INDEFINIDO"


def analyze_stock(dados):
    pl = to_float(dados.get("P/L"))
    pvp = to_float(dados.get("P/VP"))
    margem = to_float(dados.get("Marg. Líquida"))
    dy = to_float(dados.get("Div. Yield"))

    score = 0

    # P/L
    if pl is not None:
        if pl < 8:
            score += 1
        elif pl > 15:
            score -= 1

    # P/VP
    if pvp is not None:
        if pvp < 1:
            score += 1
        elif pvp > 2:
            score -= 1

    # Margem
    if margem is not None and margem > 15:
        score += 1

    # Dividend Yield
    if dy is not None and dy > 6:
        score += 1

    return classify_score(score, min_good=2, max_bad=-1)


def analyze_fii(dados):
    pvp = to_float(dados.get("P/VP"))
    dy = to_float(dados.get("Div. Yield"))

    score = 0

    # P/VP
    if pvp is not None:
        if pvp < 0.95:
            score += 1
        elif pvp > 1.10:
            score -= 1

    # Dividend Yield
    if dy is not None:
        if dy > 8:
            score += 1
        elif dy < 6:
            score -= 1

    return classify_score(score, min_good=1, max_bad=-1)


def classify_score(score, min_good, max_bad):
    if score >= min_good:
        return "BARATO"
    elif score <= max_bad:
        return "CARO"
    return "JUSTO"
