import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import uuid
from sheets import (
    authenticate_user, get_all_reports, get_user_reports,
    submit_report, update_report, get_all_users,
    add_user, delete_user, update_password, get_report_by_id
)

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DAR Portal",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Force theme independence ──────────────────────────────────────────────────
st.markdown("""
<meta name="color-scheme" content="light only">
<style>
:root, html, body, .stApp {
    color-scheme: light only !important;
}
</style>
""", unsafe_allow_html=True)

# Hide Streamlit header
st.markdown("""
<style>
header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*, *::before, *::after { color-scheme: light only !important; }

html, body {
    background-color: #0f1117 !important;
    color: #f0f0f5 !important;
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background-color: #0f1117 !important;
    color: #f0f0f5 !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.stDeployButton { display: none; }

[data-testid="stSidebar"] {
    background-color: #1a1d2e !important;
    border-right: 1px solid rgba(108,99,255,0.2) !important;
}
[data-testid="stSidebar"] * { color: #f0f0f5 !important; }
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #f0f0f5 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.main .block-container {
    background-color: #0f1117 !important;
    color: #f0f0f5 !important;
}

p, li, td, th { color: #f0f0f5 !important; }
/* Note: span and div are intentionally excluded here to avoid overriding
   widget internals like time/date pickers */
h1, h2, h3, h4, h5, h6 {
    color: #f0f0f5 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.dar-card {
    background-color: #1a1d2e !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 12px !important;
    padding: 24px !important;
    margin-bottom: 16px !important;
}
.dar-card-glow {
    background-color: #1a1d2e !important;
    border: 1px solid #6c63ff !important;
    border-radius: 12px !important;
    padding: 24px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 0 20px rgba(108,99,255,0.15) !important;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}
.metric-card {
    background-color: #1a1d2e !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    text-align: center !important;
    transition: border-color 0.2s !important;
}
.metric-card:hover { border-color: #6c63ff !important; }
.metric-value {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #8b85ff !important;
    line-height: 1 !important;
    margin-bottom: 6px !important;
}
.metric-label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: #9b9bb4 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

.page-header {
    margin-bottom: 28px !important;
    padding-bottom: 20px !important;
    border-bottom: 1px solid rgba(108,99,255,0.2) !important;
}
.page-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: #f0f0f5 !important;
    margin: 0 0 4px 0 !important;
}
.page-subtitle {
    font-size: 0.9rem !important;
    color: #9b9bb4 !important;
    margin: 0 !important;
}

.badge {
    display: inline-block !important;
    padding: 3px 10px !important;
    border-radius: 20px !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}
.badge-submitted { background-color: rgba(34,197,94,0.15) !important;  color: #22c55e !important; }
.badge-progress  { background-color: rgba(59,130,246,0.15) !important;  color: #3b82f6 !important; }
.badge-pending   { background-color: rgba(245,158,11,0.15) !important;  color: #f59e0b !important; }
.badge-leave     { background-color: rgba(168,85,247,0.15) !important;  color: #a855f7 !important; }
.badge-holiday   { background-color: rgba(236,72,153,0.15) !important;  color: #ec4899 !important; }
.badge-correction{ background-color: rgba(239,68,68,0.15)  !important;  color: #ef4444 !important; }

.login-wrapper { max-width: 420px; margin: 60px auto 0; }
.login-logo { text-align: center; margin-bottom: 36px; }
.login-logo-icon { font-size: 3rem; display: block; margin-bottom: 12px; }
.login-logo-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: #f0f0f5 !important;
}
.login-logo-sub { font-size: 0.85rem !important; color: #9b9bb4 !important; margin-top: 4px !important; }

.alert-success {
    background-color: rgba(34,197,94,0.1) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    color: #22c55e !important;
    font-size: 0.875rem !important;
    margin-bottom: 16px !important;
}
.alert-error {
    background-color: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    color: #ef4444 !important;
    font-size: 0.875rem !important;
    margin-bottom: 16px !important;
}

.nav-user-info {
    background-color: rgba(108,99,255,0.15) !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
    margin-bottom: 20px !important;
}
.nav-username {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    color: #f0f0f5 !important;
    font-size: 1rem !important;
}
.nav-role {
    font-size: 0.75rem !important;
    color: #8b85ff !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

.section-divider {
    height: 1px !important;
    background-color: rgba(108,99,255,0.2) !important;
    margin: 24px 0 !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background-color: #252836 !important;
    color: #f0f0f5 !important;
    border-color: rgba(108,99,255,0.2) !important;
    border-radius: 8px !important;
    caret-color: #f0f0f5 !important;
}
/* ── Time inputs — white bg, black text ── */
/* st.time_input renders as a select/dropdown internally */
[data-testid="stTimeInput"] > div,
[data-testid="stTimeInput"] > div > div,
[data-testid="stTimeInput"] [data-baseweb="select"] > div,
[data-testid="stTimeInput"] [data-baseweb="select"] > div > div,
[data-testid="stTimeInput"] [data-baseweb="base-input"],
[data-testid="stTimeInput"] [data-baseweb="base-input"] > div,
[data-testid="stTimeInput"] input,
[data-testid="stTimeInput"] [role="combobox"],
[data-testid="stTimeInput"] [role="combobox"] > div,
[data-testid="stTimeInput"] span,
.stTimeInput [data-baseweb="select"] > div,
.stTimeInput [data-baseweb="select"] > div > div {
    background-color: #ffffff !important;
    color: #111111 !important;
    caret-color: #111111 !important;
}
/* The visible text value inside the time dropdown */
[data-testid="stTimeInput"] [data-baseweb="select"] [data-id="select"],
[data-testid="stTimeInput"] [data-baseweb="select"] div[class*="ValueContainer"] *,
[data-testid="stTimeInput"] [data-baseweb="select"] div[class*="singleValue"],
[data-testid="stTimeInput"] [data-baseweb="select"] div[class*="placeholder"] {
    color: #111111 !important;
    background-color: #ffffff !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color: #6b6b80 !important; }
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
    outline: none !important;
}

/* ── Selectbox trigger (closed state) — keep dark ── */
.stSelectbox > div > div {
    background-color: #252836 !important;
    border-color: rgba(108,99,255,0.2) !important;
    border-radius: 8px !important;
    color: #f0f0f5 !important;
}
.stSelectbox > div > div > div {
    color: #f0f0f5 !important;
    background-color: #252836 !important;
}

/* ── Dropdown popover / menu — white background, black text ── */
[data-baseweb="popover"] {
    background-color: #ffffff !important;
}
[data-baseweb="popover"] * {
    background-color: #ffffff !important;
    color: #111111 !important;
}
[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid rgba(108,99,255,0.3) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
}
[data-baseweb="menu"] * {
    background-color: #ffffff !important;
    color: #111111 !important;
}
[data-baseweb="option"] {
    background-color: #ffffff !important;
    color: #111111 !important;
}
[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {
    background-color: rgba(108,99,255,0.1) !important;
    color: #111111 !important;
}

.stTextInput > label,
.stSelectbox > label,
.stTextArea > label,
.stDateInput > label,
.stTimeInput > label,
.stCheckbox > label {
    color: #9b9bb4 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.stButton > button {
    background-color: #6c63ff !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background-color: #8b85ff !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.3) !important;
}
.stButton > button[kind="secondary"] {
    background-color: #252836 !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    color: #f0f0f5 !important;
}
.stButton > button[kind="secondary"]:hover {
    background-color: #2e3248 !important;
    border-color: #6c63ff !important;
}

.stFormSubmitButton > button {
    background-color: #6c63ff !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stFormSubmitButton > button:hover { background-color: #8b85ff !important; }

.streamlit-expanderHeader,
[data-testid="stExpander"] > div:first-child {
    background-color: #1a1d2e !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 8px !important;
    color: #f0f0f5 !important;
}
[data-testid="stExpander"] {
    background-color: #1a1d2e !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] * { color: #f0f0f5 !important; }

.stDataFrame { border-radius: 8px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] * { background-color: #1a1d2e !important; color: #f0f0f5 !important; }
.dataframe th { background-color: #252836 !important; color: #9b9bb4 !important; }
.dataframe td {
    background-color: #1a1d2e !important;
    color: #f0f0f5 !important;
    border-color: rgba(108,99,255,0.1) !important;
}

[data-testid="stAlert"] {
    background-color: rgba(59,130,246,0.1) !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 8px !important;
    color: #f0f0f5 !important;
}
[data-testid="stAlert"] * { color: #f0f0f5 !important; }

/* ── Date picker calendar — white background, black text ── */
[data-baseweb="calendar"] {
    background-color: #ffffff !important;
    color: #111111 !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
}
[data-baseweb="calendar"] * {
    background-color: #ffffff !important;
    color: #111111 !important;
}
[data-baseweb="calendar"] [aria-selected="true"],
[data-baseweb="calendar"] [data-selected="true"] {
    background-color: #6c63ff !important;
    color: #ffffff !important;
    border-radius: 50% !important;
}
[data-baseweb="calendar"] [aria-selected="true"] *,
[data-baseweb="calendar"] [data-selected="true"] * {
    background-color: #6c63ff !important;
    color: #ffffff !important;
}
[data-baseweb="calendar"] [data-today="true"] {
    border: 1px solid #6c63ff !important;
    border-radius: 50% !important;
}
[data-baseweb="calendar"] button:hover {
    background-color: rgba(108,99,255,0.15) !important;
    border-radius: 50% !important;
}

/* ── Time input — white background, black text ── */
[data-testid="stTimeInput"] input {
    background-color: #ffffff !important;
    color: #111111 !important;
    border-color: rgba(108,99,255,0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stTimeInput"] input::placeholder {
    color: #888888 !important;
}
[data-baseweb="time-picker"] {
    background-color: #ffffff !important;
    color: #111111 !important;
}
[data-baseweb="time-picker"] * {
    background-color: #ffffff !important;
    color: #111111 !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background-color: #0f1117 !important; }
::-webkit-scrollbar-thumb { background-color: rgba(108,99,255,0.4) !important; border-radius: 3px !important; }
::-webkit-scrollbar-thumb:hover { background-color: #6c63ff !important; }

.stMarkdown, .stMarkdown p, .stMarkdown span { color: #f0f0f5 !important; }
.stMarkdown strong { color: #f0f0f5 !important; }
code {
    background-color: #252836 !important;
    color: #8b85ff !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
}

[data-baseweb="tab"] { background-color: #1a1d2e !important; color: #9b9bb4 !important; }
[data-baseweb="tab"][aria-selected="true"] {
    color: #8b85ff !important;
    border-bottom-color: #6c63ff !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "logged_in": False,
        "username": None,
        "role": None,
        "page": "dashboard",
        "edit_report_id": None,
        "message": None,
        "message_type": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─── Helpers ──────────────────────────────────────────────────────────────────
def show_message():
    if st.session_state.message:
        cls = "alert-success" if st.session_state.message_type == "success" else "alert-error"
        st.markdown(f'<div class="{cls}">{st.session_state.message}</div>', unsafe_allow_html=True)
        st.session_state.message = None
        st.session_state.message_type = None

def set_message(msg, kind="success"):
    st.session_state.message = msg
    st.session_state.message_type = kind

def status_badge(status):
    mapping = {
        "Submitted":   "badge-submitted",
        "In Progress": "badge-progress",
        "Pending":     "badge-pending",
        "Leave":       "badge-leave",
        "Holiday":     "badge-holiday",
        "Correction":  "badge-correction",
    }
    cls = mapping.get(status, "badge-pending")
    return f'<span class="badge {cls}">{status}</span>'

def nav_to(page):
    st.session_state.page = page
    st.rerun()


# ─── Login Page ───────────────────────────────────────────────────────────────
def login_page():
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-logo">
            <span class="login-logo-icon">📋</span>
            <div class="login-logo-title">DAR Portal</div>
            <div class="login-logo-sub">Daily Activity Report System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        show_message()
        with st.container():
            st.markdown('<div class="dar-card-glow">', unsafe_allow_html=True)
            st.markdown("#### Sign in to your account")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")

            if st.button("Sign In", use_container_width=True):
                if not username or not password:
                    set_message("Please enter both username and password.", "error")
                    st.rerun()
                else:
                    result = authenticate_user(username, password)
                    if result:
                        st.session_state.logged_in = True
                        st.session_state.username = result["username"]
                        st.session_state.role = result["role"]
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        set_message("Invalid username or password.", "error")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; margin-top:24px; color: #6b6b80; font-size: 0.8rem;">
            Contact your administrator if you need access.
        </div>
        """, unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 8px 0 20px;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem; font-weight:700; color:#f0f0f5;">
                📋 DAR Portal
            </div>
        </div>
        <div class="nav-user-info">
            <div class="nav-username">👤 {st.session_state.username}</div>
            <div class="nav-role">{st.session_state.role}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Navigation**")

        is_admin = st.session_state.role == "Admin"

        # ── Build nav: Change Password is Admin-only ──
        pages = [
            ("📊 Dashboard", "dashboard"),
            ("📝 Submit Report", "submit"),
            ("📁 My Reports", "my_reports"),
        ]
        if is_admin:
            pages += [
                ("🗂️ All Reports", "all_reports"),
                ("👥 Manage Users", "manage_users"),
                ("🔑 Change Password", "change_password"),   # Admin only
            ]

        for label, key in pages:
            active = st.session_state.page == key
            if st.button(label, key=f"nav_{key}", use_container_width=True,
                         type="primary" if active else "secondary"):
                nav_to(key)

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# ─── Dashboard ────────────────────────────────────────────────────────────────
def dashboard_page():
    is_admin = st.session_state.role == "Admin"
    username = st.session_state.username

    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">{"Admin Dashboard" if is_admin else "My Dashboard"}</div>
        <div class="page-subtitle">{"System-wide overview" if is_admin else f"Welcome back, {username}"}</div>
    </div>
    """, unsafe_allow_html=True)

    reports_df = get_all_reports() if is_admin else get_user_reports(username)

    if reports_df is None or reports_df.empty:
        st.info("No reports found yet. Submit your first DAR to get started.")
        if not is_admin:
            if st.button("➕ Submit Your First Report"):
                nav_to("submit")
        return

    total     = len(reports_df)
    pending   = len(reports_df[reports_df["Status"] == "Pending"])      if "Status" in reports_df else 0
    submitted = len(reports_df[reports_df["Status"] == "Submitted"])    if "Status" in reports_df else 0
    leave     = len(reports_df[reports_df["Status"] == "Leave"])        if "Status" in reports_df else 0
    holiday   = len(reports_df[reports_df["Status"] == "Holiday"])      if "Status" in reports_df else 0
    in_prog   = len(reports_df[reports_df["Status"] == "In Progress"])  if "Status" in reports_df else 0

    if is_admin:
        users_df = get_all_users()
        total_users = len(users_df) if users_df is not None else 0
        today_str = date.today().strftime("%Y-%m-%d")
        today_reports = len(reports_df[reports_df["Date"].astype(str).str.startswith(today_str)]) if "Date" in reports_df else 0

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{total_users}</div>
                <div class="metric-label">Total Employees</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total Reports</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{today_reports}</div>
                <div class="metric-label">Submitted Today</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{pending}</div>
                <div class="metric-label">Pending</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{leave}</div>
                <div class="metric-label">Leave Records</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{holiday}</div>
                <div class="metric-label">Holiday Records</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Recent Reports")
        recent = reports_df.sort_values("Created Timestamp", ascending=False).head(10) if "Created Timestamp" in reports_df.columns else reports_df.head(10)
        display_cols = [c for c in ["Username", "Date", "Daily Task / Activity", "Status", "Project", "Director"] if c in recent.columns]
        if display_cols:
            st.dataframe(recent[display_cols], use_container_width=True, hide_index=True)

    else:
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total Reports</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{pending}</div>
                <div class="metric-label">Pending</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{submitted}</div>
                <div class="metric-label">Submitted</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{in_prog}</div>
                <div class="metric-label">In Progress</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{leave}</div>
                <div class="metric-label">Leave</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("➕ Submit New Report", type="primary"):
            nav_to("submit")

        st.markdown("#### Recent Activity")
        recent = reports_df.sort_values("Created Timestamp", ascending=False).head(5) if "Created Timestamp" in reports_df.columns else reports_df.head(5)
        display_cols = [c for c in ["Date", "Daily Task / Activity", "Status", "Project", "Director"] if c in recent.columns]
        if display_cols:
            st.dataframe(recent[display_cols], use_container_width=True, hide_index=True)


# ─── Report Form (shared for submit & edit) ───────────────────────────────────
def report_form(existing=None):
    is_edit = existing is not None

    col1, col2 = st.columns(2)
    with col1:
        default_date = date.today()
        if is_edit and existing.get("Date"):
            try:
                default_date = datetime.strptime(str(existing["Date"])[:10], "%Y-%m-%d").date()
            except:
                pass
        report_date = st.date_input("Date *", value=default_date)

    with col2:
        status_opts = ["In Progress", "Submitted", "Pending", "Leave", "Holiday", "Correction"]
        default_status_idx = status_opts.index(existing["Status"]) if is_edit and existing.get("Status") in status_opts else 0
        status = st.selectbox("Status *", status_opts, index=default_status_idx)

    task = st.text_area("Daily Task / Activity *",
                         value=existing.get("Daily Task / Activity", "") if is_edit else "",
                         height=100,
                         placeholder="Describe what you worked on today...")

    col3, col4 = st.columns(2)
    with col3:
        director_opts = ["Parish Sir", "Aditya Sir", "Both"]
        default_dir_idx = director_opts.index(existing["Director"]) if is_edit and existing.get("Director") in director_opts else 0
        director = st.selectbox("Director *", director_opts, index=default_dir_idx)
    with col4:
        designer = st.text_input("Designer", value=existing.get("Designer", "") if is_edit else "")

    col5, col6 = st.columns(2)
    with col5:
        project = st.text_input("Project", value=existing.get("Project", "") if is_edit else "")
    with col6:
        new_project = st.text_input("New Project", value=existing.get("New Project", "") if is_edit else "")

    notes = st.text_area("Notes", value=existing.get("Notes", "") if is_edit else "", height=80)

    col7, col8 = st.columns(2)
    with col7:
        default_from = time(9, 0)
        if is_edit and existing.get("Time From"):
            try:
                default_from = datetime.strptime(str(existing["Time From"]), "%H:%M").time()
            except:
                pass
        time_from = st.time_input("Time From", value=default_from)
    with col8:
        default_to = time(18, 0)
        if is_edit and existing.get("Time To"):
            try:
                default_to = datetime.strptime(str(existing["Time To"]), "%H:%M").time()
            except:
                pass
        time_to = st.time_input("Time To", value=default_to)

    return {
        "date": report_date,
        "task": task,
        "status": status,
        "director": director,
        "designer": designer,
        "project": project,
        "new_project": new_project,
        "notes": notes,
        "time_from": time_from.strftime("%H:%M"),
        "time_to": time_to.strftime("%H:%M"),
    }


# ─── Submit Report ────────────────────────────────────────────────────────────
def submit_page():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📝 Submit Daily Report</div>
        <div class="page-subtitle">Log your daily activity for today</div>
    </div>
    """, unsafe_allow_html=True)

    show_message()

    with st.form("submit_dar"):
        data = report_form()
        submitted = st.form_submit_button("Submit Report", use_container_width=True)

    if submitted:
        if not data["task"].strip():
            set_message("Daily Task / Activity is required.", "error")
            st.rerun()
        else:
            report_id = str(uuid.uuid4())[:8].upper()
            ok = submit_report(
                report_id=report_id,
                username=st.session_state.username,
                date=str(data["date"]),
                task=data["task"],
                status=data["status"],
                director=data["director"],
                designer=data["designer"],
                project=data["project"],
                new_project=data["new_project"],
                notes=data["notes"],
                time_from=data["time_from"],
                time_to=data["time_to"],
            )
            if ok:
                set_message(f"✅ Report #{report_id} submitted successfully!", "success")
            else:
                set_message("Failed to submit report. Please check Google Sheets connection.", "error")
            st.rerun()


# ─── My Reports ───────────────────────────────────────────────────────────────
def my_reports_page():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">📁 My Reports</div>
        <div class="page-subtitle">View and manage your daily activity reports</div>
    </div>
    """, unsafe_allow_html=True)

    show_message()

    reports_df = get_user_reports(st.session_state.username)
    if reports_df is None or reports_df.empty:
        st.info("You haven't submitted any reports yet.")
        if st.button("➕ Submit First Report"):
            nav_to("submit")
        return

    months = {
        "All Months": None, "January": 1, "February": 2, "March": 3,
        "April": 4, "May": 5, "June": 6, "July": 7,
        "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    with st.expander("🔍 Search & Filter", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            search_project = st.text_input("Search by Project", placeholder="Project name...")
        with fc2:
            selected_month_name = st.selectbox("Filter by Month", list(months.keys()))
            search_month = months[selected_month_name]
        with fc3:
            status_filter = st.selectbox("Filter by Status", ["All"] + ["In Progress", "Submitted", "Pending", "Leave", "Holiday", "Correction"])

        search_date = st.date_input("Filter by Date", value=None)

    filtered = reports_df.copy()
    if search_project:
        filtered = filtered[filtered["Project"].astype(str).str.contains(search_project, case=False, na=False)]
    if search_month:
        filtered = filtered[pd.to_datetime(filtered["Date"], errors="coerce").dt.month == search_month]
    if search_date:
        filtered = filtered[filtered["Date"].astype(str).str.startswith(str(search_date))]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]

    st.markdown(f"**{len(filtered)} report(s) found**")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if filtered.empty:
        st.info("No reports match your filters.")
        return

    sorted_df = filtered.sort_values("Date", ascending=False) if "Date" in filtered.columns else filtered

    for _, row in sorted_df.iterrows():
        with st.expander(f"📄 {row.get('Date', 'N/A')} — {str(row.get('Daily Task / Activity', ''))[:60]}... | {row.get('Status', '')}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Date:** {row.get('Date', 'N/A')}")
                st.markdown(f"**Status:** {row.get('Status', 'N/A')}")
                st.markdown(f"**Director:** {row.get('Director', 'N/A')}")
            with c2:
                st.markdown(f"**Project:** {row.get('Project', '—')}")
                st.markdown(f"**New Project:** {row.get('New Project', '—')}")
                st.markdown(f"**Designer:** {row.get('Designer', '—')}")
            with c3:
                st.markdown(f"**Time:** {row.get('Time From', '—')} → {row.get('Time To', '—')}")
                st.markdown(f"**Report ID:** `{row.get('ID', 'N/A')}`")

            st.markdown(f"**Task:** {row.get('Daily Task / Activity', '—')}")
            if row.get("Notes"):
                st.markdown(f"**Notes:** {row.get('Notes', '')}")

            if st.button("✏️ Edit Report", key=f"edit_{row.get('ID')}"):
                st.session_state.edit_report_id = row.get("ID")
                nav_to("edit_report")


# ─── Edit Report ──────────────────────────────────────────────────────────────
def edit_report_page():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">✏️ Edit Report</div>
        <div class="page-subtitle">Update your daily activity report</div>
    </div>
    """, unsafe_allow_html=True)

    show_message()
    report_id = st.session_state.get("edit_report_id")
    if not report_id:
        st.error("No report selected.")
        if st.button("← Back"):
            nav_to("my_reports")
        return

    report = get_report_by_id(report_id)
    if report is None:
        st.error("Report not found.")
        return

    if st.session_state.role != "Admin" and report.get("Username") != st.session_state.username:
        st.error("Access denied: you can only edit your own reports.")
        return

    if st.button("← Back to Reports"):
        nav_to("my_reports" if st.session_state.role != "Admin" else "all_reports")

    with st.form("edit_dar"):
        data = report_form(existing=report)
        save_btn = st.form_submit_button("Save Changes", use_container_width=True)

    if save_btn:
        if not data["task"].strip():
            set_message("Daily Task / Activity is required.", "error")
            st.rerun()
        else:
            ok = update_report(
                report_id=report_id,
                date=str(data["date"]),
                task=data["task"],
                status=data["status"],
                director=data["director"],
                designer=data["designer"],
                project=data["project"],
                new_project=data["new_project"],
                notes=data["notes"],
                time_from=data["time_from"],
                time_to=data["time_to"],
            )
            if ok:
                set_message("✅ Report updated successfully!", "success")
                nav_to("my_reports" if st.session_state.role != "Admin" else "all_reports")
            else:
                set_message("Failed to update report.", "error")
                st.rerun()


# ─── All Reports (Admin) ──────────────────────────────────────────────────────
def all_reports_page():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">🗂️ All Reports</div>
        <div class="page-subtitle">View and manage reports from all employees</div>
    </div>
    """, unsafe_allow_html=True)

    show_message()
    reports_df = get_all_reports()
    if reports_df is None or reports_df.empty:
        st.info("No reports have been submitted yet.")
        return

    months = {
        "All Months": None, "January": 1, "February": 2, "March": 3,
        "April": 4, "May": 5, "June": 6, "July": 7,
        "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    with st.expander("🔍 Search & Filter", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            search_project = st.text_input("Search by Project", placeholder="Project name...")
        with fc2:
            selected_month_name = st.selectbox("Filter by Month", list(months.keys()))
            search_month = months[selected_month_name]
        with fc3:
            emp_list = ["All"] + sorted(reports_df["Username"].dropna().unique().tolist()) if "Username" in reports_df.columns else ["All"]
            emp_filter = st.selectbox("Filter by Employee", emp_list)

        fc4, fc5 = st.columns(2)
        with fc4:
            status_filter = st.selectbox("Filter by Status", ["All"] + ["In Progress", "Submitted", "Pending", "Leave", "Holiday", "Correction"])
        with fc5:
            search_date = st.date_input("Filter by Date", value=None)

    filtered = reports_df.copy()
    if emp_filter != "All":
        filtered = filtered[filtered["Username"] == emp_filter]
    if search_month:
        filtered = filtered[pd.to_datetime(filtered["Date"], errors="coerce").dt.month == search_month]
    if search_date:
        filtered = filtered[filtered["Date"].astype(str).str.startswith(str(search_date))]
    if search_project:
        filtered = filtered[filtered["Project"].astype(str).str.contains(search_project, case=False, na=False)]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]

    st.markdown(f"**{len(filtered)} report(s) found**")

    sorted_df = filtered.sort_values("Date", ascending=False) if "Date" in filtered.columns else filtered

    for _, row in sorted_df.iterrows():
        with st.expander(f"👤 {row.get('Username', 'N/A')} | 📄 {row.get('Date', 'N/A')} — {str(row.get('Daily Task / Activity', ''))[:50]}..."):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Employee:** {row.get('Username', 'N/A')}")
                st.markdown(f"**Date:** {row.get('Date', 'N/A')}")
                st.markdown(f"**Status:** {row.get('Status', 'N/A')}")
            with c2:
                st.markdown(f"**Director:** {row.get('Director', 'N/A')}")
                st.markdown(f"**Project:** {row.get('Project', '—')}")
                st.markdown(f"**Designer:** {row.get('Designer', '—')}")
            with c3:
                st.markdown(f"**Time:** {row.get('Time From', '—')} → {row.get('Time To', '—')}")
                st.markdown(f"**Report ID:** `{row.get('ID', 'N/A')}`")
            st.markdown(f"**Task:** {row.get('Daily Task / Activity', '—')}")
            if row.get("Notes"):
                st.markdown(f"**Notes:** {row.get('Notes', '')}")
            if st.button("✏️ Edit", key=f"admin_edit_{row.get('ID')}"):
                st.session_state.edit_report_id = row.get("ID")
                nav_to("edit_report")


# ─── Manage Users (Admin) ─────────────────────────────────────────────────────
def manage_users_page():
    st.markdown("""
    <div class="page-header">
        <div class="page-title">👥 Manage Users</div>
        <div class="page-subtitle">Add, edit and remove employee accounts</div>
    </div>
    """, unsafe_allow_html=True)

    show_message()
    users_df = get_all_users()

    with st.expander("➕ Add New Employee", expanded=False):
        with st.form("add_user"):
            u1, u2, u3 = st.columns(3)
            with u1:
                new_user = st.text_input("Username *")
            with u2:
                new_pass = st.text_input("Password *", type="password")
            with u3:
                new_role = st.selectbox("Role", ["Employee", "Admin"])
            add_btn = st.form_submit_button("Create Account", use_container_width=True)

        if add_btn:
            if not new_user.strip() or not new_pass.strip():
                set_message("Username and Password are required.", "error")
                st.rerun()
            else:
                ok = add_user(new_user.strip(), new_pass.strip(), new_role)
                if ok:
                    set_message(f"✅ User '{new_user}' created successfully!", "success")
                else:
                    set_message("Failed to create user. Username may already exist.", "error")
                st.rerun()

    st.markdown("#### Current Users")

    if users_df is None or users_df.empty:
        st.info("No users found.")
        return

    for _, row in users_df.iterrows():
        uname = row.get("Username", "N/A")
        urole = row.get("Role", "N/A")
        upass = row.get("Password", "****")

        col1, col2, col3, col4, col5 = st.columns([2, 1.5, 2, 1.5, 1.5])
        with col1:
            st.markdown(f"**{uname}**")
        with col2:
            st.markdown(f"`{urole}`")
        with col3:
            st.markdown(f"🔑 `{upass}`")
        with col4:
            new_p = st.text_input("New password", key=f"cp_{uname}", type="password",
                                   label_visibility="collapsed", placeholder="New password")
            if st.button("Update", key=f"upd_{uname}", type="secondary"):
                if new_p:
                    ok = update_password(uname, new_p)
                    set_message(f"Password updated for {uname}." if ok else "Update failed.",
                                "success" if ok else "error")
                    st.rerun()
        with col5:
            if uname != st.session_state.username:
                if st.button("🗑️ Delete", key=f"del_{uname}", type="secondary"):
                    ok = delete_user(uname)
                    set_message(f"User '{uname}' deleted." if ok else "Delete failed.",
                                "success" if ok else "error")
                    st.rerun()
            else:
                st.markdown("*(you)*")

        st.markdown('<div class="section-divider" style="margin:8px 0"></div>', unsafe_allow_html=True)


# ─── Change Password (Admin only) ─────────────────────────────────────────────
def change_password_page():
    # Double-guard: redirect non-admins away even if they navigate directly
    if st.session_state.role != "Admin":
        st.error("Access denied: this page is for administrators only.")
        if st.button("← Back to Dashboard"):
            nav_to("dashboard")
        return

    st.markdown("""
    <div class="page-header">
        <div class="page-title">🔑 Change Password</div>
        <div class="page-subtitle">Update your admin account password</div>
    </div>
    """, unsafe_allow_html=True)

    show_message()

    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("change_pw"):
            current_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")
            submit = st.form_submit_button("Update Password", use_container_width=True)

        if submit:
            auth = authenticate_user(st.session_state.username, current_pw)
            if not auth:
                set_message("Current password is incorrect.", "error")
            elif not new_pw:
                set_message("New password cannot be empty.", "error")
            elif new_pw != confirm_pw:
                set_message("New passwords do not match.", "error")
            else:
                ok = update_password(st.session_state.username, new_pw)
                set_message("✅ Password updated successfully!" if ok else "Failed to update password.",
                            "success" if ok else "error")
            st.rerun()


# ─── Main Router ──────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    render_sidebar()

    page = st.session_state.page
    is_admin = st.session_state.role == "Admin"

    if page == "dashboard":
        dashboard_page()
    elif page == "submit":
        submit_page()
    elif page == "my_reports":
        my_reports_page()
    elif page == "edit_report":
        edit_report_page()
    elif page == "all_reports" and is_admin:
        all_reports_page()
    elif page == "manage_users" and is_admin:
        manage_users_page()
    elif page == "change_password" and is_admin:   # Admin-only route guard
        change_password_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
