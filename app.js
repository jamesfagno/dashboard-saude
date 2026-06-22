// app.js — Dashboard Gestão em Saúde
// Autenticação 100% estática via Web Crypto API (SHA-256 no browser)
// Não depende de servidor — funciona no Vercel como site estático

let dadosOriginais = null;
let graficoPizza   = null;
let graficoBarras  = null;

const CORES_GRAFICO = {
    SUS:        "#4a90d9",
    Particular: "#27ae60",
    "Convênio": "#f39c12",
};

// ── 0. Elementos da tela de login ──────────────────────────────

const telaLogin   = document.getElementById("tela-login");
const appEl       = document.getElementById("app");
const formLogin   = document.getElementById("form-login");
const inputUser   = document.getElementById("login-usuario");
const inputSenha  = document.getElementById("login-senha");
const btnLogin    = document.getElementById("btn-login");
const loginErroEl = document.getElementById("login-erro");
const usuarioEl   = document.getElementById("usuario-logado");
const btnLogout   = document.getElementById("btn-logout");

// ── 0.1 Calcular SHA-256 no browser (Web Crypto API nativa) ────

async function sha256(texto) {
    const encoder = new TextEncoder();
    const data    = encoder.encode(texto);
    const buffer  = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(buffer))
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");
}

// ── 0.2 Mostrar / ocultar telas ────────────────────────────────

function mostrarApp(usuario) {
    telaLogin.classList.add("app-oculto");
    appEl.classList.remove("app-oculto");
    if (usuario) {
        usuarioEl.textContent = `${usuario.nome} • ${usuario.perfil}`;
    }
    if (!dadosOriginais) carregarDados();
}

function mostrarLogin() {
    appEl.classList.add("app-oculto");
    telaLogin.classList.remove("app-oculto");
    inputSenha.value = "";
    loginErroEl.textContent = "";
}

// ── 0.3 Verificar sessão salva ao carregar a página ─────────────

function verificarSessao() {
    const sessao = sessionStorage.getItem("usuario_logado");
    if (sessao) {
        try {
            mostrarApp(JSON.parse(sessao));
        } catch {
            mostrarLogin();
        }
    } else {
        mostrarLogin();
    }
}

// ── 0.4 Submeter login ──────────────────────────────────────────

formLogin.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    loginErroEl.textContent = "";
    btnLogin.disabled    = true;
    btnLogin.textContent = "Verificando...";

    try {
        // Carrega dados.json para obter a lista de usuários
        const resposta = await fetch("dados.json");
        if (!resposta.ok) throw new Error("Não foi possível carregar os dados.");
        const dados = await resposta.json();

        const usuarios = dados.usuarios || [];
        const loginDigitado = inputUser.value.trim().toLowerCase();
        const hashDigitado  = await sha256(inputSenha.value);

        const usuario = usuarios.find(
            u => u.login.toLowerCase() === loginDigitado && u.senha_hash === hashDigitado
        );

        if (!usuario) {
            loginErroEl.textContent = "Login ou senha incorretos.";
            return;
        }

        // Salva sessão e exibe o dashboard
        sessionStorage.setItem("usuario_logado", JSON.stringify(usuario));
        dadosOriginais = dados; // aproveita o fetch já feito
        mostrarApp(usuario);
        renderizarTudo(dadosOriginais);
        popularFiltroMes(dadosOriginais);
        atualizarStatus("Dados carregados.");

    } catch (erro) {
        loginErroEl.textContent = "Erro ao conectar. Tente novamente.";
        console.error(erro);
    } finally {
        btnLogin.disabled    = false;
        btnLogin.textContent = "Entrar";
    }
});

// ── 0.5 Logout ──────────────────────────────────────────────────

btnLogout.addEventListener("click", () => {
    sessionStorage.removeItem("usuario_logado");
    dadosOriginais = null;
    graficoPizza   = null;
    graficoBarras  = null;
    mostrarLogin();
});

// ── 1. Carregar dados (usado quando sessão já existe) ───────────

async function carregarDados() {
    try {
        const resposta = await fetch("dados.json");
        if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
        dadosOriginais = await resposta.json();
        atualizarStatus("Dados carregados.");
        renderizarTudo(dadosOriginais);
        popularFiltroMes(dadosOriginais);
    } catch (erro) {
        atualizarStatus("Erro ao carregar dados.json.");
        console.error(erro);
    }
}

// ── 2. Renderizar tudo ─────────────────────────────────────────

function renderizarTudo(dados) {
    atualizarKPIs(dados);
    atualizarGraficoPizza(dados);
    atualizarGraficoBarras(dados);
    atualizarTabela(dados);
}

// ── 3. KPIs ───────────────────────────────────────────────────

function atualizarKPIs(dados) {
    const vol  = dados.volume;
    const rec  = dados.receita;
    const canc = dados.cancelamento;

    definirTexto("kpi-total",        formatarNumero(vol.total));
    definirTexto("kpi-receita",      formatarMoeda(rec.geral.total));
    definirTexto("kpi-ticket",       formatarMoeda(rec.geral.ticket_medio));
    definirTexto("kpi-cancelamento", formatarPercentual(canc.taxa_cancelamento));
}

// ── 4. Gráfico de pizza ───────────────────────────────────────

function atualizarGraficoPizza(dados) {
    const vol    = dados.volume;
    const labels = ["SUS", "Particular", "Convênio"];
    const values = [vol.SUS, vol.Particular, vol["Convênio"]];
    const cores  = labels.map(t => CORES_GRAFICO[t]);

    const ctx = document.getElementById("grafico-pizza").getContext("2d");
    if (graficoPizza) graficoPizza.destroy();

    graficoPizza = new Chart(ctx, {
        type: "doughnut",
        data: { labels, datasets: [{ data: values, backgroundColor: cores,
                borderWidth: 2, borderColor: "#fff" }] },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { font: { size: 13 } } },
                tooltip: { callbacks: { label: c => ` ${c.label}: ${formatarNumero(c.raw)} consultas` } }
            }
        }
    });
}

// ── 5. Gráfico de barras ──────────────────────────────────────

function atualizarGraficoBarras(dados) {
    const saldo  = dados.saldo_mes || {};
    const meses  = Object.keys(saldo);
    const values = meses.map(m => saldo[m].receita);

    const ctx = document.getElementById("grafico-barras").getContext("2d");
    if (graficoBarras) graficoBarras.destroy();

    graficoBarras = new Chart(ctx, {
        type: "bar",
        data: { labels: meses, datasets: [{ label: "Receita (R$)", data: values,
                backgroundColor: "#4a90d9", borderRadius: 6 }] },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: c => ` ${formatarMoeda(c.raw)}` } }
            },
            scales: {
                y: { beginAtZero: true,
                     ticks: { callback: v => "R$ " + v.toLocaleString("pt-BR") } }
            }
        }
    });
}

// ── 6. Tabela de gargalos ─────────────────────────────────────

function atualizarTabela(dados) {
    const rec    = dados.receita;
    const canc   = dados.cancelamento;
    const perdas = dados.perdas_por_tipo || {};
    const corpo  = document.getElementById("tabela-corpo");
    const tipos  = ["SUS", "Particular", "Convênio"];
    const badges = {
        SUS: "badge-sus",
        Particular: "badge-particular",
        "Convênio": "badge-convenio"
    };

    let html = "";
    tipos.forEach(tipo => {
        const r      = rec[tipo];
        const cancel = perdas[tipo]?.canceladas || 0;
        const glosa  = perdas[tipo]?.glosadas   || 0;

        html += `<tr>
            <td class="col-tipo"><span class="badge ${badges[tipo]}">${tipo}</span></td>
            <td class="col-num">${formatarNumero(r.quantidade)}</td>
            <td class="col-num ${cancel > 0 ? "celula-alerta" : ""}">${formatarNumero(cancel)}</td>
            <td class="col-num ${glosa  > 0 ? "celula-alerta" : ""}">${formatarNumero(glosa)}</td>
            <td class="col-money">${formatarMoeda(r.total)}</td>
            <td class="col-money">${formatarMoeda(r.ticket_medio)}</td>
        </tr>`;
    });

    html += `<tr class="linha-total">
        <td class="col-tipo"><span class="badge badge-geral">Total</span></td>
        <td class="col-num">${formatarNumero(canc.realizadas)}</td>
        <td class="col-num ${canc.canceladas > 0 ? "celula-alerta" : ""}">
            ${formatarNumero(canc.canceladas)} <span class="pct">(${formatarPercentual(canc.taxa_cancelamento)})</span>
        </td>
        <td class="col-num ${canc.glosadas > 0 ? "celula-alerta" : ""}">
            ${formatarNumero(canc.glosadas)} <span class="pct">(${formatarPercentual(canc.taxa_glosa)})</span>
        </td>
        <td class="col-money">${formatarMoeda(rec.geral.total)}</td>
        <td class="col-money">${formatarMoeda(rec.geral.ticket_medio)}</td>
    </tr>`;

    corpo.innerHTML = html;
}

// ── 7. Filtros ────────────────────────────────────────────────

function popularFiltroMes(dados) {
    const saldo  = dados.saldo_mes || {};
    const select = document.getElementById("filtro-mes");
    // Limpa opções antigas (mantém só "Todos os meses")
    while (select.options.length > 1) select.remove(1);
    Object.keys(saldo).forEach(mes => {
        const op = document.createElement("option");
        op.value = mes; op.textContent = mes;
        select.appendChild(op);
    });
}

document.getElementById("btn-atualizar").addEventListener("click", () => {
    if (!dadosOriginais) return;

    const tipo = document.getElementById("filtro-tipo").value;
    const mes  = document.getElementById("filtro-mes").value;
    let d = JSON.parse(JSON.stringify(dadosOriginais));

    if (tipo !== "todos") {
        ["SUS", "Particular", "Convênio"].filter(t => t !== tipo).forEach(t => {
            d.volume[t]         = 0;
            d.receita[t]        = { total: 0, quantidade: 0, ticket_medio: 0 };
            d.perdas_por_tipo[t]= { canceladas: 0, glosadas: 0 };
        });
        d.volume.total  = dadosOriginais.volume[tipo];
        d.receita.geral = dadosOriginais.receita[tipo];

        const cancTipo = dadosOriginais.perdas_por_tipo[tipo]?.canceladas || 0;
        const glosTipo = dadosOriginais.perdas_por_tipo[tipo]?.glosadas   || 0;
        d.cancelamento = {
            total:              dadosOriginais.volume[tipo],
            realizadas:         dadosOriginais.receita[tipo].quantidade,
            canceladas:         cancTipo,
            glosadas:           glosTipo,
            taxa_cancelamento:  dadosOriginais.volume[tipo]
                ? round1(cancTipo / dadosOriginais.volume[tipo] * 100) : 0,
            taxa_glosa:         dadosOriginais.volume[tipo]
                ? round1(glosTipo / dadosOriginais.volume[tipo] * 100) : 0,
        };
    }

    if (mes !== "todos") {
        const orig  = dadosOriginais.saldo_mes || {};
        d.saldo_mes = orig[mes] ? { [mes]: orig[mes] } : {};
    }

    renderizarTudo(d);
    atualizarStatus(`Filtro: tipo=${tipo}, mês=${mes}`);
});

// ── Utilitários ───────────────────────────────────────────────

function round1(v) {
    return Math.round(v * 10) / 10;
}

function formatarMoeda(v) {
    return "R$ " + Number(v).toLocaleString("pt-BR",
        { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatarNumero(v) {
    return Number(v).toLocaleString("pt-BR");
}

function formatarPercentual(v) {
    return Number(v).toLocaleString("pt-BR",
        { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + "%";
}

function definirTexto(id, texto) {
    const el = document.getElementById(id);
    if (el) el.textContent = texto;
}

function atualizarStatus(msg) {
    const agora = new Date().toLocaleTimeString("pt-BR");
    definirTexto("status-msg", `${agora} — ${msg}`);
}

// ── Inicialização ─────────────────────────────────────────────
verificarSessao();
