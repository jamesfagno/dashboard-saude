# Dashboard — Gestão em Saúde

Sistema administrativo-financeiro para clínicas, com back-end em Python (terminal) e dashboard visual no navegador.

## 🔗 Demo ao vivo

> [dashboard-saude.vercel.app](https://dashboard-saude-phi.vercel.app)

**Credenciais de acesso:**

| Login | Senha | Perfil |
|---|---|---|
| admin | admin123 | Administrador |
| gestor1 | gestor123 | Gestor |
| recepcao | recepcao1 | Operador |

---

## 📋 Funcionalidades

- Gestão de consultas SUS, Particular e Convênio
- KPIs: receita total, ticket médio, taxa de cancelamento e glosa
- Gráficos de volume por tipo e receita por mês
- Análise de gargalos com separação de canceladas e glosadas
- Filtros por tipo de atendimento e mês
- Login com autenticação SHA-256 (sem servidor — funciona 100% estático)
- Gerenciamento de usuários com 3 perfis: admin, gestor, operador

---

## 🗂️ Estrutura do projeto

```
dashboard-saude/
├── index.html          ← Dashboard visual (front-end)
├── style.css           ← Estilos
├── app.js              ← Lógica do front-end + autenticação
├── dados.json          ← Snapshot de demonstração (servido pelo Vercel)
├── vercel.json         ← Configuração de deploy
│
├── main.py             ← Menu principal do sistema de terminal
├── models.py           ← Estrutura dos dicionários de dados
├── storage.py          ← Leitura/escrita dos CSVs
├── services.py         ← CRUD completo
├── rules.py            ← KPIs e cálculos
├── dashboard.py        ← Exibição terminal + exporta dados.json
├── usuarios.py         ← Autenticação e gerenciamento de usuários
├── setup.py            ← Cria a estrutura local na primeira execução
├── gerar_dados.py      ← Gera 10.000 registros fictícios para testes
├── requirements.txt
│
└── dados/              ← CSVs locais (ignorados pelo git)
    ├── consultas.csv
    ├── pacientes.csv
    ├── pagamentos.csv
    ├── profissionais.csv
    ├── procedimentos.csv
    └── usuarios.csv
```

---

## 🚀 Como rodar localmente

**Pré-requisito:** Python 3.8 ou superior instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/dashboard-saude.git
cd dashboard-saude

# 2. Crie a estrutura de dados local
python setup.py

# 3. Gere os dados fictícios de teste (10.000 consultas)
python gerar_dados.py

# 4. Rode o sistema
python main.py
# login: admin | senha: admin123

# 5. No menu, escolha a opção 6 para exportar o dados.json
# 6. Abra o dashboard no navegador
python -m http.server 8000
# Acesse: http://localhost:8000
```

---

## 🌐 Deploy no Vercel

```bash
# Primeira vez
git init
git add .
git commit -m "primeiro commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/dashboard-saude.git
git push -u origin main
# → No Vercel: Add New Project → importar repositório → Deploy

# Após atualizações
git add .
git commit -m "descrição da mudança"
git push origin main
# → Vercel faz deploy automático
```

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3 puro (sem frameworks) |
| Banco de dados | Arquivos CSV |
| Front-end | HTML + CSS + JavaScript |
| Gráficos | Chart.js (CDN) |
| Autenticação | SHA-256 via Web Crypto API (nativa do browser) |
| Deploy | Vercel (estático) |
| Versionamento | GitHub |

---

## 👤 Autor

Desenvolvido por **James Fagno** como projeto de portfólio.
