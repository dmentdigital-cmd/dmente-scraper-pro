"""
╔══════════════════════════════════════════════════════════════╗
║   🧠 DMENTE DIGITAL - Herramienta Profesional de Scraping   ║
║   "No es azar, es propósito"                                ║
║   Interfaz Streamlit v3.0 — Con Login + Multi-Descarga      ║
╚══════════════════════════════════════════════════════════════╝

Ejecutar: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import time
import hashlib
import json
import os
from datetime import datetime

from engine.scraper import (
    DmenteScrapingEngine,
    ScrapingConfig,
    EngineType,
    ScrapingMode,
    get_csv_download,
    get_excel_download,
    get_json_download,
)

# ─── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="Dmente Scraper Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── USER DATABASE (file-based for persistence) ──────────────
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

DEFAULT_USERS = {
    "admin": {
        "password_hash": "0eb618c9e2378f5c465097a404c09cf49572248726a4c31d056e1d985960a14a",
        "name": "Administrador Dmente",
        "role": "admin",
    },
    "dmente": {
        "password_hash": "214b68aa9a10d92646a85024ab3fad096fe032dfbcaded68259275d893a5aa91",
        "name": "Operador Dmente",
        "role": "user",
    },
}


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # First run: create default users
    save_users(DEFAULT_USERS)
    return DEFAULT_USERS


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def verify_password(username, password):
    users = load_users()
    if username not in users:
        return False
    stored_hash = users[username]["password_hash"]
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()


def get_user_info(username):
    users = load_users()
    return users.get(username, {})


def add_user(username, password, name, role="user"):
    users = load_users()
    users[username] = {
        "password_hash": hashlib.sha256(password.encode()).hexdigest(),
        "name": name,
        "role": role,
    }
    save_users(users)


# ─── SCRAPING HISTORY (file-based) ───────────────────────────
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "scraping_history.json")


def save_scraping_record(user, url, items, engine, duration, filename):
    history = load_history()
    history.append({
        "user": user,
        "url": url,
        "items": items,
        "engine": engine,
        "duration": duration,
        "filename": filename,
        "timestamp": datetime.now().isoformat(),
    })
    # Keep last 100 records
    history = history[-100:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ─── FULL CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    *, html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(160deg, #061421 0%, #0a1c2e 40%, #0d2137 70%, #061421 100%) !important;
    }

    /* ── Login Page ── */
    .login-container {
        max-width: 420px;
        margin: 8vh auto;
        background: rgba(43,235,210,0.03);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(43,235,210,0.12);
        border-radius: 24px;
        padding: 2.5rem;
        position: relative;
        overflow: hidden;
    }
    .login-container::before {
        content: '';
        position: absolute;
        top: -60%;
        left: -30%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(43,235,210,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .login-container::after {
        content: '';
        position: absolute;
        bottom: -40%;
        right: -30%;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(236,72,153,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .login-logo {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .login-title {
        font-size: 1.6rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #2bebd2 0%, #089ca0 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }
    .login-subtitle {
        text-align: center;
        color: rgba(248,250,252,0.4);
        font-size: 0.8rem;
        margin-bottom: 2rem;
    }

    /* ── Hero Header ── */
    .hero-container {
        background: linear-gradient(135deg, rgba(43,235,210,0.08) 0%, rgba(21,99,103,0.12) 50%, rgba(236,72,153,0.06) 100%);
        border: 1px solid rgba(43,235,210,0.15);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(43,235,210,0.06) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2bebd2 0%, #089ca0 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin: 0;
        line-height: 1.1;
    }
    .hero-subtitle {
        color: rgba(248,250,252,0.6);
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 0.4rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(43,235,210,0.12);
        border: 1px solid rgba(43,235,210,0.3);
        color: #2bebd2;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .hero-user {
        position: absolute;
        top: 1.5rem;
        right: 2rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .user-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2bebd2, #EC4899);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        color: #061421;
    }
    .user-name {
        color: rgba(248,250,252,0.8);
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* ── Glass Cards ── */
    .glass-card {
        background: rgba(43,235,210,0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(248,250,252,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(43,235,210,0.2);
        box-shadow: 0 8px 32px rgba(43,235,210,0.06);
    }
    .glass-card h3 {
        color: #2bebd2 !important;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }

    /* ── Console ── */
    .console-container {
        background: rgba(6,20,33,0.95);
        border: 1px solid rgba(43,235,210,0.15);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem;
        line-height: 1.7;
        max-height: 350px;
        overflow-y: auto;
        color: rgba(248,250,252,0.85);
        margin-bottom: 1rem;
    }
    .console-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    .console-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    .dot-red { background: #ff5f57; }
    .dot-yellow { background: #febc2e; }
    .dot-green { background: #28c840; }
    .log-line {
        padding: 0.15rem 0;
        border-bottom: 1px solid rgba(248,250,252,0.03);
    }

    /* ── Stats ── */
    .stat-card {
        background: linear-gradient(135deg, rgba(43,235,210,0.06) 0%, rgba(8,156,160,0.04) 100%);
        border: 1px solid rgba(43,235,210,0.12);
        border-radius: 14px;
        padding: 1.1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(43,235,210,0.3);
        box-shadow: 0 8px 24px rgba(43,235,210,0.08);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2bebd2, #089ca0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        color: rgba(248,250,252,0.5);
        font-size: 0.7rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.2rem;
    }

    .status-idle { color: rgba(248,250,252,0.4); }
    .status-running { color: #2bebd2; }
    .status-success { color: #28c840; }
    .status-error { color: #ff5f57; }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 5px rgba(43,235,210,0.3); }
        50% { box-shadow: 0 0 20px rgba(43,235,210,0.5); }
    }
    .pulse-active { animation: pulse-glow 2s ease-in-out infinite; }

    /* ── Download Cards ── */
    .dl-card {
        background: rgba(43,235,210,0.03);
        border: 1px solid rgba(248,250,252,0.08);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .dl-card:hover {
        border-color: rgba(43,235,210,0.2);
        box-shadow: 0 4px 16px rgba(43,235,210,0.06);
    }
    .dl-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .dl-title {
        color: #2bebd2;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .dl-desc {
        color: rgba(248,250,252,0.4);
        font-size: 0.72rem;
        line-height: 1.4;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071a2b 0%, #0a1e30 100%) !important;
        border-right: 1px solid rgba(43,235,210,0.08) !important;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #2bebd2 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #2bebd2 0%, #089ca0 100%) !important;
        color: #061421 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-size: 0.85rem !important;
        letter-spacing: -0.01em !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(43,235,210,0.3) !important;
    }
    .stop-btn > button {
        background: linear-gradient(135deg, #ff5f57 0%, #d43f3a 100%) !important;
        color: #fff !important;
    }
    .clear-btn > button {
        background: linear-gradient(135deg, rgba(248,250,252,0.1) 0%, rgba(248,250,252,0.05) 100%) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(248,250,252,0.15) !important;
    }
    .logout-btn > button {
        background: transparent !important;
        color: rgba(248,250,252,0.5) !important;
        border: 1px solid rgba(248,250,252,0.1) !important;
        font-size: 0.75rem !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #156367 0%, #089ca0 100%) !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
    }

    /* ── DataFrames ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(43,235,210,0.12) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: rgba(6,20,33,0.8) !important;
        border: 1px solid rgba(43,235,210,0.15) !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2bebd2 !important;
        box-shadow: 0 0 0 2px rgba(43,235,210,0.15) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(6,20,33,0.5);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: rgba(248,250,252,0.5) !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(43,235,210,0.1) !important;
        color: #2bebd2 !important;
    }

    /* ── Footer ── */
    .dm-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(43,235,210,0.08);
    }
    .dm-footer a { text-decoration: none !important; color: inherit !important; }
    .dm-dev { color: rgba(248,250,252,0.4); font-size: 0.8rem; display: block; }
    .dm-name { color: #2bebd2; font-weight: 700; }
    .dm-lema {
        color: rgba(248,250,252,0.25);
        font-size: 0.7rem;
        font-style: italic;
        display: block;
        margin-top: 0.25rem;
    }

    /* hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE ────────────────────────────────────────────
def init_state():
    defaults = {
        "authenticated": False,
        "username": "",
        "user_info": {},
        "logs": [],
        "result": None,
        "is_running": False,
        "engine_instance": None,
        "run_count": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


def add_log(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")


# ═══════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ═══════════════════════════════════════════════════════════════
def render_login_page():
    # Center the login form
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">🧠</div>
            <div class="login-title">Dmente Scraper Pro</div>
            <div class="login-subtitle">Ingresa tus credenciales para continuar</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.markdown("##### 👤 Usuario")
            username = st.text_input(
                "Usuario",
                placeholder="Tu nombre de usuario",
                label_visibility="collapsed",
                key="login_user",
            )
            st.markdown("##### 🔒 Contraseña")
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Tu contraseña",
                label_visibility="collapsed",
                key="login_pass",
            )

            submitted = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)

            if submitted:
                if verify_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_info = get_user_info(username)
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")

        # Default credentials hint
        with st.expander("💡 Credenciales por defecto"):
            st.markdown("""
            | Usuario | Contraseña | Rol |
            |---------|-----------|-----|
            | `admin` | `DmenteDigital2026!` | Administrador |
            | `dmente` | `scraper2026` | Operador |
            """)

        st.markdown("""
        <footer class="dm-footer" style="margin-top:2rem; border:none;">
            <a href="http://dmentedigital.co/" target="_blank">
                <span class="dm-dev">Desarrollado por <span class="dm-name">Dmente Digital</span></span>
                <span class="dm-lema">No es azar, es propósito</span>
            </a>
        </footer>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  MAIN APP (After Login)
# ═══════════════════════════════════════════════════════════════
def render_main_app():
    user_info = st.session_state.user_info
    user_initial = user_info.get("name", "U")[0].upper()

    # ─── HERO HEADER ──────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-badge">⚡ Ingeniería de Crecimiento Digital</div>
        <h1 class="hero-title">🧠 Dmente Scraper Pro</h1>
        <p class="hero-subtitle">
            Herramienta profesional de extracción de datos web — Selenium · Playwright · BeautifulSoup
        </p>
        <div class="hero-user">
            <div>
                <span class="user-name">👋 {user_info.get('name', st.session_state.username)}</span>
            </div>
            <div class="user-avatar">{user_initial}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Panel de Control")

        # Logout button
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.user_info = {}
            st.session_state.logs = []
            st.session_state.result = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # URL Input
        st.markdown("##### 🌐 URL Objetivo")
        url = st.text_input(
            "URL", value="http://quotes.toscrape.com/scroll",
            label_visibility="collapsed", placeholder="https://ejemplo.com",
        )

        st.markdown("---")

        # Engine
        st.markdown("##### 🔧 Motor de Scraping")
        engine_map = {
            "🎭 Playwright (Recomendado)": EngineType.PLAYWRIGHT,
            "🌐 Selenium + WebDriver": EngineType.SELENIUM,
            "📄 Requests + BS4 (Estático)": EngineType.REQUESTS_BS4,
        }
        engine_choice = st.selectbox("Motor", list(engine_map.keys()), 0, label_visibility="collapsed")
        selected_engine = engine_map[engine_choice]

        # Mode
        st.markdown("##### 📋 Modo de Operación")
        mode_map = {
            "📜 Scroll Infinito": ScrapingMode.DYNAMIC_SCROLL,
            "🔐 Login + Extracción": ScrapingMode.DYNAMIC_LOGIN,
            "📄 Página Estática": ScrapingMode.STATIC,
            "📚 Paginación Múltiple": ScrapingMode.PAGINATION,
        }
        mode_choice = st.selectbox("Modo", list(mode_map.keys()), 0, label_visibility="collapsed")
        selected_mode = mode_map[mode_choice]

        st.markdown("---")
        st.markdown("##### 🧭 Navegación")

        col1, col2 = st.columns(2)
        with col1:
            headless = st.toggle("Segundo Plano", value=True)
        with col2:
            st.caption("👻 Headless" if headless else "👁️ Visible")

        scroll_depth = 3
        scroll_pause = 5.0
        max_pages = 3

        if selected_mode == ScrapingMode.DYNAMIC_SCROLL:
            scroll_depth = st.slider("Profundidad de Scroll", 1, 20, 5)
            scroll_pause = st.slider("Pausa entre Scrolls (seg)", 1.0, 15.0, 5.0, 0.5)

        if selected_mode == ScrapingMode.PAGINATION:
            st.markdown("---")
            st.markdown("##### 📚 Paginación")
            st.caption("Usa `{}` en la URL como placeholder de número de página")
            max_pages = st.number_input("Páginas", 1, 100, 3)

        login_user = login_pass = ""
        user_selector = "#username"
        pass_selector = "#password"
        submit_selector = "input[type='submit']"

        if selected_mode == ScrapingMode.DYNAMIC_LOGIN:
            st.markdown("---")
            st.markdown("##### 🔐 Credenciales del Sitio")
            login_user = st.text_input("Usuario Sitio", value="platzi-admin")
            login_pass = st.text_input("Contraseña Sitio", value="12345", type="password")
            user_selector = st.text_input("Selector Usuario", value="#username")
            pass_selector = st.text_input("Selector Contraseña", value="#password")
            submit_selector = st.text_input("Selector Submit", value="input[type='submit']")

        st.markdown("---")
        with st.expander("🎯 Selector CSS Personalizado"):
            css_selector = st.text_input(
                "CSS Selector", value="",
                placeholder="div.quote, article.product_pod",
                help="Dejar vacío para auto-detección",
            )

        # Admin: manage users
        if user_info.get("role") == "admin":
            st.markdown("---")
            with st.expander("👥 Gestión de Usuarios (Admin)"):
                st.markdown("##### Crear Nuevo Usuario")
                new_user = st.text_input("Nuevo usuario", key="new_user_input")
                new_pass = st.text_input("Nueva contraseña", type="password", key="new_pass_input")
                new_name = st.text_input("Nombre completo", key="new_name_input")
                new_role = st.selectbox("Rol", ["user", "admin"], key="new_role_input")
                if st.button("➕ Crear Usuario", key="create_user_btn"):
                    if new_user and new_pass and new_name:
                        add_user(new_user, new_pass, new_name, new_role)
                        st.success(f"✅ Usuario '{new_user}' creado")
                    else:
                        st.warning("Completa todos los campos")

                st.markdown("##### Usuarios Registrados")
                users = load_users()
                for u, info in users.items():
                    st.caption(f"• **{u}** — {info.get('name', '')} ({info.get('role', 'user')})")

        st.markdown("""
        <div style="text-align:center; padding:1rem 0; opacity:0.3;">
            <small>v3.0 · Producción</small><br>
            <small>Python 3.12 · Dmente Digital</small>
        </div>
        """, unsafe_allow_html=True)

    # ─── ACTION BUTTONS ───────────────────────────────────────
    col_btn1, col_btn2, col_btn3, col_spacer = st.columns([2, 1.5, 1.5, 5])

    with col_btn1:
        start_clicked = st.button("🚀 Iniciar Scraping", use_container_width=True,
                                  disabled=st.session_state.is_running)
    with col_btn2:
        st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
        stop_clicked = st.button("🛑 Detener", use_container_width=True,
                                 disabled=not st.session_state.is_running)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_btn3:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        clear_clicked = st.button("🗑️ Limpiar", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle actions
    if clear_clicked:
        st.session_state.logs = []
        st.session_state.result = None
        st.session_state.is_running = False
        st.rerun()

    if stop_clicked and st.session_state.engine_instance:
        st.session_state.engine_instance.stop()

    if start_clicked and not st.session_state.is_running:
        st.session_state.logs = []
        st.session_state.result = None
        st.session_state.is_running = True
        st.session_state.run_count += 1

        config = ScrapingConfig(
            url=url, engine=selected_engine, mode=selected_mode,
            headless=headless, scroll_depth=scroll_depth,
            scroll_pause=scroll_pause, max_pages=max_pages,
            css_selector=css_selector, username=login_user,
            password=login_pass, username_selector=user_selector,
            password_selector=pass_selector, submit_selector=submit_selector,
        )

        add_log("━━━ DMENTE SCRAPER PRO ━━━")
        add_log(f"Operador: {st.session_state.user_info.get('name', st.session_state.username)}")
        add_log(f"Motor: {config.engine.value}")
        add_log(f"Modo: {config.mode.value}")
        add_log(f"URL: {config.url}")

        engine = DmenteScrapingEngine(config, log_callback=add_log)
        st.session_state.engine_instance = engine

        with st.spinner("🧠 Procesando... Los datos se cargarán automáticamente."):
            result = engine.run()

        st.session_state.result = result
        st.session_state.is_running = False
        st.session_state.engine_instance = None

        # Save to history
        if result.success:
            save_scraping_record(
                user=st.session_state.username,
                url=url,
                items=result.total_items,
                engine=result.engine_used,
                duration=result.duration_seconds,
                filename=f"scraping_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            )

        st.rerun()

    # ─── STATS ROW ────────────────────────────────────────────
    result = st.session_state.result

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    with col_s1:
        if st.session_state.is_running:
            status = '<span class="status-running">● EJECUTANDO</span>'
        elif result and result.success:
            status = '<span class="status-success">● COMPLETADO</span>'
        elif result and not result.success:
            status = '<span class="status-error">● ERROR</span>'
        else:
            status = '<span class="status-idle">● EN ESPERA</span>'
        st.markdown(f"""
        <div class="stat-card {'pulse-active' if st.session_state.is_running else ''}">
            <div style="font-size:1.1rem; font-weight:700;">{status}</div>
            <div class="stat-label">Estado</div>
        </div>""", unsafe_allow_html=True)

    with col_s2:
        items = result.total_items if result else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{items}</div>
            <div class="stat-label">Items Extraídos</div>
        </div>""", unsafe_allow_html=True)

    with col_s3:
        duration = result.duration_seconds if result else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{duration}s</div>
            <div class="stat-label">Duración</div>
        </div>""", unsafe_allow_html=True)

    with col_s4:
        errors = len(result.errors) if result else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{errors}</div>
            <div class="stat-label">Errores</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ─── TABS ─────────────────────────────────────────────────
    tab_console, tab_data, tab_download, tab_history = st.tabs([
        "🖥️ Consola de Estado",
        "📊 Tabla de Resultados",
        "💾 Descargar Datos",
        "📜 Historial",
    ])

    # TAB: Console
    with tab_console:
        st.markdown("""
        <div class="console-container">
            <div class="console-header">
                <span class="console-dot dot-red"></span>
                <span class="console-dot dot-yellow"></span>
                <span class="console-dot dot-green"></span>
                <span style="color:rgba(248,250,252,0.4); font-size:0.65rem; margin-left:0.5rem;
                             font-family:'JetBrains Mono',monospace;">dmente-scraper-pro</span>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.logs:
            log_html = ""
            for log in st.session_state.logs:
                if "❌" in log or "Error" in log:
                    color = "#ff5f57"
                elif "✅" in log or "exitoso" in log.lower() or "completado" in log.lower():
                    color = "#28c840"
                elif "⚠️" in log:
                    color = "#febc2e"
                elif "🚀" in log or "📜" in log:
                    color = "#2bebd2"
                elif "⏱️" in log or "⏳" in log:
                    color = "rgba(248,250,252,0.4)"
                else:
                    color = "rgba(248,250,252,0.7)"
                log_html += f'<div class="log-line" style="color:{color};">{log}</div>'
            st.markdown(log_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="color:rgba(248,250,252,0.3); font-family:'JetBrains Mono',monospace;">
                Esperando instrucciones...<br>
                Configura los parámetros y presiona "🚀 Iniciar Scraping"
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB: Results Table
    with tab_data:
        if result and result.data:
            df = pd.DataFrame(result.data)
            st.markdown(f"""
            <div class="glass-card">
                <h3>📊 Vista Previa — {len(df)} registros × {len(df.columns)} columnas</h3>
            </div>""", unsafe_allow_html=True)

            # Column filter
            cols_to_show = st.multiselect(
                "Columnas a mostrar",
                options=df.columns.tolist(),
                default=df.columns.tolist(),
                key="col_filter",
            )

            # Search filter
            search = st.text_input("🔍 Buscar en resultados", placeholder="Filtrar por texto...", key="search_filter")

            display_df = df[cols_to_show] if cols_to_show else df
            if search:
                mask = display_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
                display_df = display_df[mask]
                st.caption(f"Mostrando {len(display_df)} de {len(df)} resultados")

            st.dataframe(display_df, use_container_width=True, height=450)

            with st.expander("📈 Estadísticas Rápidas"):
                st.write(df.describe(include="all").fillna("—"))
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:3rem;">
                <div style="font-size:3rem; margin-bottom:1rem;">📭</div>
                <h3 style="color:rgba(248,250,252,0.5) !important;">Sin datos aún</h3>
                <p style="color:rgba(248,250,252,0.3);">
                    Ejecuta un scraping para ver los resultados aquí
                </p>
            </div>""", unsafe_allow_html=True)

    # TAB: Downloads (CSV, Excel, JSON)
    with tab_download:
        if result and result.data:
            st.markdown("""
            <div class="glass-card">
                <h3>💾 Exportar Resultados en Múltiples Formatos</h3>
            </div>""", unsafe_allow_html=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            col_d1, col_d2, col_d3 = st.columns(3)

            with col_d1:
                st.markdown("""
                <div class="dl-card">
                    <div class="dl-icon">📄</div>
                    <div class="dl-title">CSV</div>
                    <div class="dl-desc">Universal. Compatible con Excel, Google Sheets, Power BI, etc.</div>
                </div>""", unsafe_allow_html=True)
                csv_data = get_csv_download(result.data)
                st.download_button(
                    "⬇️ Descargar CSV",
                    data=csv_data,
                    file_name=f"dmente_scraping_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col_d2:
                st.markdown("""
                <div class="dl-card">
                    <div class="dl-icon">📊</div>
                    <div class="dl-title">EXCEL</div>
                    <div class="dl-desc">Formato .xlsx nativo con soporte para filtros y formato avanzado.</div>
                </div>""", unsafe_allow_html=True)
                excel_data = get_excel_download(result.data)
                st.download_button(
                    "⬇️ Descargar Excel",
                    data=excel_data,
                    file_name=f"dmente_scraping_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

            with col_d3:
                st.markdown("""
                <div class="dl-card">
                    <div class="dl-icon">🔗</div>
                    <div class="dl-title">JSON</div>
                    <div class="dl-desc">Formato estructurado ideal para APIs, programadores y automatizaciones.</div>
                </div>""", unsafe_allow_html=True)
                json_data = get_json_download(result.data)
                st.download_button(
                    "⬇️ Descargar JSON",
                    data=json_data,
                    file_name=f"dmente_scraping_{timestamp}.json",
                    mime="application/json",
                    use_container_width=True,
                )

            # Error details
            if result.errors:
                with st.expander("⚠️ Detalle de Errores"):
                    for err in result.errors:
                        st.error(err)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:3rem;">
                <div style="font-size:3rem; margin-bottom:1rem;">💾</div>
                <h3 style="color:rgba(248,250,252,0.5) !important;">Nada que descargar</h3>
                <p style="color:rgba(248,250,252,0.3);">
                    Los botones de descarga aparecerán cuando haya datos
                </p>
            </div>""", unsafe_allow_html=True)

    # TAB: History
    with tab_history:
        history = load_history()
        if history:
            st.markdown("""
            <div class="glass-card">
                <h3>📜 Historial de Ejecuciones</h3>
            </div>""", unsafe_allow_html=True)

            history_data = []
            for h in reversed(history):
                history_data.append({
                    "Fecha": h.get("timestamp", "")[:19].replace("T", " "),
                    "Usuario": h.get("user", ""),
                    "URL": h.get("url", "")[:60] + ("..." if len(h.get("url", "")) > 60 else ""),
                    "Items": h.get("items", 0),
                    "Motor": h.get("engine", ""),
                    "Duración": f"{h.get('duration', 0)}s",
                })

            st.dataframe(pd.DataFrame(history_data), use_container_width=True, height=350)
        else:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:3rem;">
                <div style="font-size:3rem; margin-bottom:1rem;">📜</div>
                <h3 style="color:rgba(248,250,252,0.5) !important;">Sin historial</h3>
                <p style="color:rgba(248,250,252,0.3);">
                    El historial de ejecuciones aparecerá aquí
                </p>
            </div>""", unsafe_allow_html=True)

    # ─── FOOTER ───────────────────────────────────────────────
    st.markdown("""
    <footer class="dm-footer">
        <a href="http://dmentedigital.co/" target="_blank">
            <span class="dm-dev">Desarrollado por <span class="dm-name">Dmente Digital</span></span>
            <span class="dm-lema">No es azar, es propósito</span>
        </a>
    </footer>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════════════
if st.session_state.authenticated:
    render_main_app()
else:
    render_login_page()
