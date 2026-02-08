import os
import json
from analyzer import analyze_asset

# ==========================
# PASTA PUBLIC NA RAIZ
# ==========================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta atual do script
PUBLIC_DIR = os.path.join(ROOT_DIR, "..", "public")    # pasta public na raiz do projeto
os.makedirs(PUBLIC_DIR, exist_ok=True)

# ==========================
# FUNÇÃO PARA NOME LIMPO DE ARQUIVO
# ==========================
def tipo_para_arquivo(tipo):
    mapping = {"AÇÃO": "acoes","FIIS": "fiis"}
    return mapping.get(tipo.lower(), tipo.lower())

# ==========================
# ARQUIVOS DE ENTRADA
# ==========================
input_files = {
    "acoes": "data/acoes.json",
    "fiis": "data/fiis.json"
}

# ==========================
# PROCESSA CADA TIPO
# ==========================
for tipo, path in input_files.items():
    if not os.path.exists(path):
        print(f"Arquivo {path} não encontrado, pulando...")
        continue

    with open(path, "r", encoding="utf-8") as f:
        ativos = json.load(f)

    resultados = []

    for ativo in ativos:
        # Determina automaticamente o tipo para o analyzer
        if tipo.lower() == "acoes":
            ativo["Tipo"] = "AÇÃO"
        else:
            ativo["Tipo"] = "FII"

        # Analisa ativo
        avaliacao = analyze_asset(ativo)
        ativo["Avaliacao"] = avaliacao
        resultados.append(ativo)

    # Salva resultado em public na raiz
    output_file = os.path.join(PUBLIC_DIR, f"{tipo_para_arquivo(tipo)}_avaliados.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"{tipo.upper()} → {len(resultados)} ativos analisados → {output_file}")
