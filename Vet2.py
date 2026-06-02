import streamlit as st
import json
import os
from datetime import datetime

# ─────────────────────────────────────────
# CONFIG & ESTILOS (Adaptado al nuevo diseño)
# ─────────────────────────────────────────
st.set_page_config(
    page_title="VetSystem",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,400;0,500;1,400&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;0,9..144,900;1,9..144,400&display=swap');

:root {
  --bg:      #f4f0ec;
  --ink:     #18120e;
  --ink2:    #3a3028;
  --muted:   #9a8e82;
  --border:  #d8cfc3;
  --surface: #ece7df;
  --surface2:#e3ddd4;

  --violet:  #4a2c8a;
  --violet2: #7b52d4;
  --teal:    #1a7a6e;
  --orange:  #c94f12;
  --green:   #2a6b3c;
  --red:     #b83025;
  --gold:    #b8860b;

  --code-bg: #1a1520;
  --code-fg: #e5dff5;
}

html, body, [class*="css"] {
    font-family: 'Fraunces', Georgia, serif !important;
    color: var(--ink) !important;
}

/* Fondo general con textura SVG */
.stApp {
    background: var(--bg);
    color: var(--ink);
}
.stApp::before {
    content:'';
    position:fixed; inset:0; z-index:0; pointer-events:none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    background-size:180px 180px;
}

/* Ocultar elementos nativos de Streamlit */
header[data-testid="stHeader"] { background: transparent !important; }
footer { display: none !important; }

/* Sidebar estilo Header oscuro del HTML */
section[data-testid="stSidebar"] {
    background: var(--ink);
    border-right: 1px solid #2a2035;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #2a2035 !important;
}

/* Título principal (Hero) */
.vet-hero {
    position: relative;
    background: var(--ink);
    padding: 3rem 2.5rem;
    overflow: hidden;
    margin-bottom: 2rem;
    border-radius: 6px;
}
.vet-hero::after {
    content:'VET';
    position:absolute; right:-1rem; top:-2rem;
    font-family:'Fraunces',serif; font-size:10rem; font-weight:900;
    font-style:italic; color:rgba(255,255,255,.04);
    pointer-events:none; line-height:1; letter-spacing:-.05em;
    user-select:none;
}
.vet-hero h1 {
    font-size: clamp(2rem, 5vw, 3.5rem); 
    font-weight: 900; line-height: .9; 
    letter-spacing: -.04em; font-style: italic; color: white;
    margin: 0;
}
.vet-hero p {
    font-family: 'DM Mono', monospace; 
    font-size: .65rem; 
    color: #6b6070; 
    letter-spacing: .05em;
    text-transform: uppercase;
    margin-top: 1rem;
}

/* Cards de estadísticas (Estilo geo-card) */
.stat-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    transition: box-shadow 0.2s;
    overflow: hidden;
}
.stat-card:hover { box-shadow: 0 4px 20px rgba(74,44,138,.1); }
.stat-num {
    font-size: 2.2rem;
    font-weight: 700;
    font-style: italic;
    color: var(--violet);
    line-height: 1;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-top: 0.8rem;
}

/* Sección headers (Estilo sec-label) */
.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--violet2);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.section-header::after {
    content: ''; flex: 1; height: 1px; background: currentColor; opacity: .2;
}
.section-header span {
    font-weight: bold;
}

/* Tabla custom (Estilo events-table) */
.vet-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.2rem 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    background: white;
}
.vet-table th {
    background: var(--ink);
    color: white;
    padding: 0.65rem 1rem;
    text-align: left;
    font-size: 0.63rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.vet-table td {
    padding: 0.7rem 1rem;
    border-bottom: 1px solid var(--border);
    color: var(--ink2);
    vertical-align: middle;
}
.vet-table tr:hover td { background: var(--surface); }

/* Badges */
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    padding: 0.25rem 0.8rem;
    border-radius: 2px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
.badge-blue { background: #edf7f5; color: var(--teal); border: 1px solid var(--teal); }
.badge-green { background: #eef7f5; color: var(--green); border: 1px solid var(--green); }
.badge-orange { background: #fdf1ec; color: var(--orange); border: 1px solid var(--orange); }
.badge-red { background: #fdf0ed; color: var(--red); border: 1px solid var(--red); }
.badge-gray { background: var(--surface); color: var(--muted); border: 1px solid var(--border); }
.badge-purple { background: #f0ecf8; color: var(--violet); border: 1px solid var(--violet); }
.badge-pink { background: #fdf8ec; color: var(--gold); border: 1px solid var(--gold); }

/* Historial médico (Estilo recipe-step) */
.hist-entry {
    background: white;
    border: 1px solid var(--border);
    border-left: 4px solid var(--violet2);
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    border-radius: 2px;
}
.hist-date {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.hist-motivo { font-size: 0.95rem; font-weight: 700; color: var(--ink); }
.hist-diag { font-size: 0.85rem; color: var(--ink2); margin-top: 0.4rem; line-height: 1.5; }

/* Ticket de venta (Estilo Code Wrap) */
.ticket {
    background: var(--code-bg);
    border-radius: 6px;
    border: 1px solid #2a2035;
    border-left: 3px solid var(--violet2);
    padding: 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: var(--code-fg);
}
.ticket-header {
    text-align: center;
    border-bottom: 1px dashed #4a4055;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}
.ticket-total {
    border-top: 1px dashed #4a4055;
    margin-top: 1rem;
    padding-top: 1rem;
    text-align: right;
    font-size: 1.1rem;
    font-weight: 600;
    color: #5ecf8a;
}

/* Botones Streamlit override */
.stButton > button {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    background: var(--violet) !important;
    color: white !important;
    border: none !important;
    border-radius: 2px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    transition: background 0.2s !important;
    padding: 0.55rem 1.4rem !important;
}
.stButton > button:hover {
    background: var(--ink) !important;
    color: white !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: white !important;
    border: 2px inset #a090c0 !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    font-family: Arial, sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus {
    border-color: var(--violet) !important;
    box-shadow: none !important;
}

/* Tabs estilo HTML */
button[data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.66rem !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    border-bottom: 3px solid transparent !important;
    background: none !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--violet) !important;
    border-bottom-color: var(--violet) !important;
}

/* Alertas (Estilo callouts) */
.alert-success { background: #edf7f5; border: 1px solid var(--border); border-left: 3px solid var(--teal); border-radius: 4px; padding: 1rem 1.2rem; color: var(--ink); font-size: 0.88rem; margin: 0.5rem 0; display:flex; gap: 0.9rem;}
.alert-error { background: #fdf1ec; border: 1px solid var(--border); border-left: 3px solid var(--red); border-radius: 4px; padding: 1rem 1.2rem; color: var(--ink); font-size: 0.88rem; margin: 0.5rem 0; display:flex; gap: 0.9rem;}
.alert-warn { background: #fdf8ec; border: 1px solid var(--border); border-left: 3px solid var(--gold); border-radius: 4px; padding: 1rem 1.2rem; color: var(--ink); font-size: 0.88rem; margin: 0.5rem 0; display:flex; gap: 0.9rem;}

/* POS carrito */
.cart-item {
    background: white;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cart-item-name { font-weight: 700; color: var(--ink); font-size: 0.88rem; }
.cart-item-price { color: var(--teal); font-family: 'DM Mono', monospace; font-weight: 700; }
.cart-item-qty { color: var(--muted); font-family: 'DM Mono', monospace; font-size: 0.7rem; }

.total-bar {
    background: var(--ink);
    border-radius: 4px;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}
.total-label { color: white; font-family: 'DM Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; }
.total-amount { font-size: 1.6rem; font-weight: 800; color: #5ecf8a; font-family: 'DM Mono', monospace; }

/* Preview producto agregado */
.prod-preview {
    background: #eef7f5;
    border: 1px solid var(--border);
    border-left: 4px solid var(--teal);
    border-radius: 4px;
    padding: 1.1rem 1.4rem;
    margin-top: 1rem;
}
.prod-preview-title { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--teal); text-transform: uppercase; letter-spacing: 0.1em; font-weight: bold; margin-bottom: 0.6rem; }
.prod-preview-name { font-size: 1rem; font-weight: 700; color: var(--ink); margin-bottom: 0.4rem; }
.prod-preview-meta { font-size: 0.82rem; color: var(--ink2); font-family: 'DM Mono', monospace; }

/* Paneles de Edición */
.edit-panel {
    background: white;
    border: 1px solid var(--border);
    border-top: 3px solid var(--violet);
    border-radius: 4px;
    padding: 1.25rem 1.5rem;
    margin-top: 0.5rem;
}
.danger-zone {
    background: #fdf0ed;
    border: 1px solid var(--border);
    border-left: 3px solid var(--red);
    border-radius: 4px;
    padding: 1rem 1.25rem;
    margin-top: 1.5rem;
}
.danger-zone-title { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--red); text-transform: uppercase; letter-spacing: 0.1em; font-weight: bold; margin-bottom: 0.75rem; }

/* Fixes menores */
hr { border-color: var(--border) !important; margin: 2rem 0 !important;}
.stRadio label, .stCheckbox label { color: var(--ink) !important; font-family: Arial, sans-serif !important;}
p, div { color: var(--ink); }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LÓGICA DE DATOS
# ─────────────────────────────────────────
ARCHIVO_DATOS = 'datos_veterinaria.json'

def cargar_datos():
    estructura_base = {"mascotas": {}, "inventario": {}, "ventas": [], "facturas": []}
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            if "mascotas" not in datos:
                datos = {"mascotas": datos, "inventario": {}, "ventas": [], "facturas": []}
            if "facturas" not in datos:
                datos["facturas"] = []
            if "inventario" in datos:
                for p_id, info in datos["inventario"].items():
                    if "caducidad" not in info: info["caducidad"] = "N/A"
            if "mascotas" in datos:
                for m_id, info in datos["mascotas"].items():
                    if "peso" not in info: info["peso"] = "N/A"
                    if "sexo" not in info: info["sexo"] = "N/A"
            return datos
    return estructura_base

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def generar_id_mascota(datos):
    if not datos["mascotas"]: return "VET-001"
    ids = [int(k.split('-')[1]) for k in datos["mascotas"].keys()]
    return f"VET-{max(ids) + 1:03d}"

def generar_id_producto(datos):
    if not datos["inventario"]: return "PROD-001"
    ids = [int(k.split('-')[1]) for k in datos["inventario"].keys()]
    return f"PROD-{max(ids) + 1:03d}"

def generar_id_factura(datos):
    if not datos["facturas"]: return "FAC-0001"
    ids = [int(f["id"].split('-')[1]) for f in datos["facturas"]]
    return f"FAC-{max(ids) + 1:04d}"

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "datos" not in st.session_state:
    st.session_state.datos = cargar_datos()
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "total_factura" not in st.session_state:
    st.session_state.total_factura = 0.0
if "cliente_pos" not in st.session_state:
    st.session_state.cliente_pos = ""
if "factura_generada" not in st.session_state:
    st.session_state.factura_generada = None
if "pos_iniciado" not in st.session_state:
    st.session_state.pos_iniciado = False
if "ultimo_producto_agregado" not in st.session_state:
    st.session_state.ultimo_producto_agregado = None
if "confirm_delete_mascota" not in st.session_state:
    st.session_state.confirm_delete_mascota = None
if "confirm_delete_producto" not in st.session_state:
    st.session_state.confirm_delete_producto = None

datos = st.session_state.datos

# ─────────────────────────────────────────
# SIDEBAR NAVEGACIÓN
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem 0;'>
        <div style='font-family:"Fraunces",serif; font-size:1.8rem; font-weight:800; font-style:italic; color:white;'>🐾 VetSystem</div>
        <div style='font-family:"DM Mono",monospace; font-size:0.65rem; color:#b0a8b5; letter-spacing:0.1em; text-transform:uppercase; margin-top:0.5rem;'>Panel de Gestión</div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Módulos",
        [
            "🏠 Dashboard",
            "🐶 Mascotas",
            "🩺 Consultas",
            "📦 Inventario",
            "💵 Punto de Venta",
            "📊 Facturas",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    n_mascotas = len(datos["mascotas"])
    n_productos = len(datos["inventario"])
    n_facturas = len(datos["facturas"])
    st.markdown(f"""
    <div style='font-family:"DM Mono",monospace; font-size:0.75rem; color:#b0a8b5; padding: 0.5rem 0; line-height: 1.8;'>
        <div>🐾 Mascotas: <b style='color:white'>{n_mascotas}</b></div>
        <div>📦 Productos: <b style='color:white'>{n_productos}</b></div>
        <div>🧾 Facturas: <b style='color:white'>{n_facturas}</b></div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER: Badges
# ─────────────────────────────────────────
def badge_categoria(cat):
    mapa = {
        "Fármaco": ("badge-red", "💊 Fármaco"),
        "Alimento": ("badge-green", "🌿 Alimento"),
        "Accesorio": ("badge-blue", "🎀 Accesorio"),
    }
    cls, lbl = mapa.get(cat, ("badge-gray", cat))
    return f'<span class="badge {cls}">{lbl}</span>'

def badge_especie(esp):
    mapa = {"Perro": "🐕", "Gato": "🐈", "Ave": "🦜", "Conejo": "🐇", "Reptil": "🦎"}
    ico = mapa.get(esp, "🐾")
    return f'<span class="badge badge-purple">{ico} {esp}</span>'

def badge_sexo(sexo):
    if sexo == "Macho":
        return '<span class="badge badge-blue">♂ Macho</span>'
    elif sexo == "Hembra":
        return '<span class="badge badge-pink">♀ Hembra</span>'
    else:
        return '<span class="badge badge-gray">— N/A</span>'


# ══════════════════════════════════════════
# PÁGINA: DASHBOARD
# ══════════════════════════════════════════
if pagina == "🏠 Dashboard":
    st.markdown("""
    <div class='vet-hero'>
        <h1>Sistema Veterinaria</h1>
        <p>Control clínico · Inventario · Punto de venta</p>
    </div>
    """, unsafe_allow_html=True)

    total_ingresos = sum(f["total"] for f in datos["facturas"])
    stock_bajo = sum(1 for p in datos["inventario"].values() if p["stock"] < 5)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-num'>{len(datos['mascotas'])}</div>
            <div class='stat-label'>Pacientes</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-num'>{len(datos['inventario'])}</div>
            <div class='stat-label'>Productos</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-num'>{len(datos['facturas'])}</div>
            <div class='stat-label'>Facturas</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='stat-card'>
            <div class='stat-num'>${total_ingresos:,.0f}</div>
            <div class='stat-label'>Ingresos</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-header'><span>Últimas mascotas</span></div>", unsafe_allow_html=True)
        if datos["mascotas"]:
            items = list(datos["mascotas"].items())[-5:][::-1]
            filas = "".join(
                f"<tr><td><code>{id_m}</code></td><td><strong>{i['nombre']}</strong></td><td>{badge_especie(i['especie'])}</td><td>{badge_sexo(i.get('sexo','N/A'))}</td><td>{i['dueño']}</td></tr>"
                for id_m, i in items
            )
            st.markdown(f"""
            <table class='vet-table'>
                <thead><tr><th>ID</th><th>Nombre</th><th>Especie</th><th>Sexo</th><th>Dueño</th></tr></thead>
                <tbody>{filas}</tbody>
            </table>""", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-warn'><span>⚠️</span> No hay mascotas registradas.</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='section-header' style='color:var(--teal)'><span>Últimas facturas</span></div>", unsafe_allow_html=True)
        if datos["facturas"]:
            ultimas = datos["facturas"][-5:][::-1]
            filas = "".join(
                f"<tr><td><code>{f['id']}</code></td><td>{f['cliente'][:14]}</td><td>{f['fecha'][:10]}</td><td style='color:var(--teal);font-weight:bold'>${f['total']:.2f}</td></tr>"
                for f in ultimas
            )
            st.markdown(f"""
            <table class='vet-table'>
                <thead><tr><th>ID</th><th>Cliente</th><th>Fecha</th><th>Total</th></tr></thead>
                <tbody>{filas}</tbody>
            </table>""", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-warn'><span>⚠️</span> Sin facturas aún.</div>", unsafe_allow_html=True)

    if stock_bajo > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='alert-error'><span>🚨</span> <div><b>{stock_bajo}</b> producto(s) con stock menor a 5 unidades. Revisá el inventario.</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PÁGINA: MASCOTAS
# ══════════════════════════════════════════
elif pagina == "🐶 Mascotas":
    st.markdown("<div class='section-header'><span>Gestión de Mascotas</span></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Ver Mascotas", "➕ Registrar", "🔍 Buscar / Perfil", "✏️ Editar / Eliminar"])

    with tab1:
        if not datos["mascotas"]:
            st.markdown("<div class='alert-warn'><span>⚠️</span> No hay mascotas registradas aún.</div>", unsafe_allow_html=True)
        else:
            busq = st.text_input("🔎 Filtrar por nombre o dueño...", placeholder="Ej: Max, Juan Pérez")
            mascotas_filtradas = {
                k: v for k, v in datos["mascotas"].items()
                if not busq or busq.lower() in v["nombre"].lower() or busq.lower() in v["dueño"].lower()
            }
            filas = "".join(
                f"""<tr>
                    <td><code>{id_m}</code></td>
                    <td><b>{i['nombre']}</b></td>
                    <td>{badge_especie(i['especie'])}</td>
                    <td>{badge_sexo(i.get('sexo','N/A'))}</td>
                    <td>{i['raza']}</td>
                    <td>{i.get('peso','N/A')}</td>
                    <td>{i['dueño']}</td>
                    <td>{i['telefono']}</td>
                    <td><span class='badge badge-gray'>{len(i['historial'])} reg</span></td>
                </tr>"""
                for id_m, i in mascotas_filtradas.items()
            )
            st.markdown(f"""
            <table class='vet-table'>
                <thead><tr><th>ID</th><th>Nombre</th><th>Especie</th><th>Sexo</th><th>Raza</th><th>Peso</th><th>Dueño</th><th>Teléfono</th><th>Historial</th></tr></thead>
                <tbody>{filas}</tbody>
            </table>""", unsafe_allow_html=True)
            st.caption(f"{len(mascotas_filtradas)} mascota(s) encontrada(s)")

    with tab2:
        with st.form("form_mascota", clear_on_submit=True):
            st.markdown("### Datos del paciente")
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre de la mascota *")
            especie = c2.selectbox("Especie *", ["Perro", "Gato", "Ave", "Conejo", "Reptil", "Otro"])
            c3, c4 = st.columns(2)
            raza = c3.text_input("Raza *")
            edad = c4.text_input("Edad", placeholder="Ej: 2 años")
            c5, c6, c7 = st.columns(3)
            peso = c5.text_input("Peso", placeholder="Ej: 8.5 kg")
            sexo = c6.selectbox("Sexo *", ["Macho", "Hembra"])
            c7.markdown("")

            st.markdown("### Datos del dueño")
            c8, c9 = st.columns(2)
            dueño = c8.text_input("Nombre del dueño *")
            telefono = c9.text_input("Teléfono")

            submitted = st.form_submit_button("Registrar Mascota", use_container_width=True)
            if submitted:
                if not nombre or not especie or not raza or not dueño:
                    st.markdown("<div class='alert-error'><span>❌</span> Completá los campos obligatorios (*)</div>", unsafe_allow_html=True)
                else:
                    id_m = generar_id_mascota(datos)
                    datos["mascotas"][id_m] = {
                        "nombre": nombre.strip().title(),
                        "especie": especie,
                        "raza": raza.strip().title(),
                        "edad": edad.strip(),
                        "peso": peso.strip() or "N/A",
                        "sexo": sexo,
                        "dueño": dueño.strip().title(),
                        "telefono": telefono.strip(),
                        "historial": []
                    }
                    guardar_datos(datos)
                    st.session_state.datos = datos
                    st.markdown(f"<div class='alert-success'><span>✅</span> Mascota registrada con ID: <code>{id_m}</code></div>", unsafe_allow_html=True)

    with tab3:
        ids_disponibles = list(datos["mascotas"].keys())
        if not ids_disponibles:
            st.markdown("<div class='alert-warn'><span>⚠️</span> No hay mascotas registradas.</div>", unsafe_allow_html=True)
        else:
            opciones = {f"{id_m} — {i['nombre']} ({i['dueño']})": id_m for id_m, i in datos["mascotas"].items()}
            seleccion = st.selectbox("Seleccioná una mascota", list(opciones.keys()))
            id_sel = opciones[seleccion]
            info = datos["mascotas"][id_sel]

            st.markdown(f"""
            <div style='background:white; border:1px solid var(--border); border-top: 3px solid var(--violet); border-radius:4px; padding:1.25rem 1.5rem; margin:1rem 0;'>
                <div style='font-size:1.6rem; font-weight:700; color:var(--ink); margin-bottom:0.75rem; font-style: italic;'>
                    {info['nombre']} <code style='font-size:0.75rem; color:var(--violet); background:var(--surface); padding:0.2rem 0.5rem; border-radius:2px;'>{id_sel}</code>
                </div>
                <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:0.8rem; font-size:0.9rem; color:var(--ink2);'>
                    <div><b>Especie:</b> {info['especie']} ({info['raza']})</div>
                    <div><b>Edad:</b> {info.get('edad','N/A')}</div>
                    <div><b>Peso:</b> {info.get('peso','N/A')}</div>
                    <div><b>Sexo:</b> {info.get('sexo', 'N/A')}</div>
                    <div><b>Dueño:</b> {info['dueño']}</div>
                    <div><b>Tel:</b> {info['telefono']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='section-header' style='color:var(--teal)'><span>Historial médico</span></div>", unsafe_allow_html=True)
            if not info["historial"]:
                st.markdown("<div class='alert-warn'><span>ℹ️</span> Sin registros en el historial.</div>", unsafe_allow_html=True)
            else:
                for reg in reversed(info["historial"]):
                    color = "var(--red)" if "Farmacia" in reg["motivo"] else "var(--teal)"
                    st.markdown(f"""
                    <div class='hist-entry' style='border-left-color:{color}'>
                        <div class='hist-date'>{reg['fecha']}</div>
                        <div class='hist-motivo'>{reg['motivo']}</div>
                        {f"<div class='hist-diag'><strong>Diagnóstico:</strong> {reg['diagnostico']}</div>" if reg['diagnostico'] != 'N/A' else ''}
                        <div class='hist-diag' style='font-style:italic;'>{reg['tratamiento']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab4:
        if not datos["mascotas"]:
            st.markdown("<div class='alert-warn'><span>⚠️</span> No hay mascotas registradas.</div>", unsafe_allow_html=True)
        else:
            opciones_edit = {f"{id_m} — {i['nombre']} ({i['dueño']})": id_m for id_m, i in datos["mascotas"].items()}
            sel_edit = st.selectbox("Seleccioná la mascota a modificar", list(opciones_edit.keys()), key="sel_edit_mascota")
            id_edit = opciones_edit[sel_edit]
            info_edit = datos["mascotas"][id_edit]

            st.markdown("<div class='edit-panel'>", unsafe_allow_html=True)
            st.markdown(f"**Editando:** `{id_edit}` — **{info_edit['nombre']}**")
            st.markdown("<br>", unsafe_allow_html=True)

            with st.form("form_editar_mascota"):
                st.markdown("### Datos del paciente")
                ec1, ec2 = st.columns(2)
                e_nombre = ec1.text_input("Nombre *", value=info_edit["nombre"])
                especies_lista = ["Perro", "Gato", "Ave", "Conejo", "Reptil", "Otro"]
                e_especie = ec2.selectbox(
                    "Especie *",
                    especies_lista,
                    index=especies_lista.index(info_edit["especie"]) if info_edit["especie"] in especies_lista else 0
                )
                ec3, ec4 = st.columns(2)
                e_raza = ec3.text_input("Raza *", value=info_edit["raza"])
                e_edad = ec4.text_input("Edad", value=info_edit.get("edad", ""))
                ec5, ec6 = st.columns(2)
                e_peso = ec5.text_input("Peso", value=info_edit.get("peso", "N/A"))
                sexos_lista = ["Macho", "Hembra"]
                e_sexo = ec6.selectbox(
                    "Sexo *",
                    sexos_lista,
                    index=sexos_lista.index(info_edit.get("sexo", "Macho")) if info_edit.get("sexo") in sexos_lista else 0
                )

                st.markdown("### Datos del dueño")
                ec7, ec8 = st.columns(2)
                e_dueño = ec7.text_input("Nombre del dueño *", value=info_edit["dueño"])
                e_telefono = ec8.text_input("Teléfono", value=info_edit["telefono"])

                guardar_edit = st.form_submit_button("Guardar cambios", use_container_width=True)
                if guardar_edit:
                    if not e_nombre or not e_raza or not e_dueño:
                        st.markdown("<div class='alert-error'><span>❌</span> Completá los campos obligatorios.</div>", unsafe_allow_html=True)
                    else:
                        datos["mascotas"][id_edit].update({
                            "nombre": e_nombre.strip().title(),
                            "especie": e_especie,
                            "raza": e_raza.strip().title(),
                            "edad": e_edad.strip(),
                            "peso": e_peso.strip() or "N/A",
                            "sexo": e_sexo,
                            "dueño": e_dueño.strip().title(),
                            "telefono": e_telefono.strip(),
                        })
                        guardar_datos(datos)
                        st.session_state.datos = datos
                        st.markdown("<div class='alert-success'><span>✅</span> Datos actualizados correctamente.</div>", unsafe_allow_html=True)
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='danger-zone'>", unsafe_allow_html=True)
            st.markdown("<div class='danger-zone-title'>Zona de peligro</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem; margin-bottom:1rem;'>Eliminar el registro de <strong>{info_edit['nombre']}</strong> ({id_edit}). Esta acción es irreversible y borrará también su historial clínico.</p>", unsafe_allow_html=True)

            if st.session_state.confirm_delete_mascota == id_edit:
                st.markdown("<div class='alert-error'><span>⚠️</span> ¿Confirmás la eliminación? Esta acción no se puede deshacer.</div>", unsafe_allow_html=True)
                cd1, cd2, cd3 = st.columns([2, 2, 4])
                with cd1:
                    if st.button("Sí, eliminar", key="confirm_del_m"):
                        del datos["mascotas"][id_edit]
                        guardar_datos(datos)
                        st.session_state.datos = datos
                        st.session_state.confirm_delete_mascota = None
                        st.rerun()
                with cd2:
                    if st.button("Cancelar", key="cancel_del_m"):
                        st.session_state.confirm_delete_mascota = None
                        st.rerun()
            else:
                if st.button(f"Eliminar {info_edit['nombre']}", key="del_mascota_btn"):
                    st.session_state.confirm_delete_mascota = id_edit
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PÁGINA: CONSULTAS CLÍNICAS
# ══════════════════════════════════════════
elif pagina == "🩺 Consultas":
    st.markdown("<div class='section-header' style='color:var(--teal)'><span>Registro de Consulta Clínica</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='alert-warn'><span>💡</span> El cobro de consultas se realiza en el <b>Punto de Venta</b>. Acá solo se registra el historial clínico.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not datos["mascotas"]:
        st.markdown("<div class='alert-error'><span>❌</span> No hay mascotas registradas. Registrá primero un paciente.</div>", unsafe_allow_html=True)
    else:
        opciones = {f"{id_m} — {i['nombre']} ({i['dueño']})": id_m for id_m, i in datos["mascotas"].items()}
        seleccion = st.selectbox("Seleccioná el paciente", list(opciones.keys()))
        id_sel = opciones[seleccion]
        paciente = datos["mascotas"][id_sel]

        st.markdown(f"""
        <div style='background:white; border:1px solid var(--border); border-radius:4px; padding:1rem; margin-bottom:1rem; font-size:0.9rem;'>
            <b>{paciente['nombre']}</b> &nbsp;·&nbsp; 
            {paciente['especie']} ({paciente['raza']}) &nbsp;·&nbsp;
            {badge_sexo(paciente.get('sexo','N/A'))} &nbsp;·&nbsp;
            Dueño: {paciente['dueño']} &nbsp;·&nbsp; 
            Peso actual: <b>{paciente.get('peso','N/A')}</b>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_consulta", clear_on_submit=True):
            nuevo_peso = st.text_input("Actualizar peso (opcional)", placeholder=f"Peso actual: {paciente.get('peso','N/A')}")
            c1, c2 = st.columns(2)
            motivo = c1.text_input("Motivo de la consulta *", placeholder="Ej: Vómitos y decaimiento")
            diagnostico = c2.text_input("Diagnóstico", placeholder="Ej: Gastroenteritis leve")
            tratamiento = st.text_area("Tratamiento recetado *", placeholder="Ej: Amoxicilina 250mg cada 12hs por 7 días...", height=100)

            submitted = st.form_submit_button("Registrar Consulta", use_container_width=True)
            if submitted:
                if not motivo or not tratamiento:
                    st.markdown("<div class='alert-error'><span>❌</span> Completá el motivo y tratamiento.</div>", unsafe_allow_html=True)
                else:
                    if nuevo_peso.strip():
                        datos["mascotas"][id_sel]["peso"] = nuevo_peso.strip()
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
                    datos["mascotas"][id_sel]["historial"].append({
                        "fecha": fecha,
                        "motivo": f"Consulta: {motivo.strip()}",
                        "diagnostico": diagnostico.strip() or "N/A",
                        "tratamiento": tratamiento.strip()
                    })
                    guardar_datos(datos)
                    st.session_state.datos = datos
                    st.markdown("<div class='alert-success'><span>✅</span> Consulta registrada en el historial clínico.</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PÁGINA: INVENTARIO
# ══════════════════════════════════════════
elif pagina == "📦 Inventario":
    st.markdown("<div class='section-header' style='color:var(--orange)'><span>Tienda e Inventario</span></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 Ver Inventario", "➕ Agregar Producto", "✏️ Editar / Eliminar"])

    with tab1:
        col_titulo, col_refresh = st.columns([6, 1])
        with col_refresh:
            if st.button("Refrescar", use_container_width=True):
                st.session_state.datos = cargar_datos()
                datos = st.session_state.datos
                st.rerun()

        if not datos["inventario"]:
            st.markdown("<div class='alert-warn'><span>⚠️</span> El inventario está vacío.</div>", unsafe_allow_html=True)
        else:
            col_fil, col_ord = st.columns([3, 1])
            filtro = col_fil.text_input("🔎 Filtrar productos...", placeholder="Nombre o categoría")
            cat_filter = col_ord.selectbox("Categoría", ["Todas", "Fármaco", "Alimento", "Accesorio"])

            inv_filtrado = {
                k: v for k, v in datos["inventario"].items()
                if (not filtro or filtro.lower() in v["nombre"].lower())
                and (cat_filter == "Todas" or v["categoria"] == cat_filter)
            }

            filas = ""
            for id_p, info in inv_filtrado.items():
                stock_color = "var(--red)" if info["stock"] < 5 else "var(--green)" if info["stock"] > 20 else "var(--gold)"
                receta = '<span class="badge badge-red">Receta</span>' if info.get("requiere_receta") else ""
                filas += f"""<tr>
                    <td><code>{id_p}</code></td>
                    <td><strong>{info['nombre']}</strong> {receta}</td>
                    <td>{badge_categoria(info['categoria'])}</td>
                    <td>{info.get('caducidad','N/A')}</td>
                    <td style='color:var(--teal); font-weight:bold;'>${info['precio']:.2f}</td>
                    <td style='color:{stock_color}; font-weight:bold;'>{info['stock']}</td>
                </tr>"""

            st.markdown(f"""
            <table class='vet-table'>
                <thead><tr><th>ID</th><th>Nombre</th><th>Categoría</th><th>Caducidad</th><th>Precio</th><th>Stock</th></tr></thead>
                <tbody>{filas}</tbody>
            </table>""", unsafe_allow_html=True)

            valor_total = sum(p["precio"] * p["stock"] for p in datos["inventario"].values())
            st.markdown(f"""
            <div style='text-align:right; margin-top:0.75rem; font-family:"DM Mono",monospace; font-size:0.85rem; color:var(--muted);'>
                Valor total del inventario: <b style='color:var(--ink)'>${valor_total:,.2f}</b>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if st.session_state.ultimo_producto_agregado:
            ult = st.session_state.ultimo_producto_agregado
            receta_txt = " · <span style='color:var(--red)'>Requiere receta</span>" if ult.get("requiere_receta") else ""
            st.markdown(f"""
            <div class='prod-preview'>
                <div class='prod-preview-title'>Último producto agregado</div>
                <div class='prod-preview-name'>{ult['nombre']} <code>{ult['id']}</code></div>
                <div class='prod-preview-meta'>
                    {badge_categoria(ult['categoria'])} &nbsp;
                    Precio: <b style='color:var(--ink)'>${ult['precio']:.2f}</b> &nbsp;·&nbsp;
                    Stock: <b style='color:var(--ink)'>{ult['stock']}</b> unidades &nbsp;·&nbsp;
                    Cad: {ult.get('caducidad','N/A')}
                    {receta_txt}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_limpiar, _ = st.columns([2, 5])
            with col_limpiar:
                if st.button("Cerrar preview"):
                    st.session_state.ultimo_producto_agregado = None
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

        with st.form("form_producto", clear_on_submit=True):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre del producto *")
            categoria = c2.selectbox("Categoría *", ["Alimento", "Accesorio", "Fármaco"])

            c3, c4 = st.columns(2)
            precio = c3.number_input("Precio unitario ($) *", min_value=0.0, step=0.5, format="%.2f")
            stock = c4.number_input("Stock inicial *", min_value=0, step=1)

            requiere_receta = False
            caducidad = "N/A"

            if categoria == "Fármaco":
                requiere_receta = st.checkbox("¿Requiere receta médica?")
            if categoria in ["Fármaco", "Alimento"]:
                caducidad_input = st.text_input("Fecha de caducidad (DD/MM/AAAA)", placeholder="Ej: 31/12/2026")
                if caducidad_input.strip():
                    caducidad = caducidad_input.strip()

            submitted = st.form_submit_button("Agregar al Inventario", use_container_width=True)
            if submitted:
                if not nombre or precio <= 0:
                    st.markdown("<div class='alert-error'><span>❌</span> Completá nombre y precio válido.</div>", unsafe_allow_html=True)
                else:
                    id_p = generar_id_producto(datos)
                    nuevo_prod = {
                        "nombre": nombre.strip().title(),
                        "categoria": categoria,
                        "precio": precio,
                        "stock": stock,
                        "requiere_receta": requiere_receta,
                        "caducidad": caducidad
                    }
                    datos["inventario"][id_p] = nuevo_prod
                    guardar_datos(datos)
                    st.session_state.datos = datos
                    st.session_state.ultimo_producto_agregado = {**nuevo_prod, "id": id_p}
                    st.rerun()

    with tab3:
        if not datos["inventario"]:
            st.markdown("<div class='alert-warn'><span>⚠️</span> El inventario está vacío.</div>", unsafe_allow_html=True)
        else:
            opciones_inv = {
                f"{id_p} — {info['nombre']} ({info['categoria']})": id_p
                for id_p, info in datos["inventario"].items()
            }
            sel_prod_edit = st.selectbox("Seleccioná el producto a modificar", list(opciones_inv.keys()), key="sel_edit_prod")
            id_prod_edit = opciones_inv[sel_prod_edit]
            prod_edit = datos["inventario"][id_prod_edit]

            st.markdown("<div class='edit-panel'>", unsafe_allow_html=True)
            st.markdown(f"**Editando:** `{id_prod_edit}` — **{prod_edit['nombre']}**")
            st.markdown("<br>", unsafe_allow_html=True)

            with st.form("form_editar_producto"):
                ep1, ep2 = st.columns(2)
                e_p_nombre = ep1.text_input("Nombre del producto *", value=prod_edit["nombre"])
                cats_lista = ["Alimento", "Accesorio", "Fármaco"]
                e_p_cat = ep2.selectbox(
                    "Categoría *",
                    cats_lista,
                    index=cats_lista.index(prod_edit["categoria"]) if prod_edit["categoria"] in cats_lista else 0
                )

                ep3, ep4 = st.columns(2)
                e_p_precio = ep3.number_input(
                    "Precio unitario ($) *",
                    min_value=0.0, step=0.5, format="%.2f",
                    value=float(prod_edit["precio"])
                )
                e_p_stock = ep4.number_input(
                    "Stock actual *",
                    min_value=0, step=1,
                    value=int(prod_edit["stock"])
                )

                e_p_caducidad = st.text_input(
                    "Fecha de caducidad (DD/MM/AAAA)",
                    value=prod_edit.get("caducidad", "N/A"),
                    placeholder="Ej: 31/12/2026 · Dejar N/A si no aplica"
                )

                e_p_receta = False
                if e_p_cat == "Fármaco":
                    e_p_receta = st.checkbox(
                        "¿Requiere receta médica?",
                        value=bool(prod_edit.get("requiere_receta", False))
                    )

                guardar_prod = st.form_submit_button("Guardar cambios", use_container_width=True)
                if guardar_prod:
                    if not e_p_nombre or e_p_precio <= 0:
                        st.markdown("<div class='alert-error'><span>❌</span> Nombre y precio son obligatorios.</div>", unsafe_allow_html=True)
                    else:
                        datos["inventario"][id_prod_edit].update({
                            "nombre": e_p_nombre.strip().title(),
                            "categoria": e_p_cat,
                            "precio": e_p_precio,
                            "stock": e_p_stock,
                            "caducidad": e_p_caducidad.strip() or "N/A",
                            "requiere_receta": e_p_receta,
                        })
                        guardar_datos(datos)
                        st.session_state.datos = datos
                        st.markdown("<div class='alert-success'><span>✅</span> Producto actualizado correctamente.</div>", unsafe_allow_html=True)
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='danger-zone'>", unsafe_allow_html=True)
            st.markdown("<div class='danger-zone-title'>Zona de peligro</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem; margin-bottom:1rem;'>Eliminar el producto <strong>{prod_edit['nombre']}</strong> ({id_prod_edit}) del inventario. Esta acción es irreversible.</p>", unsafe_allow_html=True)

            if st.session_state.confirm_delete_producto == id_prod_edit:
                st.markdown("<div class='alert-error'><span>⚠️</span> ¿Confirmás la eliminación del producto? Esta acción no se puede deshacer.</div>", unsafe_allow_html=True)
                pd1, pd2, pd3 = st.columns([2, 2, 4])
                with pd1:
                    if st.button("Sí, eliminar", key="confirm_del_p"):
                        del datos["inventario"][id_prod_edit]
                        guardar_datos(datos)
                        st.session_state.datos = datos
                        st.session_state.confirm_delete_producto = None
                        st.rerun()
                with pd2:
                    if st.button("Cancelar", key="cancel_del_p"):
                        st.session_state.confirm_delete_producto = None
                        st.rerun()
            else:
                if st.button(f"Eliminar {prod_edit['nombre']}", key="del_prod_btn"):
                    st.session_state.confirm_delete_producto = id_prod_edit
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════
# PÁGINA: PUNTO DE VENTA
# ══════════════════════════════════════════
elif pagina == "💵 Punto de Venta":
    st.markdown("<div class='section-header' style='color:var(--green)'><span>Punto de Venta</span></div>", unsafe_allow_html=True)

    if st.session_state.factura_generada:
        fac = st.session_state.factura_generada
        st.markdown(f"""
        <div class='ticket'>
            <div class='ticket-header'>
                <div style='font-size:1.1rem; font-weight:700; letter-spacing:0.1em; color:var(--violet)'>VETERINARIA & PETSHOP</div>
                <div style='font-size:0.7rem; margin-top:0.3rem; color:var(--muted);'>TICKET DE VENTA</div>
                <div style='margin-top:0.8rem; font-size:0.75rem; color:var(--code-fg)'>
                    Factura: <b>{fac['id']}</b> &nbsp;|&nbsp; {fac['fecha']}<br>
                    Cliente: <b>{fac['cliente']}</b>
                </div>
            </div>
            <div>
                {''.join(f"<div style='display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px dashed #4a4055;'><span>{item['cantidad']}x {item['nombre'][:22]}</span><span style='color:#5ecf8a'>${item['subtotal']:.2f}</span></div>" for item in fac['items'])}
            </div>
            <div class='ticket-total'>
                TOTAL A PAGAR: ${fac['total']:.2f}
            </div>
            <div style='text-align:center; margin-top:1.5rem; font-size:0.7rem; color:var(--muted);'>¡Gracias por su preferencia!</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Nueva Venta", use_container_width=True):
            st.session_state.carrito = []
            st.session_state.total_factura = 0.0
            st.session_state.cliente_pos = ""
            st.session_state.factura_generada = None
            st.session_state.pos_iniciado = False
            st.rerun()

    else:
        if not st.session_state.pos_iniciado:
            st.markdown("""
            <div style='background:white; border:1px solid var(--border); border-radius:4px; padding:1.5rem; max-width:480px; margin-bottom: 1rem;'>
                <div style='font-size:1.1rem; font-weight:700; color:var(--ink); margin-bottom:1rem; font-style:italic;'>Iniciar nueva venta</div>
            """, unsafe_allow_html=True)
            cliente_input = st.text_input("Nombre del cliente", placeholder="Dejar vacío para Público General")
            st.markdown("</div>", unsafe_allow_html=True)
            if st.button("Abrir Caja", use_container_width=False):
                st.session_state.cliente_pos = cliente_input.strip().title() or "Público General"
                st.session_state.pos_iniciado = True
                st.rerun()

        else:
            col_izq, col_der = st.columns([3, 2])

            with col_izq:
                st.markdown(f"**Venta para:** {st.session_state.cliente_pos}")
                st.markdown("<hr style='margin:1rem 0 !important'>", unsafe_allow_html=True)

                with st.expander("➕ Agregar Servicio (Consulta, Vacuna, Baño, etc.)"):
                    with st.form("form_servicio"):
                        desc = st.text_input("Descripción del servicio", placeholder="Ej: Consulta General")
                        precio_serv = st.number_input("Precio ($)", min_value=0.0, step=50.0, format="%.2f")
                        if st.form_submit_button("Agregar servicio"):
                            if desc and precio_serv > 0:
                                st.session_state.carrito.append({
                                    "tipo": "Servicio", "id_prod": "N/A",
                                    "nombre": desc.strip().title(), "cantidad": 1,
                                    "precio": precio_serv, "subtotal": precio_serv,
                                    "id_mascota": None
                                })
                                st.session_state.total_factura += precio_serv
                                st.rerun()
                            else:
                                st.error("Completá descripción y precio.")

                with st.expander("📦 Agregar Producto del Inventario"):
                    if not datos["inventario"]:
                        st.warning("Inventario vacío.")
                    else:
                        with st.form("form_producto_pos"):
                            opciones_prod = {
                                f"{id_p} — {info['nombre']} (${info['precio']:.2f} | Stock: {info['stock']})": id_p
                                for id_p, info in datos["inventario"].items() if info["stock"] > 0
                            }
                            if not opciones_prod:
                                st.warning("Sin stock disponible.")
                                st.form_submit_button("Agregar", disabled=True)
                            else:
                                sel_prod = st.selectbox("Producto", list(opciones_prod.keys()))
                                id_prod_sel = opciones_prod[sel_prod]
                                prod = datos["inventario"][id_prod_sel]
                                cant = st.number_input("Cantidad", min_value=1, max_value=prod["stock"], step=1, value=1)

                                id_paciente_fijo = None
                                if prod.get("requiere_receta", False):
                                    st.markdown("<div class='alert-warn'><span>⚠️</span> Fármaco controlado — requiere receta</div>", unsafe_allow_html=True)
                                    opciones_pac = {f"{id_m} — {i['nombre']}": id_m for id_m, i in datos["mascotas"].items()}
                                    if opciones_pac:
                                        sel_pac = st.selectbox("Paciente con receta", list(opciones_pac.keys()))
                                        id_paciente_fijo = opciones_pac[sel_pac]
                                    else:
                                        st.error("Sin pacientes registrados. Venta bloqueada.")
                                        st.form_submit_button("Agregar", disabled=True)
                                        st.stop()

                                if st.form_submit_button("Agregar al carrito"):
                                    en_carrito = sum(i["cantidad"] for i in st.session_state.carrito if i.get("id_prod") == id_prod_sel)
                                    if (cant + en_carrito) > prod["stock"]:
                                        st.error("Stock insuficiente.")
                                    else:
                                        subt = cant * prod["precio"]
                                        st.session_state.carrito.append({
                                            "tipo": "Producto", "id_prod": id_prod_sel,
                                            "nombre": prod["nombre"], "cantidad": cant,
                                            "precio": prod["precio"], "subtotal": subt,
                                            "id_mascota": id_paciente_fijo
                                        })
                                        st.session_state.total_factura += subt
                                        st.rerun()

            with col_der:
                st.markdown("**Carrito actual**")
                if not st.session_state.carrito:
                    st.markdown("<div class='alert-warn' style='font-size:0.82rem;'>El carrito está vacío.</div>", unsafe_allow_html=True)
                else:
                    for i, item in enumerate(st.session_state.carrito):
                        st.markdown(f"""
                        <div class='cart-item'>
                            <div>
                                <div class='cart-item-name'>{item['nombre']}</div>
                                <div class='cart-item-qty'>{item['cantidad']}x · ${item['precio']:.2f} c/u</div>
                            </div>
                            <div class='cart-item-price'>${item['subtotal']:.2f}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button("Quitar último ítem"):
                        ultimo = st.session_state.carrito.pop()
                        st.session_state.total_factura -= ultimo["subtotal"]
                        st.rerun()

                    st.markdown(f"""
                    <div class='total-bar'>
                        <div>
                            <div class='total-label'>Total a pagar</div>
                        </div>
                        <div class='total-amount'>${st.session_state.total_factura:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Cancelar Venta", use_container_width=True):
                            st.session_state.carrito = []
                            st.session_state.total_factura = 0.0
                            st.session_state.cliente_pos = ""
                            st.session_state.pos_iniciado = False
                            st.rerun()
                    with c2:
                        if st.button("Procesar Pago", use_container_width=True):
                            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
                            for item in st.session_state.carrito:
                                if item["tipo"] == "Producto":
                                    datos["inventario"][item["id_prod"]]["stock"] -= item["cantidad"]
                                    if item["id_mascota"]:
                                        datos["mascotas"][item["id_mascota"]]["historial"].append({
                                            "fecha": fecha_actual,
                                            "motivo": "Despacho en Farmacia",
                                            "diagnostico": "N/A",
                                            "tratamiento": f"Se suministró: {item['cantidad']}x {item['nombre']}"
                                        })
                            id_fac = generar_id_factura(datos)
                            factura = {
                                "id": id_fac,
                                "fecha": fecha_actual,
                                "cliente": st.session_state.cliente_pos,
                                "items": list(st.session_state.carrito),
                                "total": st.session_state.total_factura
                            }
                            datos["facturas"].append(factura)
                            guardar_datos(datos)
                            st.session_state.datos = datos
                            st.session_state.factura_generada = factura
                            st.rerun()


# ══════════════════════════════════════════
# PÁGINA: FACTURAS
# ══════════════════════════════════════════
elif pagina == "📊 Facturas":
    st.markdown("<div class='section-header' style='color:var(--ink)'><span>Historial de Facturación</span></div>", unsafe_allow_html=True)

    if not datos["facturas"]:
        st.markdown("<div class='alert-warn'><span>⚠️</span> No hay facturas registradas aún.</div>", unsafe_allow_html=True)
    else:
        gran_total = sum(f["total"] for f in datos["facturas"])
        promedio = gran_total / len(datos["facturas"])

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"""<div class='stat-card'><div class='stat-num'>{len(datos['facturas'])}</div><div class='stat-label'>Total facturas</div></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class='stat-card'><div class='stat-num'>${gran_total:,.2f}</div><div class='stat-label'>Ingresos totales</div></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class='stat-card'><div class='stat-num'>${promedio:,.2f}</div><div class='stat-label'>Ticket promedio</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        filas = "".join(
            f"""<tr>
                <td><code>{f['id']}</code></td>
                <td>{f['fecha'][:10]}</td>
                <td>{f['fecha'][11:16]}</td>
                <td><b>{f['cliente']}</b></td>
                <td><span class='badge badge-gray'>{len(f['items'])} ítems</span></td>
                <td style='color:var(--green); font-weight:bold;'>${f['total']:.2f}</td>
            </tr>"""
            for f in reversed(datos["facturas"])
        )
        st.markdown(f"""
        <table class='vet-table'>
            <thead><tr><th>ID</th><th>Fecha</th><th>Hora</th><th>Cliente</th><th>Ítems</th><th>Total</th></tr></thead>
            <tbody>{filas}</tbody>
        </table>""", unsafe_allow_html=True)

        st.markdown("<br><div class='section-header'><span>Detalle de factura</span></div>", unsafe_allow_html=True)
        opciones_fac = {f["id"]: f for f in datos["facturas"]}
        fac_id_sel = st.selectbox("Seleccioná una factura para ver el detalle", list(reversed(list(opciones_fac.keys()))))
        fac_det = opciones_fac[fac_id_sel]

        items_html = "".join(
            f"<div style='display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px dashed #4a4055;'><span>{i['cantidad']}x {i['nombre'][:24]}</span><span style='color:#5ecf8a;'>${i['subtotal']:.2f}</span></div>"
            for i in fac_det["items"]
        )
        st.markdown(f"""
        <div class='ticket'>
            <div class='ticket-header'>
                <div style='font-size:1.1rem; font-weight:700; letter-spacing:0.1em; color:var(--violet)'>VETERINARIA & PETSHOP</div>
                <div style='font-size:0.7rem; margin-top:0.3rem; color:var(--muted);'>COMPROBANTE DE VENTA</div>
                <div style='margin-top:0.8rem; font-size:0.75rem; color:var(--code-fg)'>
                    Factura: <b>{fac_det['id']}</b> &nbsp;|&nbsp; {fac_det['fecha']}<br>
                    Cliente: <b>{fac_det['cliente']}</b>
                </div>
            </div>
            {items_html}
            <div class='ticket-total'>TOTAL: ${fac_det['total']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)