import os
import json
from .acoes import get_acoes
from .fiis import get_fiis
from .analyzer import analyze_asset

# ==========================
# PASTAS
# ==========================
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do projeto
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ==========================
# COLETA ATIVOS
# ==========================
acoes = get_acoes()
fiis = get_fiis()

print(f"Quantidade de Ações Encontradas: {len(acoes)}")
print(f"Quantidade de Fiis Encontrados: {len(fiis)}\n")

# ==========================
# SALVA JSON ORIGINAIS
# ==========================
acoes_file = os.path.join(DATA_DIR, "acoes.json")
fiis_file = os.path.join(DATA_DIR, "fiis.json")

with open(acoes_file, "w", encoding="utf-8") as f:
    json.dump(acoes, f, ensure_ascii=False, indent=2)
print(f"[INFO] Arquivo salvo: {acoes_file}")

with open(fiis_file, "w", encoding="utf-8") as f:
    json.dump(fiis, f, ensure_ascii=False, indent=2)
print(f"[INFO] Arquivo salvo: {fiis_file}")


# ==========================
# FUNÇÃO AUXILIAR PARA NOMES DE ARQUIVO
# ==========================
def tipo_para_arquivo(tipo):
    mapping = {"AÇÃO": "acoes","FII": "fiis"}
    return mapping.get(tipo.upper(), tipo.lower())

# ==========================
# FUNÇÃO PARA ANALISAR E SALVAR
# ==========================
def analisar_e_salvar(ativos, tipo):
    resultados = []
    for ativo in ativos:
        ativo["Tipo"] = tipo
        ativo["Avaliacao"] = analyze_asset(ativo)
        resultados.append(ativo)

    output_file = os.path.join(PUBLIC_DIR, f"{tipo_para_arquivo(tipo)}_avaliados.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"[INFO] {tipo.upper()} analisados → arquivo salvo: {output_file}")
    return resultados

# ==========================
# ANALISA ATIVOS
# ==========================
acoes_analisadas = analisar_e_salvar(acoes, "AÇÃO")
fiis_analisados = analisar_e_salvar(fiis, "FII")



# ==========================
# RESUMO FINAL
# ==========================
print(f"\nAções Analisadas: {len(acoes_analisadas)}")
print(f"Fiis Analisados: {len(fiis_analisados)}\n")

print(f"Ações Classificadas: {len(acoes_analisadas)}")
print(f"Fiis Classificados: {len(fiis_analisados)}")
