# rules.py — Cálculos e KPIs do sistema.

from storage import carregar_consultas

def volume_por_tipo(consultas=None):
    if consultas is None: consultas = carregar_consultas()
    c = {"SUS": 0, "Particular": 0, "Convênio": 0}
    for x in consultas:
        if x["tipo"] in c: c[x["tipo"]] += 1
    c["total"] = sum(c.values())
    return c

def receita_por_tipo(consultas=None):
    if consultas is None: consultas = carregar_consultas()
    r = {"SUS":{"total":0.0,"quantidade":0},
         "Particular":{"total":0.0,"quantidade":0},
         "Convênio":{"total":0.0,"quantidade":0}}
    for c in consultas:
        if c["status"] != "realizada": continue
        if c["tipo"] in r:
            r[c["tipo"]]["total"]      += float(c["valor"])
            r[c["tipo"]]["quantidade"] += 1
    for d in r.values():
        d["ticket_medio"] = round(d["total"]/d["quantidade"],2) if d["quantidade"] else 0.0
    tg = sum(d["total"]      for d in r.values())
    qg = sum(d["quantidade"] for d in r.values())
    r["geral"] = {"total": round(tg,2), "quantidade": qg,
                  "ticket_medio": round(tg/qg,2) if qg else 0.0}
    return r

def taxa_cancelamento_glosa(consultas=None):
    if consultas is None: consultas = carregar_consultas()
    total = len(consultas)
    real  = sum(1 for c in consultas if c["status"] == "realizada")
    canc  = sum(1 for c in consultas if c["status"] == "cancelada")
    glos  = sum(1 for c in consultas if c["status"] == "glosada")
    return {"total": total, "realizadas": real, "canceladas": canc, "glosadas": glos,
            "taxa_cancelamento": round(canc/total*100,1) if total else 0.0,
            "taxa_glosa":        round(glos/total*100,1) if total else 0.0}

def perdas_por_tipo(consultas=None):
    """
    Separa, para cada tipo (SUS, Particular, Convênio),
    quantas consultas foram canceladas e quantas foram glosadas.
    Necessário porque a tabela de gargalos do front-end exibe
    essas duas colunas separadamente.
    """
    if consultas is None: consultas = carregar_consultas()
    resultado = {
        "SUS":        {"canceladas": 0, "glosadas": 0},
        "Particular": {"canceladas": 0, "glosadas": 0},
        "Convênio":   {"canceladas": 0, "glosadas": 0},
    }
    for c in consultas:
        tipo = c["tipo"]
        if tipo not in resultado:
            continue
        if c["status"] == "cancelada":
            resultado[tipo]["canceladas"] += 1
        elif c["status"] == "glosada":
            resultado[tipo]["glosadas"] += 1
    return resultado

def saldo_por_mes(ano=None):
    consultas = carregar_consultas()
    if ano: consultas = [c for c in consultas if c["data"].startswith(str(ano))]
    saldo = {}
    for c in consultas:
        if c["status"] != "realizada": continue
        m = c["data"][:7]
        if m not in saldo: saldo[m] = {"receita": 0.0, "consultas": 0}
        saldo[m]["receita"]   += float(c["valor"])
        saldo[m]["consultas"] += 1
    for m in saldo: saldo[m]["receita"] = round(saldo[m]["receita"], 2)
    return dict(sorted(saldo.items()))

def resumo_geral():
    consultas = carregar_consultas()
    return {"volume":          volume_por_tipo(consultas),
            "receita":         receita_por_tipo(consultas),
            "cancelamento":    taxa_cancelamento_glosa(consultas),
            "perdas_por_tipo": perdas_por_tipo(consultas),
            "saldo_mes":       saldo_por_mes()}
