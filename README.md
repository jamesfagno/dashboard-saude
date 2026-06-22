# Dashboard para Gestão em Saúde

Sistema administrativo-financeiro para gestão de consultas médicas com suporte a SUS, Particular e Convênios. Desenvolvido em Python (back-end) com dashboard visual em HTML/CSS/JS (front-end).

**🔗 Demo ao vivo:** _adicione o link do Vercel após o deploy_

---

## Funcionalidades

- Login com controle de acesso por perfil (admin, gestor, operador)
- Cadastro de pacientes, profissionais, consultas e pagamentos
- Filtros por tipo de consulta, status e período
- KPIs financeiros: receita total, ticket médio, taxa de cancelamento e glosa
- Dashboard visual com gráficos de pizza e barras
- Dados baseados na Tabela SUS 2024 (SIGTAP)
- Gerenciamento de usuários com senhas em hash SHA-256

---

## Tecnologias

| Camada     | Tecnologia                        |
|------------|-----------------------------------|
| Back-end   | Python 3.x (sem bibliotecas externas) |
| Banco      | CSV (arquivos locais)             |
| Front-end  | HTML, CSS, JavaScript             |
| Gráficos   | Chart.js (via CDN)                |
| Deploy     | Vercel (front-end estático)       |

---

## Estrutura do projeto

```
Projeto/                        ← pasta com os arquivos baixados
├── setup.py                    ← roda uma vez para montar tudo
├── models.py                   ← estrutura dos dados
├── storage.py                  ← leitura e escrita dos CSVs
├── services.py                 ← cadastro, listagem e busca
├── rules.py                    ← cálculos e KPIs
├── dashboard.py                ← exibição no terminal e geração do JSON
├── main.py                     ← menu principal (ponto de entrada)
├── usuarios.py                 ← autenticação e gerenciamento de usuários
├── index.html                  ← tela do dashboard
├── style.css                   ← estilos
├── app.js                      ← lógica do front-end
├── dados.json                  ← dados de demonstração (usado pelo Vercel)
├── vercel.json                 ← configuração do deploy
├── .gitignore
└── README.md

dashboard_saude/                ← criado pelo setup.py
├── main.py ... usuarios.py     ← cópias dos arquivos Python
├── dados/
│   ├── pacientes.csv           (120 pacientes)
│   ├── profissionais.csv       (15 profissionais)
│   ├── consultas.csv           (168 consultas — Jan a Ago/2024)
│   ├── pagamentos.csv          (133 pagamentos)
│   ├── procedimentos.csv       (Tabela SUS 2024)
│   └── usuarios.csv            (usuários do sistema)
└── frontend/
    ├── index.html
    ├── style.css
    ├── app.js
    └── dados.json              ← gerado pela opção 6 do menu
```

---

## Como instalar e rodar localmente

### Pré-requisito

Ter o **Python 3** instalado. Verifique no terminal:

```bash
python --version
```

Se não tiver, baixe em: https://www.python.org/downloads/

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Rode o setup

```bash
python setup.py
```

Isso cria a pasta `dashboard_saude/` com todas as subpastas, CSVs com dados reais e cópias dos arquivos Python.

### 3. Acesse o sistema

```bash
cd dashboard_saude
python main.py
```

| Login      | Senha       | Perfil        |
|------------|-------------|---------------|
| admin      | admin123    | Administrador |
| gestor1    | gestor123   | Gestor        |
| recepcao   | recepcao1   | Operador      |

> ⚠️ Troque as senhas após o primeiro acesso (menu 7 → opção 6).

### 4. Gerar o JSON para o front-end

Dentro do sistema, escolha a **opção 6** no menu principal. Isso gera o arquivo `dashboard_saude/frontend/dados.json`.

### 5. Abrir o dashboard no navegador

```bash
cd dashboard_saude/frontend
python -m http.server 8000
```

Acesse: **http://localhost:8000**

---

## Deploy no Vercel (front-end)

O Vercel serve apenas o front-end estático. O arquivo `dados.json` já está incluído no repositório com dados reais de demonstração.

### Passo a passo

**1. Crie uma conta no Vercel**

Acesse https://vercel.com e entre com sua conta do GitHub.

**2. Importe o repositório**

- Clique em **Add New → Project**
- Selecione o repositório do projeto
- Clique em **Deploy** (sem alterar nenhuma configuração — o `vercel.json` já cuida de tudo)

**3. Pronto**

O Vercel vai gerar uma URL pública como:
```
https://dashboard-saude-omega.vercel.app/
```

> O `dados.json` incluído no repositório garante que o dashboard funcione no Vercel com dados reais de demonstração sem precisar do Python.

---

## Como subir para o GitHub

### Primeira vez

```bash
# Dentro da pasta Projeto/
git init
git add .
git commit -m "primeiro commit — dashboard gestão em saúde"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

### Atualizações futuras

```bash
git add .
git commit -m "descrição da alteração"
git push
```

---

## Base de dados de demonstração

| Arquivo             | Registros                          |
|---------------------|------------------------------------|
| pacientes.csv       | 120 pacientes                      |
| profissionais.csv   | 15 profissionais / 15 especialidades |
| consultas.csv       | 168 consultas (Jan–Ago 2024)       |
| pagamentos.csv      | 133 pagamentos                     |
| procedimentos.csv   | 19 procedimentos — Tabela SUS 2024 |

**Receita total demonstração:** R$ 27.923,36  
**Ticket médio geral:** R$ 209,95  
**Taxa de cancelamento:** 11,3%

---

## Perfis de acesso

| Perfil    | Permissões                                              |
|-----------|---------------------------------------------------------|
| admin     | Acesso total, incluindo gerenciamento de usuários       |
| gestor    | Acesso a consultas, pagamentos e dashboard              |
| operador  | Cadastro de pacientes e consultas, sem acesso ao dashboard financeiro |

---

## Licença

Projeto acadêmico desenvolvido para fins de aprendizado.
