# dashboard.py — Exibe KPIs no terminal e gera dados.json para o front-end.

import csv
import hashlib
import json
import os
from rules import resumo_geral

_BASE        = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(_BASE, "dados.json")
USUARIOS_CSV = os.path.join(_BASE, "dados", "usuarios.csv")

def _linha(c="─", n=50):
    print(c * n)

def exibir_dashboard():
    dados = resumo_geral()
    vol   = dados["volume"]
    rec   = dados["receita"]
    canc  = dados["cancelamento"]
    saldo = dados["saldo_mes"]

    print()
    _linha("═")
    print("       DASHBOARD — GESTÃO EM SAÚDE")
    _linha("═")

    print("\n  VOLUME DE CONSULTAS")
    _linha()
    print(f"  {'Total geral':<25} {vol['total']:>6} consultas")
    print(f"  {'SUS':<25} {vol['SUS']:>6} consultas")
    print(f"  {'Particular':<25} {vol['Particular']:>6} consultas")
    print(f"  {'Convênio':<25} {vol['Convênio']:>6} consultas")

    print("\n  RECEITA FINANCEIRA  (somente realizadas)")
    _linha()
    print(f"  {'Receita total':<25} R$ {rec['geral']['total']:>10.2f}")
    print(f"  {'Ticket médio geral':<25} R$ {rec['geral']['ticket_medio']:>10.2f}")
    print()
    print(f"  {'Tipo':<14} {'Receita':>12}  {'Qtd':>5}  {'Ticket médio':>13}")
    _linha("-")
    for tipo in ["SUS", "Particular", "Convênio"]:
        d = rec[tipo]
        print(f"  {tipo:<14} R$ {d['total']:>9.2f}  {d['quantidade']:>5}"
              f"  R$ {d['ticket_medio']:>10.2f}")

    print("\n  CANCELAMENTOS E GLOSAS")
    _linha()
    pct_real = round(100 - canc['taxa_cancelamento'] - canc['taxa_glosa'], 1)
    print(f"  {'Realizadas':<25} {canc['realizadas']:>5}  ({pct_real}%)")
    print(f"  {'Canceladas':<25} {canc['canceladas']:>5}  ({canc['taxa_cancelamento']}%)")
    print(f"  {'Glosadas':<25} {canc['glosadas']:>5}  ({canc['taxa_glosa']}%)")

    print("\n  SALDO POR MÊS")
    _linha()
    if saldo:
        maior = max(d["receita"] for d in saldo.values()) or 1
        for mes, d in saldo.items():
            barra = "█" * int(d["receita"] / maior * 20)
            print(f"  {mes}   R$ {d['receita']:>9.2f}  {barra}")
    else:
        print("  Nenhum dado encontrado.")

    print()
    _linha("═")
    print()

def _ler_usuarios():
    """Lê usuarios.csv e retorna lista com login, nome, perfil e senha_hash."""
    usuarios = []
    if not os.path.exists(USUARIOS_CSV):
        return usuarios
    with open(USUARIOS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            usuarios.append({
                "login":      row["login"],
                "nome":       row["nome"],
                "perfil":     row["perfil"],
                "senha_hash": row["senha_hash"],
            })
    return usuarios

def gerar_json():
    """Gera dados.json com KPIs + lista de usuários (hashes) para o front-end."""
    try:
        payload = resumo_geral()
        payload["usuarios"] = _ler_usuarios()

        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"  Arquivo gerado: {ARQUIVO_JSON}")
        print(f"  Usuários incluídos: {len(payload['usuarios'])}")
    except Exception as e:
        print(f"  Erro ao gerar JSON: {e}")

def exibir_tabela_consultas(consultas):
    if not consultas:
        print("  Nenhuma consulta encontrada.")
        return
    print()
    print(f"  {'ID':>4}  {'Data':<12}  {'Tipo':<12}  {'Valor':>10}  {'Status':<12}")
    print("  " + "─" * 56)
    for c in consultas:
        print(f"  {c['id']:>4}  {c['data']:<12}  {c['tipo']:<12}"
              f"  R$ {float(c['valor']):>7.2f}  {c['status']:<12}")
    print("  " + "─" * 56)
    print(f"  Total: {len(consultas)} registro(s)\n")

def exibir_tabela_pacientes(pacientes):
    if not pacientes:
        print("  Nenhum paciente encontrado.")
        return
    print()
    print(f"  {'ID':>4}  {'Nome':<26}  {'Convênio':<14}  {'Telefone'}")
    print("  " + "─" * 60)
    for p in pacientes:
        print(f"  {p['id']:>4}  {p['nome']:<26}  {p['convenio']:<14}  {p['telefone']}")
    print("  " + "─" * 60)
    print(f"  Total: {len(pacientes)} registro(s)\n")
