# services.py — Cadastrar, listar, buscar e atualizar registros.

from models import criar_paciente, criar_profissional, criar_consulta, criar_pagamento
from storage import (carregar_pacientes, salvar_pacientes,
                     carregar_profissionais, salvar_profissionais,
                     carregar_consultas, salvar_consultas,
                     carregar_pagamentos, salvar_pagamentos)

def _proximo_id(lista):
    return max((int(i["id"]) for i in lista), default=0) + 1

# ── Pacientes ──
def cadastrar_paciente(nome, data_nascimento, cpf, convenio, telefone):
    pacientes = carregar_pacientes()
    if any(p["cpf"] == cpf for p in pacientes):
        print(f"  CPF '{cpf}' já cadastrado.")
        return None
    novo = criar_paciente(_proximo_id(pacientes), nome, data_nascimento, cpf, convenio, telefone)
    pacientes.append(novo)
    salvar_pacientes(pacientes)
    print(f"  Paciente '{nome}' cadastrado com ID {novo['id']}.")
    return novo

def listar_pacientes(convenio=None):
    pacs = carregar_pacientes()
    return [p for p in pacs if p["convenio"] == convenio] if convenio else pacs

def buscar_paciente(termo):
    termo = str(termo).lower()
    return [p for p in carregar_pacientes()
            if termo in p["nome"].lower() or termo == str(p["id"])]

# ── Profissionais ──
def cadastrar_profissional(nome, especialidade, crm):
    profs = carregar_profissionais()
    if any(p["crm"] == crm for p in profs):
        print(f"  CRM '{crm}' já cadastrado.")
        return None
    novo = criar_profissional(_proximo_id(profs), nome, especialidade, crm)
    profs.append(novo)
    salvar_profissionais(profs)
    print(f"  Profissional '{nome}' cadastrado com ID {novo['id']}.")
    return novo

def listar_profissionais(especialidade=None):
    profs = carregar_profissionais()
    return [p for p in profs if p["especialidade"] == especialidade] if especialidade else profs

def buscar_profissional(termo):
    termo = str(termo).lower()
    return [p for p in carregar_profissionais()
            if termo in p["nome"].lower() or termo == str(p["id"])]

# ── Consultas ──
def cadastrar_consulta(paciente_id, profissional_id, data, tipo, valor,
                       status="realizada", procedimento=""):
    consultas = carregar_consultas()
    novo = criar_consulta(_proximo_id(consultas), paciente_id, profissional_id,
                          data, tipo, valor, status, procedimento)
    consultas.append(novo)
    salvar_consultas(consultas)
    print(f"  Consulta ID {novo['id']} — {tipo} | R$ {valor:.2f} | {status}.")
    return novo

def listar_consultas(tipo=None, status=None, mes=None, ano=None):
    cons = carregar_consultas()
    if tipo:   cons = [c for c in cons if c["tipo"] == tipo]
    if status: cons = [c for c in cons if c["status"] == status]
    if ano:    cons = [c for c in cons if c["data"].startswith(str(ano))]
    if mes:    cons = [c for c in cons if c["data"][5:7] == str(mes).zfill(2)]
    return cons

def buscar_consulta(termo):
    termo = str(termo).lower()
    return [c for c in carregar_consultas()
            if termo == str(c["id"]) or termo in c["tipo"].lower()
            or termo in c["status"].lower()]

def cancelar_consulta(consulta_id):
    consultas = carregar_consultas()
    for c in consultas:
        if int(c["id"]) == int(consulta_id):
            c["status"] = "cancelada"
            salvar_consultas(consultas)
            print(f"  Consulta ID {consulta_id} cancelada.")
            return True
    print(f"  Consulta ID {consulta_id} não encontrada.")
    return False

# ── Pagamentos ──
def cadastrar_pagamento(consulta_id, data_pagamento, valor_pago, forma):
    pags = carregar_pagamentos()
    novo = criar_pagamento(_proximo_id(pags), consulta_id, data_pagamento, valor_pago, forma)
    pags.append(novo)
    salvar_pagamentos(pags)
    print(f"  Pagamento ID {novo['id']} — R$ {valor_pago:.2f} via {forma}.")
    return novo

def listar_pagamentos(forma=None, mes=None, ano=None):
    pags = carregar_pagamentos()
    if forma: pags = [p for p in pags if p["forma"] == forma]
    if ano:   pags = [p for p in pags if p["data_pagamento"].startswith(str(ano))]
    if mes:   pags = [p for p in pags if p["data_pagamento"][5:7] == str(mes).zfill(2)]
    return pags
