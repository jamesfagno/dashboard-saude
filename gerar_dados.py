# api/_dados.py — Versão enxuta de storage.py + rules.py para a função
# serverless. Só leitura (a API pública não cadastra nada), lendo os CSVs
# de /dados na raiz do repositório.
#
# Mantido separado de storage.py/rules.py (usados pelo sistema de terminal
# em dashboard_saude/) para não acoplar o deploy web ao fluxo de CRUD local.

import os
import csv

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_CONSULTAS = os.path.join(_BASE, "dados", "consultas.csv")


def carregar_consultas():
    if not os.path.exists(ARQUIVO_CONSULTAS):
        return []
    with open(ARQUIVO_CONSULTAS, "r", encoding="utf-8") as f:
        registros = list(csv.DictReader(f))
    for r in registros:
        try:
            r["id"] = int(r["id"])
            r["paciente_id"] = int(r["paciente_id"])
            r["profissional_id"] = int(r["profissional_id"])
            r["valor"] = float(r["valor"])
        except (ValueError, KeyError):
            pass
    return registros


def volume_por_tipo(consultas):
    c = {"SUS": 0, "Particular": 0, "Convênio": 0}
    for x in consultas:
        if x["tipo"] in c:
            c[x["tipo"]] += 1
    c["total"] = sum(c.values())
    return c


def receita_por_tipo(consultas):
    r = {"SUS": {"total": 0.0, "quantidade": 0},
         "Particular": {"total": 0.0, "quantidade": 0},
         "Convênio": {"total": 0.0, "quantidade": 0}}
    for c in consultas:
        if c["status"] != "realizada":
            continue
        if c["tipo"] in r:
            r[c["tipo"]]["total"] += float(c["valor"])
            r[c["tipo"]]["quantidade"] += 1
    for d in r.values():
        d["ticket_medio"] = round(d["total"] / d["quantidade"], 2) if d["quantidade"] else 0.0
    tg = sum(d["total"] for d in r.values())
    qg = sum(d["quantidade"] for d in r.values())
    r["geral"] = {"total": round(tg, 2), "quantidade": qg,
                  "ticket_medio": round(tg / qg, 2) if qg else 0.0}
    return r


def taxa_cancelamento_glosa(consultas):
    total = len(consultas)
    real = sum(1 for c in consultas if c["status"] == "realizada")
    canc = sum(1 for c in consultas if c["status"] == "cancelada")
    glos = sum(1 for c in consultas if c["status"] == "glosada")
    return {"total": total, "realizadas": real, "canceladas": canc, "glosadas": glos,
            "taxa_cancelamento": round(canc / total * 100, 1) if total else 0.0,
            "taxa_glosa": round(glos / total * 100, 1) if total else 0.0}


def saldo_por_mes():
    consultas = carregar_consultas()
    saldo = {}
    for c in consultas:
        if c["status"] != "realizada":
            continue
        m = c["data"][:7]
        if m not in saldo:
            saldo[m] = {"receita": 0.0, "consultas": 0}
        saldo[m]["receita"] += float(c["valor"])
        saldo[m]["consultas"] += 1
    for m in saldo:
        saldo[m]["receita"] = round(saldo[m]["receita"], 2)
    return dict(sorted(saldo.items()))


def resumo_geral():
    consultas = carregar_consultas()
    return {"volume": volume_por_tipo(consultas),
            "receita": receita_por_tipo(consultas),
            "cancelamento": taxa_cancelamento_glosa(consultas),
            "saldo_mes": saldo_por_mes()}
