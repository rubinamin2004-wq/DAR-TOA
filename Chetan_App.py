"""
Team DAR — Pune  |  Streamlit Edition v3
Run:  streamlit run dar_app.py
"""

import streamlit as st
import json, os, hashlib, copy, random, string
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Must be FIRST Streamlit call ─────────────────────────────────────
st.set_page_config(
    page_title="Team DAR — Pune",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────────────────────────────

import streamlit as st

# Hide the upper-right menu items and GitHub icon
st.markdown(
    """
    <style>
    /* Hides the entire top header bar including Share, Star, and GitHub buttons */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
    
    /* Optional: Hides the main menu three-dot icon specifically if header is kept */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Optional: Hides the "Deploy" or header buttons if they still render */
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root palette ── */
:root {
  --bg:        #F7F6F2;
  --surface:   #FFFFFF;
  --border:    #E4E1D9;
  --border2:   #CCC9BF;
  --text:      #1C1B18;
  --text2:     #5C5952;
  --text3:     #9C9890;
  --accent:    #C17B3C;
  --accent-bg: #FDF4EB;
  --blue:      #2D6FB3;
  --blue-bg:   #EDF3FB;
  --green:     #2A7A4E;
  --green-bg:  #EAF5EF;
  --red:       #B83232;
  --red-bg:    #FDF0F0;
  --purple:    #6B4DB3;
  --purple-bg: #F2EEFB;
  --orange:    #D4620A;
  --orange-bg: #FFF0E6;
}

/* ── Global ── */
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
  color: var(--text);
}
.main .block-container {
  padding-top: 1.5rem;
  padding-bottom: 3rem;
  max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stButton > button {
  border-radius: 8px !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 8px 12px !important;
  text-align: left !important;
  justify-content: flex-start !important;
  width: 100% !important;
  transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid transparent !important;
  color: var(--text2) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
  background: var(--bg) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: var(--accent-bg) !important;
  border: 1px solid #E8C08A !important;
  color: var(--accent) !important;
}

/* ── Buttons ── */
.stButton > button[kind="primary"] {
  background: var(--accent) !important;
  border: none !important;
  color: #fff !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  padding: 10px 22px !important;
  transition: opacity 0.15s !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88 !important; }
.stButton > button[kind="secondary"] {
  border-radius: 8px !important;
  font-size: 13px !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  color: var(--text2) !important;
}
.stButton > button[kind="secondary"]:hover {
  border-color: var(--border2) !important;
  color: var(--text) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  border-radius: 8px !important;
  border: 1px solid var(--border) !important;
  background: #FAFAF8 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
  color: var(--text) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(193,123,60,0.12) !important;
  background: #fff !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface);
  border-bottom: 2px solid var(--border);
  gap: 4px;
  padding: 0 4px;
}
.stTabs [data-baseweb="tab"] {
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--text2) !important;
  padding: 10px 18px !important;
  border-radius: 0 !important;
  background: transparent !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom-color: var(--accent) !important;
  font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding-top: 20px !important;
}

/* ── Metrics ── */
div[data-testid="metric-container"] {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
div[data-testid="metric-container"] label {
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.6px !important;
  color: var(--text3) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-size: 28px !important;
  font-weight: 700 !important;
  letter-spacing: -0.8px !important;
}

/* ── Expander ── */
.stExpander {
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  background: var(--surface) !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
  overflow: hidden !important;
}
.stExpander > details > summary {
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 14px 18px !important;
  background: var(--surface) !important;
  border-radius: 12px !important;
}
.stExpander > details[open] > summary {
  border-bottom: 1px solid var(--border) !important;
  border-radius: 12px 12px 0 0 !important;
}
.stExpander > details > div {
  padding: 18px !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px !important; border: 1px solid var(--border) !important; overflow: hidden !important; }
.stDataFrame thead th { background: #FAFAF8 !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; color: var(--text3) !important; }

/* ── Alerts ── */
.stWarning { border-radius: 10px !important; border-left: 4px solid var(--orange) !important; background: var(--orange-bg) !important; }
.stInfo    { border-radius: 10px !important; border-left: 4px solid var(--blue)   !important; background: var(--blue-bg)   !important; }
.stSuccess { border-radius: 10px !important; border-left: 4px solid var(--green)  !important; background: var(--green-bg)  !important; }
.stError   { border-radius: 10px !important; border-left: 4px solid var(--red)    !important; background: var(--red-bg)    !important; }

/* ── Dividers ── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 16px 0 !important; }

/* ── Status badges ── */
.badge {
  display: inline-block; padding: 3px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; font-family: 'Inter', sans-serif;
}
.badge-submitted    { background:#EAF5EF; color:#2A7A4E; border:1px solid #A8D8BB; }
.badge-in-progress  { background:#EDF3FB; color:#2D6FB3; border:1px solid #A8C4E8; }
.badge-pending      { background:#FDF3E8; color:#C17B3C; border:1px solid #E8C08A; }
.badge-leave        { background:#FDF0F0; color:#B83232; border:1px solid #E8A8A8; }
.badge-correction   { background:#FFF0E6; color:#D4620A; border:1px solid #F0C09A; }
.badge-holiday      { background:#F2EEFB; color:#6B4DB3; border:1px solid #C4B0E8; }

/* ── Section headings ── */
.section-title {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.7px; color: var(--text3); margin-bottom: 10px;
}

/* ── Card containers ── */
.dar-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px 22px; margin-bottom: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* ── Entry row ── */
.entry-row-date { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text2); }
.entry-row-task { font-size: 13px; color: var(--text); line-height: 1.4; }
.entry-divider  { border: none; border-top: 1px solid #F0EDE8; margin: 6px 0; }

/* ── Page title ── */
.page-title {
  font-size: 22px; font-weight: 700; letter-spacing: -0.5px; color: var(--text);
  margin-bottom: 2px;
}
.page-subtitle { font-size: 13px; color: var(--text2); margin-bottom: 22px; }

/* ── Plotly chart containers ── */
.js-plotly-plot { border-radius: 10px; }

/* ── Radio horizontal ── */
.stRadio [data-testid="stHorizontalBlock"] label {
  font-size: 12px !important;
  font-weight: 500 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
  border-radius: 8px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
  color: var(--text2) !important;
}
.stDownloadButton > button:hover {
  border-color: var(--border2) !important;
  color: var(--text) !important;
}

/* ── Sidebar section label ── */
.sb-section-lbl {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--text3); padding: 0 8px;
  margin: 12px 0 6px 0; display: block;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────
DATA_FILE    = "dar_data.json"
ADMIN_MEMBER = "Chetan"
DIRECTORS    = ["Aditya Sir", "Parish Sir"]
STATUS_OPTIONS = ["In Progress", "Submitted", "Pending", "Leave", "Holiday", "Correction"]

STATUS_COLORS = {
    "In Progress": "#2D6FB3",
    "Submitted":   "#2A7A4E",
    "Pending":     "#C17B3C",
    "Leave":       "#B83232",
    "Holiday":     "#6B4DB3",
    "Correction":  "#D4620A",
}
STATUS_BG = {
    "In Progress": "#EDF3FB",
    "Submitted":   "#EAF5EF",
    "Pending":     "#FDF3E8",
    "Leave":       "#FDF0F0",
    "Holiday":     "#F2EEFB",
    "Correction":  "#FFF0E6",
}

DIR_PALETTE  = ["#6B4DB3","#C17B3C","#2D6FB3","#2A7A4E","#B83232","#1D7E70","#A94080","#3D4FB3"]
MB_PALETTE   = ["#E8923A","#2D6FB3","#2A7A4E","#6B4DB3","#B83232","#1D7E70","#A94080","#3D4FB3"]

DEFAULT_MEMBERS = [
    {"id": 1, "name": "Chetan",    "initials": "CH"},
    {"id": 2, "name": "Kushal",    "initials": "KU"},
    {"id": 3, "name": "Siddharth", "initials": "SD"},
    {"id": 4, "name": "Rohan",     "initials": "RO"},
    {"id": 5, "name": "Prasad",    "initials": "PR"},
    {"id": 6, "name": "Nikita",    "initials": "NK"},
    {"id": 7, "name": "Sachin",    "initials": "SA"},
    {"id": 8, "name": "Sukhada",   "initials": "SU"},
]
DEFAULT_ENTRIES = [
    {"id":"d1","member_id":5,"date":"2026-04-02","task":"Changes in views","director":"Aditya Sir","designer":"Prasad","project":"GENERAC","new_project":"","time_from":"","time_to":"","status":"In Progress","notes":"Individual working"},
    {"id":"d2","member_id":5,"date":"2026-04-17","task":"Submitted walkthrough","director":"Parish Sir","designer":"Prasad","project":"SULZER","new_project":"","time_from":"09:00","time_to":"12:30","status":"Submitted","notes":""},
    {"id":"d3","member_id":6,"date":"2026-04-07","task":"Revision 5th, Cabin 3 option","director":"Aditya Sir","designer":"Nikita","project":"STRUX ONE","new_project":"","time_from":"09:33","time_to":"18:00","status":"Submitted","notes":"Views submitted"},
    {"id":"d4","member_id":6,"date":"2026-04-28","task":"Schmersal reception changes","director":"Parish Sir","designer":"Nikita","project":"SCHMERSAL","new_project":"","time_from":"","time_to":"","status":"Correction","notes":"Correction round 2"},
    {"id":"d5","member_id":1,"date":"2026-04-10","task":"3D modelling for lobby area","director":"Aditya Sir","designer":"Chetan","project":"GENERAC","new_project":"","time_from":"10:00","time_to":"17:00","status":"Submitted","notes":""},
    {"id":"d6","member_id":2,"date":"2026-04-12","task":"Render revisions","director":"Parish Sir","designer":"Kushal","project":"DELTA","new_project":"","time_from":"09:00","time_to":"13:00","status":"Pending","notes":""},
]

# ─────────────────────────────────────────────────────────────────────
# PERSISTENCE
# ─────────────────────────────────────────────────────────────────────
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                d = json.load(f)
            d.setdefault("members",       copy.deepcopy(DEFAULT_MEMBERS))
            d.setdefault("entries",       copy.deepcopy(DEFAULT_ENTRIES))
            d.setdefault("admin_pw_hash", hash_pw("admin123"))
            d.setdefault("member_pins",   {})
            return d
        except Exception:
            pass
    fresh = {
        "members":       copy.deepcopy(DEFAULT_MEMBERS),
        "entries":       copy.deepcopy(DEFAULT_ENTRIES),
        "admin_pw_hash": hash_pw("admin123"),
        "member_pins":   {},
    }
    save_data(fresh)
    return fresh

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

def persist():
    save_data(st.session_state.data)

# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────
def uid():
    return datetime.now().strftime("%Y%m%d%H%M%S") + "".join(random.choices(string.ascii_lowercase, k=4))

def calc_time(tf, tt):
    if not tf or not tt:
        return ""
    try:
        delta = datetime.strptime(tt, "%H:%M") - datetime.strptime(tf, "%H:%M")
        mins  = int(delta.total_seconds() / 60)
        if mins <= 0: return ""
        h, m = divmod(mins, 60)
        if h and m: return f"{h}h {m}m"
        return f"{h}h" if h else f"{m}m"
    except Exception:
        return ""

def calc_mins(tf, tt):
    try:
        delta = datetime.strptime(tt, "%H:%M") - datetime.strptime(tf, "%H:%M")
        m = int(delta.total_seconds() / 60)
        return m if m > 0 else 0
    except Exception:
        return 0

def fmt_date(d):
    try: return datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y")
    except Exception: return d

def all_projects(data):
    return sorted(set(e["project"] for e in data["entries"] if e.get("project")))

def get_member(data, mid):
    return next((m for m in data["members"] if m["id"] == mid), None)

def member_entries(data, mid):
    return [e for e in data["entries"] if e["member_id"] == mid]

def missing_today(data):
    today = date.today().isoformat()
    return [m for m in data["members"]
            if not any(e["date"] == today and e["member_id"] == m["id"] for e in data["entries"])]

def mb_color(idx):
    return MB_PALETTE[idx % len(MB_PALETTE)]

def status_badge(status):
    cls = status.lower().replace(" ", "-")
    return f'<span class="badge badge-{cls}">{status}</span>'

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────
if "data"                not in st.session_state: st.session_state.data = load_data()
if "admin_unlocked"      not in st.session_state: st.session_state.admin_unlocked = False
if "current_view"        not in st.session_state: st.session_state.current_view = st.session_state.data["members"][0]["id"]
if "pin_unlocked_for"    not in st.session_state: st.session_state.pin_unlocked_for = set()
if "chetan_verified"     not in st.session_state: st.session_state.chetan_verified = False

data = st.session_state.data  # alias

# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div style="padding:16px 12px 10px 12px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <div style="width:32px;height:32px;background:#C17B3C;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:15px;">D</div>
        <div>
          <div style="font-size:14px;font-weight:700;color:#1C1B18;letter-spacing:-0.3px;">Team DAR</div>
          <div style="font-size:11px;color:#9C9890;">Pune Office</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='padding:0 12px 8px;font-size:11px;color:#9C9890;'>{date.today().strftime('%A, %d %B %Y')}</div>", unsafe_allow_html=True)

    # Missing DAR pill
    missing = missing_today(data)
    if missing:
        names = ", ".join(m["name"] for m in missing[:3])
        extra = f" +{len(missing)-3}" if len(missing) > 3 else ""
        st.markdown(f"""
        <div style="margin:0 12px 10px;background:#FDF0F0;border:1px solid #E8A8A8;
          border-radius:8px;padding:8px 12px;font-size:12px;color:#B83232;font-weight:500;">
          ⚠ {len(missing)} missing today's DAR<br>
          <span style="font-weight:400;font-size:11px;">{names}{extra}</span>
        </div>""", unsafe_allow_html=True)

    # Members section
    st.markdown("<span class='sb-section-lbl'>Team Members</span>", unsafe_allow_html=True)
    for i, m in enumerate(data["members"]):
        today_iso = date.today().isoformat()
        has_today = any(e["date"] == today_iso and e["member_id"] == m["id"] for e in data["entries"])
        has_pin   = str(m["id"]) in data.get("member_pins", {})
        dot       = "" if has_today else " 🔴"
        pin_icon  = " 🔑" if has_pin else ""
        is_active = st.session_state.current_view == m["id"]
        label     = f"{m['initials']}  {m['name']}{pin_icon}{dot}"
        if st.button(label, key=f"nav_{m['id']}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.current_view = m["id"]
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<span class='sb-section-lbl'>Admin</span>", unsafe_allow_html=True)
    is_admin = st.session_state.current_view == "admin"
    if st.button("⚙  Admin Panel", use_container_width=True, key="nav_admin",
                 type="primary" if is_admin else "secondary"):
        st.session_state.current_view = "admin"
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    with st.expander("＋  Add Team Member"):
        new_name = st.text_input("Full name", key="new_member_name",
                                 label_visibility="collapsed", placeholder="e.g. Rahul Sharma")
        if st.button("Add Member", key="btn_add_member", use_container_width=True):
            n = new_name.strip()
            if n:
                ini   = "".join(w[0].upper() for w in n.split())[:2]
                new_m = {"id": int(datetime.now().timestamp()), "name": n, "initials": ini}
                data["members"].append(new_m)
                persist()
                st.success(f"✅ {n} added")
                st.rerun()
            else:
                st.error("Please enter a name.")


# ─────────────────────────────────────────────────────────────────────
# CHART HELPERS  (Plotly, professional theme)
# ─────────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#5C5952"),
    margin=dict(t=30, b=30, l=10, r=10),
)

def donut(labels, values, colors, title="", size=280, hole=0.58):
    """Single donut chart figure."""
    total = sum(values)
    fig   = go.Figure(go.Pie(
        labels=labels, values=values, hole=hole,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value} entries (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=size,
        showlegend=False,
        annotations=[dict(
            text=f"<b>{total}</b>",
            x=0.5, y=0.5, font_size=22, font_color="#1C1B18", showarrow=False
        )],
    )
    return fig

def hbar(names, values, colors, xlabel="Tasks"):
    """Horizontal bar chart."""
    fig = go.Figure(go.Bar(
        y=names, x=values, orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)")),
        text=[f"  {v}" for v in values], textposition="outside",
        hovertemplate="<b>%{y}</b>: %{x}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=max(200, 60 * len(names) + 80),
        xaxis=dict(title=xlabel, showgrid=True, gridcolor="#F0EDE8", zeroline=False),
        yaxis=dict(showgrid=False),
        bargap=0.35,
    )
    return fig

# ─────────────────────────────────────────────────────────────────────
# ADMIN PAGE
# ─────────────────────────────────────────────────────────────────────
def render_admin():

    # ── Password gate ──────────────────────────────────────────────
    if not st.session_state.admin_unlocked:
        col = st.columns([1, 1.4, 1])[1]
        with col:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="dar-card" style="text-align:center;padding:36px 32px;">
              <div style="font-size:40px;margin-bottom:12px;">🔐</div>
              <div class="page-title" style="font-size:18px;margin-bottom:6px;">Admin Access</div>
              <div class="page-subtitle">Enter the admin password to continue</div>
            </div>""", unsafe_allow_html=True)
            pw_val = st.text_input("Password", type="password", key="admin_pw_input",
                                   placeholder="••••••••", label_visibility="collapsed")
            if st.button("Unlock Admin Panel →", type="primary", use_container_width=True, key="admin_unlock_btn"):
                if hash_pw(pw_val) == data.get("admin_pw_hash", ""):
                    st.session_state.admin_unlocked = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        return

    # ── Header ─────────────────────────────────────────────────────
    st.markdown('<div class="page-title">⚙  Admin Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Full team overview · All activity reports</div>', unsafe_allow_html=True)

    # ── KPI Row ────────────────────────────────────────────────────
    total  = len(data["entries"])
    sub    = sum(1 for e in data["entries"] if e["status"] == "Submitted")
    ip     = sum(1 for e in data["entries"] if e["status"] == "In Progress")
    cor    = sum(1 for e in data["entries"] if e["status"] == "Correction")
    leave  = sum(1 for e in data["entries"] if e["status"] == "Leave")
    miss   = missing_today(data)
    total_mins = sum(calc_mins(e.get("time_from",""), e.get("time_to","")) for e in data["entries"])
    total_hrs  = f"{total_mins // 60}h {total_mins % 60}m" if total_mins else "0h"

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("📊 Total Entries",  total)
    k2.metric("✅ Submitted",       sub,  delta=f"{round(sub/total*100) if total else 0}% of total")
    k3.metric("🔄 In Progress",     ip)
    k4.metric("⚠️ Corrections",    cor)
    k5.metric("⏱ Hours Logged",    total_hrs)
    k6.metric("❌ Missing Today",   len(miss),
              delta=", ".join(m["name"] for m in miss[:2]) + ("…" if len(miss)>2 else "") if miss else "All submitted ✓",
              delta_color="inverse" if miss else "normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────
    tab_entries, tab_analysis, tab_calendar, tab_hours, tab_settings = st.tabs([
        "📋  All Entries",
        "📊  Work Analysis",
        "📆  Attendance Calendar",
        "⏱  Hours Logged",
        "🔒  Settings",
    ])

    # ══════════════════════════════════════════════════════════════
    # TAB 1 — ALL ENTRIES
    # ══════════════════════════════════════════════════════════════
    with tab_entries:
        # Filter bar
        fa, fb, fc, fd = st.columns([2, 1.4, 1.4, 1.4])
        with fa: search     = st.text_input("🔍", key="admin_search", placeholder="Search task, project, member...", label_visibility="collapsed")
        with fb:
            mmap = {"All Members": None}
            mmap.update({m["name"]: m["id"] for m in data["members"]})
            sel_member = st.selectbox("Member", list(mmap.keys()), key="af_member", label_visibility="collapsed")
        with fc: sel_status = st.selectbox("Status", ["All Statuses"] + STATUS_OPTIONS, key="af_status", label_visibility="collapsed")
        with fd:
            months    = sorted(set(e["date"][:7] for e in data["entries"]), reverse=True)
            sel_month = st.selectbox("Month", ["All Months"] + months, key="af_month",
                                     format_func=lambda x: x if x == "All Months" else datetime.strptime(x, "%Y-%m").strftime("%B %Y"),
                                     label_visibility="collapsed")

        fe, ff, fg = st.columns([1.5, 1.5, 1])
        with fe: date_from = st.date_input("From", value=None, key="af_from", label_visibility="collapsed")
        with ff: date_to   = st.date_input("To",   value=None, key="af_to",   label_visibility="collapsed")
        with fg: st.markdown("<br>", unsafe_allow_html=True)

        # Apply filters
        filt = data["entries"][:]
        if search:
            q    = search.lower()
            filt = [e for e in filt if q in (
                e.get("task","") + e.get("project","") + e.get("director","") +
                (get_member(data, e["member_id"]) or {}).get("name","")
            ).lower()]
        if mmap.get(sel_member): filt = [e for e in filt if e["member_id"] == mmap[sel_member]]
        if sel_status != "All Statuses": filt = [e for e in filt if e["status"] == sel_status]
        if sel_month  != "All Months":   filt = [e for e in filt if e["date"].startswith(sel_month)]
        if date_from: filt = [e for e in filt if e["date"] >= date_from.isoformat()]
        if date_to:   filt = [e for e in filt if e["date"] <= date_to.isoformat()]
        filt = sorted(filt, key=lambda e: e["date"], reverse=True)

        st.markdown(f"<div style='font-size:12px;color:#9C9890;margin-bottom:10px;'>{len(filt)} entries</div>", unsafe_allow_html=True)

        if filt:
            rows = []
            for e in filt:
                m = get_member(data, e["member_id"])
                rows.append({
                    "Date":     fmt_date(e["date"]),
                    "Member":   m["name"] if m else "?",
                    "Task":     e.get("task",""),
                    "Director": e.get("director",""),
                    "Designer": e.get("designer",""),
                    "Project":  e.get("project",""),
                    "New Project": e.get("new_project",""),
                    "Time":     (f"{e.get('time_from','')}–{e.get('time_to','')} ({calc_time(e.get('time_from',''),e.get('time_to',''))})"
                                 if e.get("time_from") and e.get("time_to") else "—"),
                    "Status":   e.get("status",""),
                    "Notes":    e.get("notes",""),
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True,
                         column_config={
                             "Status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS),
                             "Task":   st.column_config.TextColumn("Task", width="large"),
                         })

            dl_col, _, del_col = st.columns([1, 2, 2])
            with dl_col:
                csv_bytes = df.to_csv(index=False).encode()
                st.download_button("⬇  Export CSV", data=csv_bytes,
                                   file_name="Team_DAR_Pune.csv", mime="text/csv", key="csv_dl")
            with del_col:
                del_opts = {
                    f"{fmt_date(e['date'])} | {(get_member(data,e['member_id']) or {}).get('name','?')} | {e.get('task','')}": e["id"]
                    for e in filt
                }
                del_sel = st.selectbox("Delete entry", ["— select to delete —"] + list(del_opts.keys()),
                                       key="admin_del_sel", label_visibility="collapsed")
                if del_sel != "— select to delete —":
                    if st.button("🗑  Delete", type="secondary", key="admin_del_btn"):
                        data["entries"] = [x for x in data["entries"] if x["id"] != del_opts[del_sel]]
                        persist()
                        st.success("Entry deleted.")
                        st.rerun()
        else:
            st.info("No entries match your filters.")

    # ══════════════════════════════════════════════════════════════
    # TAB 2 — WORK ANALYSIS  (full feature parity with HTML)
    # ══════════════════════════════════════════════════════════════
    with tab_analysis:
        if not data["entries"]:
            st.info("No entries yet — nothing to analyse.")
        else:
            entries = data["entries"]

            # ── Section A : Overall Team Performance ──────────────
            st.markdown('<div class="section-title">Overall Team Performance</div>', unsafe_allow_html=True)

            # status counts
            sc = {}
            for e in entries:
                sc[e["status"]] = sc.get(e["status"], 0) + 1

            col_donut, col_legend = st.columns([1, 1.6])
            with col_donut:
                fig_ov = donut(
                    list(sc.keys()), list(sc.values()),
                    [STATUS_COLORS.get(s, "#ccc") for s in sc.keys()],
                    size=260
                )
                st.plotly_chart(fig_ov, use_container_width=True, key="chart_overall")

            with col_legend:
                st.markdown("<br>", unsafe_allow_html=True)
                total_e = len(entries)
                for s in STATUS_OPTIONS:
                    cnt  = sc.get(s, 0)
                    pct  = round(cnt / total_e * 100) if total_e else 0
                    w    = max(2, pct)
                    col  = STATUS_COLORS.get(s, "#ccc")
                    bg   = STATUS_BG.get(s, "#f5f5f5")
                    st.markdown(f"""
                    <div style="margin-bottom:10px;">
                      <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                        <div style="width:10px;height:10px;border-radius:3px;background:{col};flex-shrink:0;"></div>
                        <span style="font-size:12px;font-weight:600;flex:1;">{s}</span>
                        <span style="font-size:13px;font-weight:700;color:{col};">{cnt}</span>
                        <span style="font-size:11px;color:#9C9890;min-width:34px;text-align:right;">{pct}%</span>
                      </div>
                      <div style="background:#F0EDE8;border-radius:4px;height:5px;overflow:hidden;">
                        <div style="width:{w}%;height:100%;background:{col};border-radius:4px;transition:width 0.4s;"></div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── Section B : Director Workload ─────────────────────
            st.markdown('<div class="section-title">🎯 Director Workload — Who Occupied the Team Most</div>', unsafe_allow_html=True)

            # Build director map: {director: {count, members: {name: count}}}
            dir_map = {}
            for e in entries:
                key = e.get("director") or "Unassigned"
                mn  = (get_member(data, e["member_id"]) or {}).get("name", "Unknown")
                if key not in dir_map:
                    dir_map[key] = {"count": 0, "members": {}}
                dir_map[key]["count"] += 1
                dir_map[key]["members"][mn] = dir_map[key]["members"].get(mn, 0) + 1

            dir_list = sorted(dir_map.items(), key=lambda x: x[1]["count"], reverse=True)
            dir_names  = [d[0] for d in dir_list]
            dir_counts = [d[1]["count"] for d in dir_list]
            dir_colors_list = [DIR_PALETTE[i % len(DIR_PALETTE)] for i in range(len(dir_list))]

            # Left: overall donut + legend  |  Right: per-director donuts
            dcol1, dcol2 = st.columns([1, 2])

            with dcol1:
                fig_dir_ov = donut(dir_names, dir_counts, dir_colors_list, size=240)
                st.plotly_chart(fig_dir_ov, use_container_width=True, key="chart_dir_overall")
                total_dir = sum(dir_counts)
                for i, (dname, ddata) in enumerate(dir_list):
                    col = dir_colors_list[i]
                    pct = round(ddata["count"] / total_dir * 100) if total_dir else 0
                    # member breakdown inside each director
                    mb_html = "".join(
                        f'<span style="font-size:10px;color:#5C5952;margin-right:8px;">▸ {mn}: <b>{cnt}</b></span>'
                        for mn, cnt in sorted(ddata["members"].items(), key=lambda x: -x[1])
                    )
                    st.markdown(f"""
                    <div style="margin-bottom:10px;padding:10px 12px;background:#FAFAF8;border:1px solid #E4E1D9;border-radius:8px;">
                      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <div style="width:10px;height:10px;border-radius:3px;background:{col};flex-shrink:0;"></div>
                        <span style="font-size:12px;font-weight:700;flex:1;">{dname}</span>
                        <span style="font-size:15px;font-weight:700;color:{col};">{ddata['count']}</span>
                        <span style="font-size:11px;color:#9C9890;">{pct}%</span>
                      </div>
                      <div style="flex-wrap:wrap;">{mb_html}</div>
                    </div>""", unsafe_allow_html=True)

            with dcol2:
                # Per-director mini donuts showing member breakdown
                if len(dir_list) > 0:
                    dc_cols = st.columns(min(len(dir_list), 3))
                    for i, (dname, ddata) in enumerate(dir_list):
                        mb_list   = sorted(ddata["members"].items(), key=lambda x: -x[1])
                        mb_names  = [x[0] for x in mb_list]
                        mb_vals   = [x[1] for x in mb_list]
                        mb_colors = [MB_PALETTE[j % len(MB_PALETTE)] for j in range(len(mb_list))]
                        with dc_cols[i % min(len(dir_list), 3)]:
                            st.markdown(f"""
                            <div style="text-align:center;margin-bottom:6px;">
                              <span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:{dir_colors_list[i]};vertical-align:middle;"></span>
                              <span style="font-size:12px;font-weight:700;margin-left:6px;">{dname}</span>
                            </div>""", unsafe_allow_html=True)
                            fig_di = donut(mb_names, mb_vals, mb_colors, size=200)
                            st.plotly_chart(fig_di, use_container_width=True, key=f"chart_dir_{i}")
                            for j, (mn, cnt) in enumerate(mb_list):
                                st.markdown(f"""
                                <div style="display:flex;align-items:center;gap:7px;font-size:11px;margin-bottom:3px;">
                                  <div style="width:8px;height:8px;border-radius:50%;background:{mb_colors[j]};flex-shrink:0;"></div>
                                  <span style="flex:1;color:#5C5952;">{mn}</span>
                                  <strong>{cnt}</strong>
                                </div>""", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── Section C : Individual Performance ────────────────
            st.markdown('<div class="section-title">Individual Performance</div>', unsafe_allow_html=True)

            n_members = len(data["members"])
            n_cols    = min(4, n_members)
            ind_cols  = st.columns(n_cols)

            for i, m in enumerate(data["members"]):
                m_ent = member_entries(data, m["id"])
                m_sc  = {}
                for e in m_ent:
                    m_sc[e["status"]] = m_sc.get(e["status"], 0) + 1

                with ind_cols[i % n_cols]:
                    # Member chip
                    mc = MB_PALETTE[i % len(MB_PALETTE)]
                    st.markdown(f"""
                    <div style="text-align:center;margin-bottom:8px;">
                      <div style="width:36px;height:36px;border-radius:50%;background:{mc};
                        color:#fff;font-size:12px;font-weight:700;display:inline-flex;
                        align-items:center;justify-content:center;margin-bottom:4px;">{m['initials']}</div>
                      <div style="font-size:12px;font-weight:700;color:#1C1B18;">{m['name']}</div>
                    </div>""", unsafe_allow_html=True)

                    if m_sc:
                        labs   = list(m_sc.keys())
                        vals   = list(m_sc.values())
                        colors = [STATUS_COLORS.get(s,"#ccc") for s in labs]
                        fig_m  = donut(labs, vals, colors, size=180)
                        st.plotly_chart(fig_m, use_container_width=True, key=f"chart_ind_{m['id']}")
                        for s, cnt in sorted(m_sc.items(), key=lambda x: -x[1]):
                            col = STATUS_COLORS.get(s,"#ccc")
                            st.markdown(f"""
                            <div style="display:flex;align-items:center;gap:6px;font-size:11px;margin-bottom:3px;">
                              <div style="width:8px;height:8px;border-radius:50%;background:{col};flex-shrink:0;"></div>
                              <span style="flex:1;color:#5C5952;">{s}</span>
                              <strong>{cnt}</strong>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align:center;color:#9C9890;font-size:12px;padding:20px 0;'>No entries yet</div>",
                                    unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── Section D : Project Breakdown ─────────────────────
            st.markdown('<div class="section-title">📁 Project Activity Breakdown</div>', unsafe_allow_html=True)

            proj_map = {}
            for e in entries:
                pn = e.get("project") or "Unassigned"
                if pn not in proj_map:
                    proj_map[pn] = {"count": 0, "statuses": {}, "members": set()}
                proj_map[pn]["count"] += 1
                proj_map[pn]["statuses"][e["status"]] = proj_map[pn]["statuses"].get(e["status"], 0) + 1
                m = get_member(data, e["member_id"])
                if m: proj_map[pn]["members"].add(m["name"])

            proj_sorted = sorted(proj_map.items(), key=lambda x: -x[1]["count"])
            proj_names  = [p[0] for p in proj_sorted]
            proj_counts = [p[1]["count"] for p in proj_sorted]
            proj_colors = [DIR_PALETTE[i % len(DIR_PALETTE)] for i in range(len(proj_sorted))]

            if proj_names:
                fig_proj = hbar(proj_names, proj_counts, proj_colors, "Entries")
                st.plotly_chart(fig_proj, use_container_width=True, key="chart_projects")

                # Mini table
                proj_rows = []
                for pn, pd_data in proj_sorted:
                    top_s = max(pd_data["statuses"], key=pd_data["statuses"].get) if pd_data["statuses"] else "—"
                    proj_rows.append({
                        "Project":       pn,
                        "Total Entries": pd_data["count"],
                        "Top Status":    top_s,
                        "Members":       ", ".join(sorted(pd_data["members"])),
                    })
                st.dataframe(pd.DataFrame(proj_rows), use_container_width=True, hide_index=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── Section E : Activity Timeline ─────────────────────
            st.markdown('<div class="section-title">📈 Activity Timeline — Entries per Day</div>', unsafe_allow_html=True)

            # Group entries by date
            date_map = {}
            for e in entries:
                date_map[e["date"]] = date_map.get(e["date"], 0) + 1

            if date_map:
                dates      = sorted(date_map.keys())
                date_vals  = [date_map[d] for d in dates]
                date_labels = [fmt_date(d) for d in dates]

                fig_tl = go.Figure()
                fig_tl.add_trace(go.Scatter(
                    x=date_labels, y=date_vals,
                    mode="lines+markers",
                    line=dict(color="#C17B3C", width=2.5),
                    marker=dict(size=7, color="#C17B3C",
                                line=dict(color="#fff", width=2)),
                    fill="tozeroy",
                    fillcolor="rgba(193,123,60,0.08)",
                    hovertemplate="<b>%{x}</b><br>%{y} entries<extra></extra>",
                ))
                fig_tl.update_layout(
                    **PLOTLY_LAYOUT,
                    height=260,
                    xaxis=dict(showgrid=False, tickangle=-35, tickfont=dict(size=10)),
                    yaxis=dict(showgrid=True, gridcolor="#F0EDE8", zeroline=False, title="Entries"),
                )
                st.plotly_chart(fig_tl, use_container_width=True, key="chart_timeline")

    # ══════════════════════════════════════════════════════════════
    # TAB 3 — ATTENDANCE CALENDAR
    # ══════════════════════════════════════════════════════════════
    with tab_calendar:
        st.markdown('<div class="section-title">Attendance Calendar</div>', unsafe_allow_html=True)

        cal_names = [m["name"] for m in data["members"]]
        cal_name  = st.selectbox("Select Member", cal_names, key="cal_member")
        cal_m     = next(m for m in data["members"] if m["name"] == cal_name)

        today_dt = date.today()
        cy_col, cm_col = st.columns(2)
        with cy_col:
            cal_year  = st.selectbox("Year", list(range(today_dt.year-1, today_dt.year+2)),
                                     index=1, key="cal_year")
        with cm_col:
            cal_month = st.selectbox("Month", list(range(1, 13)), index=today_dt.month-1,
                                     format_func=lambda mn: datetime(cal_year, mn, 1).strftime("%B"),
                                     key="cal_month_sel")

        prefix    = f"{cal_year}-{str(cal_month).zfill(2)}"
        emap      = {e["date"]: e for e in data["entries"]
                     if e["member_id"] == cal_m["id"] and e["date"].startswith(prefix)}

        last_day  = (date(cal_year, cal_month % 12 + 1, 1) - timedelta(days=1)).day if cal_month < 12 else 31
        start_wd  = (date(cal_year, cal_month, 1).weekday() + 1) % 7  # Sun=0

        CAL_COLORS = {
            "Submitted":   ("#C8ECD8","#1A5C35","#A8D8BB"),
            "In Progress": ("#D4E5F7","#1A4A7A","#B0CCE8"),
            "Pending":     ("#FDECD5","#7A4A1A","#F0C89A"),
            "Leave":       ("#FAD8D8","#7A2020","#F0B0B0"),
            "Correction":  ("#FDE8D0","#7A3810","#F0C09A"),
            "Holiday":     ("#EDE8FB","#3D2080","#C4B0E8"),
        }
        DAY_HDRS = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

        # Render header
        hcols = st.columns(7)
        for i, dl in enumerate(DAY_HDRS):
            hcols[i].markdown(
                f"<div style='text-align:center;font-size:10px;font-weight:700;color:#9C9890;"
                f"padding:4px 0;text-transform:uppercase;letter-spacing:0.5px;'>{dl}</div>",
                unsafe_allow_html=True)

        cells = [""] * start_wd + [str(d) for d in range(1, last_day+1)]
        while len(cells) % 7: cells.append("")

        for row_start in range(0, len(cells), 7):
            row   = cells[row_start:row_start+7]
            rcols = st.columns(7)
            for i, day_str in enumerate(row):
                with rcols[i]:
                    if not day_str:
                        st.markdown("<div style='height:42px;'></div>", unsafe_allow_html=True)
                    else:
                        ds     = f"{prefix}-{day_str.zfill(2)}"
                        entry  = emap.get(ds)
                        status = entry["status"] if entry else None
                        future = ds > today_dt.isoformat()
                        is_today = ds == today_dt.isoformat()

                        if future:
                            bg, fg, border = "#F7F6F2", "#C8C5BC", "1px solid #E4E1D9"
                        elif status and status in CAL_COLORS:
                            bg, fg, bc = CAL_COLORS[status]
                            border = f"1px solid {bc}"
                        else:
                            bg, fg, border = "#FAFAF8", "#9C9890", "1px solid #E4E1D9"

                        if is_today:
                            border = "2px solid #C17B3C"

                        opacity = "0.45" if future else "1"
                        tip     = status or "No entry"
                        st.markdown(
                            f"<div title='{ds}: {tip}' style='background:{bg};border:{border};"
                            f"border-radius:7px;text-align:center;padding:8px 2px;"
                            f"font-size:12px;font-family:JetBrains Mono,monospace;color:{fg};"
                            f"opacity:{opacity};cursor:default;'>{day_str}</div>",
                            unsafe_allow_html=True)

        # Legend
        st.markdown("<br>", unsafe_allow_html=True)
        leg_items = list(CAL_COLORS.items()) + [("No Entry", ("#FAFAF8","#9C9890","#E4E1D9"))]
        lcols = st.columns(len(leg_items))
        for i, (s, colors) in enumerate(leg_items):
            bg = colors[0]; bc = colors[2] if len(colors) > 2 else "#E4E1D9"
            lcols[i].markdown(
                f"<div style='display:flex;align-items:center;gap:5px;font-size:11px;color:#5C5952;'>"
                f"<div style='width:11px;height:11px;border-radius:3px;background:{bg};"
                f"border:1px solid {bc};flex-shrink:0;'></div>{s}</div>",
                unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # TAB 4 — HOURS LOGGED
    # ══════════════════════════════════════════════════════════════
    with tab_hours:
        st.markdown('<div class="section-title">Hours Logged by Member</div>', unsafe_allow_html=True)
        range_sel = st.radio("Range", ["This Week", "This Month", "All Time"],
                             horizontal=True, key="hours_range")
        today_dt = date.today()
        if   range_sel == "This Week":  from_dt = (today_dt - timedelta(days=(today_dt.weekday()+1)%7)).isoformat()
        elif range_sel == "This Month": from_dt = today_dt.strftime("%Y-%m-01")
        else: from_dt = ""

        h_cols = st.columns(min(4, len(data["members"])))
        all_h_names, all_h_vals, all_h_cols2 = [], [], []

        for i, m in enumerate(data["members"]):
            m_ent = [e for e in data["entries"]
                     if e["member_id"] == m["id"] and (not from_dt or e["date"] >= from_dt)]
            total_mins = sum(calc_mins(e.get("time_from",""), e.get("time_to","")) for e in m_ent)
            h, mn   = divmod(total_mins, 60)
            ts      = f"{h}h {mn}m" if (h and mn) else (f"{h}h" if h else (f"{mn}m" if mn else "0h"))
            mc      = MB_PALETTE[i % len(MB_PALETTE)]
            with h_cols[i % 4]:
                st.markdown(f"""
                <div class="dar-card" style="padding:16px 18px;">
                  <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:36px;height:36px;border-radius:50%;background:{mc};
                      color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;
                      justify-content:center;flex-shrink:0;">{m['initials']}</div>
                    <div>
                      <div style="font-size:12px;font-weight:600;color:#1C1B18;">{m['name']}</div>
                      <div style="font-size:20px;font-weight:700;color:#C17B3C;
                        font-family:'JetBrains Mono',monospace;letter-spacing:-0.5px;">{ts}</div>
                      <div style="font-size:10px;color:#9C9890;">{len(m_ent)} entries</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)
            all_h_names.append(m["name"])
            all_h_vals.append(total_mins)
            all_h_cols2.append(mc)

        st.markdown("<br>", unsafe_allow_html=True)
        if any(v > 0 for v in all_h_vals):
            fig_h = hbar(all_h_names, [round(v/60, 1) for v in all_h_vals], all_h_cols2, "Hours")
            fig_h.update_layout(height=max(240, 50*len(all_h_names)+80))
            st.plotly_chart(fig_h, use_container_width=True, key="chart_hours")

    # ══════════════════════════════════════════════════════════════
    # TAB 5 — SETTINGS
    # ══════════════════════════════════════════════════════════════
    with tab_settings:
        st.markdown('<div class="section-title">Change Admin Password</div>', unsafe_allow_html=True)
        st.info(f"ℹ Only **{ADMIN_MEMBER}** can change the admin password. Verify your identity first.")

        chetan = get_member(data, next((m["id"] for m in data["members"] if m["name"] == ADMIN_MEMBER), -1))

        if not chetan:
            st.warning(f"Member '{ADMIN_MEMBER}' not found.")
        elif not st.session_state.chetan_verified:
            v_input = st.text_input(f"{ADMIN_MEMBER}'s PIN or current admin password",
                                    type="password", key="chetan_v_input")
            if st.button("Verify Identity", type="primary", key="chetan_verify_btn"):
                pin_hash  = data.get("member_pins", {}).get(str(chetan["id"]), "")
                pw_stored = data.get("admin_pw_hash", "")
                entered   = hash_pw(v_input)
                if (pin_hash and entered == pin_hash) or entered == pw_stored:
                    st.session_state.chetan_verified = True
                    st.rerun()
                else:
                    st.error("Verification failed.")
        else:
            pw1 = st.text_input("New Admin Password",    type="password", key="new_pw1")
            pw2 = st.text_input("Confirm New Password",  type="password", key="new_pw2")
            ca, cb = st.columns(2)
            with ca:
                if st.button("✅ Update Password", type="primary", key="update_pw_btn"):
                    if len(pw1) < 4:        st.error("Minimum 4 characters.")
                    elif pw1 != pw2:        st.error("Passwords don't match.")
                    else:
                        data["admin_pw_hash"] = hash_pw(pw1)
                        persist()
                        st.session_state.chetan_verified = False
                        st.success("✅ Password updated!")
            with cb:
                if st.button("Cancel", key="cancel_pw"):
                    st.session_state.chetan_verified = False
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Member PINs</div>', unsafe_allow_html=True)

        pin_name = st.selectbox("Member", [m["name"] for m in data["members"]], key="pin_sel")
        pin_m    = next(m for m in data["members"] if m["name"] == pin_name)
        has_pin  = str(pin_m["id"]) in data.get("member_pins", {})
        st.caption(f"Status: {'🔑 PIN is set' if has_pin else '🔓 No PIN set'}")

        pc1, pc2 = st.columns(2)
        with pc1:
            new_pin = st.text_input("New PIN (4 digits)", max_chars=4, type="password",
                                    key="new_pin_input", placeholder="••••")
            if st.button("Set PIN", key="set_pin_btn"):
                if len(new_pin) == 4 and new_pin.isdigit():
                    data.setdefault("member_pins", {})[str(pin_m["id"])] = hash_pw(new_pin)
                    persist(); st.success(f"✅ PIN set for {pin_name}"); st.rerun()
                else:
                    st.error("PIN must be exactly 4 digits.")
        with pc2:
            if has_pin:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔓 Remove PIN", key="remove_pin_btn"):
                    data["member_pins"].pop(str(pin_m["id"]), None)
                    persist(); st.success(f"PIN removed for {pin_name}"); st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Manage Members</div>', unsafe_allow_html=True)
        for m in data["members"]:
            mc1, mc2, mc3 = st.columns([3, 1.5, 0.8])
            with mc1:
                new_n = st.text_input("", value=m["name"], key=f"rename_{m['id']}",
                                      label_visibility="collapsed")
            with mc2:
                if st.button("Rename", key=f"do_rename_{m['id']}"):
                    s = new_n.strip()
                    if s and s != m["name"]:
                        m["name"] = s
                        m["initials"] = "".join(w[0].upper() for w in s.split())[:2]
                        persist(); st.success(f"Renamed → {s}"); st.rerun()
            with mc3:
                if st.button("🗑", key=f"del_mem_{m['id']}", help=f"Delete {m['name']}"):
                    data["members"] = [x for x in data["members"] if x["id"] != m["id"]]
                    data["entries"] = [e for e in data["entries"] if e["member_id"] != m["id"]]
                    data.get("member_pins", {}).pop(str(m["id"]), None)
                    if st.session_state.current_view == m["id"]:
                        st.session_state.current_view = data["members"][0]["id"] if data["members"] else "admin"
                    persist(); st.success(f"Deleted {m['name']}"); st.rerun()


# ─────────────────────────────────────────────────────────────────────
# MEMBER PAGE
# ─────────────────────────────────────────────────────────────────────
def render_member(mid):
    m = get_member(data, mid)
    if not m:
        st.error("Member not found.")
        return

    # ── PIN gate ──────────────────────────────────────────────────
    pin_key = str(m["id"])
    has_pin = pin_key in data.get("member_pins", {})
    if has_pin and mid not in st.session_state.pin_unlocked_for:
        col = st.columns([1, 1.2, 1])[1]
        with col:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="dar-card" style="text-align:center;padding:32px;">
              <div style="font-size:36px;margin-bottom:10px;">🔑</div>
              <div class="page-title" style="font-size:17px;">{m['name']}'s Report</div>
              <div class="page-subtitle">Enter your 4-digit PIN</div>
            </div>""", unsafe_allow_html=True)
            pin_in = st.text_input("PIN", max_chars=4, type="password",
                                   key=f"pin_input_{mid}", label_visibility="collapsed",
                                   placeholder="••••")
            ca, cb = st.columns(2)
            with ca:
                if st.button("Unlock →", type="primary", key=f"pin_unlock_{mid}", use_container_width=True):
                    if hash_pw(pin_in) == data["member_pins"][pin_key]:
                        st.session_state.pin_unlocked_for.add(mid)
                        st.rerun()
                    else:
                        st.error("Incorrect PIN.")
            with cb:
                if st.button("Skip", key=f"pin_skip_{mid}", use_container_width=True):
                    st.session_state.pin_unlocked_for.add(mid)
                    st.rerun()
        return

    # ── Header ────────────────────────────────────────────────────
    today_iso = date.today().isoformat()
    has_today = any(e["date"] == today_iso and e["member_id"] == mid for e in data["entries"])
    m_color   = MB_PALETTE[next((i for i,x in enumerate(data["members"]) if x["id"]==mid), 0) % len(MB_PALETTE)]

    hcol1, hcol2 = st.columns([1, 8])
    with hcol1:
        st.markdown(f"""<div style="width:48px;height:48px;border-radius:50%;background:{m_color};
          color:#fff;font-size:16px;font-weight:700;display:flex;align-items:center;
          justify-content:center;margin-top:4px;">{m['initials']}</div>""", unsafe_allow_html=True)
    with hcol2:
        st.markdown(f'<div class="page-title">{m["name"]}\'s Daily Report</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="page-subtitle">Fill in your daily activity for the team record</div>', unsafe_allow_html=True)

    if not has_today:
        st.warning("⚠  No DAR submitted for today yet. Please fill in your activity below.")

    # ── New Entry Form ─────────────────────────────────────────────
    with st.expander("📝  New Entry", expanded=True):
        c1, c2 = st.columns(2)
        with c1: entry_date = st.date_input("Date", value=date.today(), key=f"f_date_{mid}")
        with c2: f_status   = st.selectbox("Status", STATUS_OPTIONS, key=f"f_status_{mid}")

        f_task = st.text_area("Daily Task / Activity *",
                              placeholder="Describe what you worked on today...",
                              key=f"f_task_{mid}", height=90)

        c3, c4 = st.columns(2)
        with c3: f_director = st.selectbox("Director", [""] + DIRECTORS, key=f"f_director_{mid}")
        with c4: f_designer  = st.text_input("Designer", key=f"f_designer_{mid}", placeholder=m["name"])

        c5, c6, c7 = st.columns(3)
        with c5:
            f_project = st.text_input("Project", key=f"f_project_{mid}", placeholder="e.g. GENERAC")
            projects  = all_projects(data)
            if projects:
                pp = st.selectbox("Pick recent ▾", ["—"] + projects, key=f"pp_{mid}",
                                  label_visibility="collapsed")
                if pp != "—" and not st.session_state.get(f"f_project_{mid}", "").strip():
                    f_project = pp
        with c6: f_new_proj = st.text_input("New Project", key=f"f_newproject_{mid}")
        with c7: f_notes    = st.text_input("Notes / What's New", key=f"f_notes_{mid}")

        c8, c9 = st.columns(2)
        with c8: f_from = st.text_input("Time From (HH:MM)", placeholder="09:00", key=f"f_from_{mid}")
        with c9: f_to   = st.text_input("Time To   (HH:MM)", placeholder="18:00", key=f"f_to_{mid}")

        total_t = calc_time(f_from, f_to)
        if total_t:
            st.markdown(f"<div style='font-size:12px;color:#C17B3C;font-weight:600;margin-top:2px;'>⏱  Total: {total_t}</div>", unsafe_allow_html=True)

        bc1, _, bc3 = st.columns([1.6, 1, 1])
        with bc1:
            if st.button("⟳  Copy from Last Entry", key=f"copy_y_{mid}"):
                prev = sorted(member_entries(data, mid), key=lambda e: e["date"], reverse=True)
                if prev:
                    p = prev[0]
                    for k, v in [
                        (f"f_task_{mid}",     p.get("task","")),
                        (f"f_designer_{mid}", p.get("designer","")),
                        (f"f_project_{mid}",  p.get("project","")),
                        (f"f_from_{mid}",     p.get("time_from","")),
                        (f"f_to_{mid}",       p.get("time_to","")),
                    ]: st.session_state[k] = v
                    if p.get("director","") in DIRECTORS:
                        st.session_state[f"f_director_{mid}"] = p["director"]
                    st.rerun()
                else:
                    st.warning("No previous entries to copy from.")
        with bc3:
            if st.button("Save Entry →", type="primary", key=f"save_{mid}"):
                task_val = st.session_state.get(f"f_task_{mid}", "").strip()
                if not task_val:
                    st.error("Please describe the task.")
                else:
                    data["entries"].append({
                        "id":          uid(),
                        "member_id":   mid,
                        "date":        entry_date.isoformat(),
                        "task":        task_val,
                        "director":    st.session_state.get(f"f_director_{mid}", ""),
                        "designer":    st.session_state.get(f"f_designer_{mid}", m["name"]),
                        "project":     st.session_state.get(f"f_project_{mid}", ""),
                        "new_project": st.session_state.get(f"f_newproject_{mid}", ""),
                        "time_from":   st.session_state.get(f"f_from_{mid}", ""),
                        "time_to":     st.session_state.get(f"f_to_{mid}", ""),
                        "status":      st.session_state.get(f"f_status_{mid}", "In Progress"),
                        "notes":       st.session_state.get(f"f_notes_{mid}", ""),
                    })
                    persist()
                    for k in [f"f_task_{mid}", f"f_project_{mid}", f"f_newproject_{mid}",
                               f"f_from_{mid}", f"f_to_{mid}", f"f_notes_{mid}", f"f_designer_{mid}"]:
                        st.session_state.pop(k, None)
                    st.success("✅ Entry saved!")
                    st.rerun()

    # ── Recent Entries ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Daily Reports</div>', unsafe_allow_html=True)

    sc1, sc2 = st.columns([2.5, 1])
    with sc1:
        search = st.text_input("🔍", key=f"srch_{mid}", placeholder="Search task, project...",
                               label_visibility="collapsed")
    with sc2:
        mo_opts = sorted(set(e["date"][:7] for e in member_entries(data, mid)), reverse=True)
        sel_mo  = st.selectbox("Month", ["All"] + mo_opts, key=f"mo_{mid}",
                               format_func=lambda x: x if x=="All" else datetime.strptime(x,"%Y-%m").strftime("%b %Y"),
                               label_visibility="collapsed")

    rows = sorted(member_entries(data, mid), key=lambda e: e["date"], reverse=True)
    if search:
        q    = search.lower()
        rows = [e for e in rows if q in (e.get("task","") + e.get("project","") + e.get("director","")).lower()]
    if sel_mo != "All":
        rows = [e for e in rows if e["date"].startswith(sel_mo)]

    if not rows:
        st.markdown("""
        <div style="text-align:center;padding:48px 24px;color:#9C9890;">
          <div style="font-size:36px;margin-bottom:10px;opacity:0.4;">📄</div>
          <div style="font-size:13px;">No entries yet. Fill in your first daily report above!</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Column headers
        th = st.columns([1.4, 3.5, 1.5, 1.5, 1.3, 1.8, 0.5])
        for col, lbl in zip(th, ["Date","Task","Project","Director","Time","Status",""]):
            col.markdown(f"<div style='font-size:10px;font-weight:700;text-transform:uppercase;"
                         f"letter-spacing:0.5px;color:#9C9890;padding:4px 0;'>{lbl}</div>",
                         unsafe_allow_html=True)
        st.markdown("<div style='border-top:1px solid #E4E1D9;margin-bottom:6px;'></div>",
                    unsafe_allow_html=True)

        for e in rows:
            total     = calc_time(e.get("time_from",""), e.get("time_to",""))
            badge_cls = e["status"].lower().replace(" ","-")
            rc = st.columns([1.4, 3.5, 1.5, 1.5, 1.3, 1.8, 0.5])
            rc[0].markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:11px;"
                           f"color:#5C5952;padding-top:4px;'>{fmt_date(e['date'])}</div>",
                           unsafe_allow_html=True)
            rc[1].markdown(f"<div style='font-size:13px;color:#1C1B18;padding-top:3px;'>{e.get('task','—')}</div>",
                           unsafe_allow_html=True)
            rc[2].markdown(f"<div style='font-size:12px;color:#5C5952;padding-top:4px;'>{e.get('project','—')}</div>",
                           unsafe_allow_html=True)
            rc[3].markdown(f"<div style='font-size:12px;color:#5C5952;padding-top:4px;'>{e.get('director','—')}</div>",
                           unsafe_allow_html=True)
            rc[4].markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:11px;"
                           f"color:#5C5952;padding-top:4px;'>{total or '—'}</div>",
                           unsafe_allow_html=True)
            rc[5].markdown(f"<div style='padding-top:3px;'><span class='badge badge-{badge_cls}'>{e['status']}</span></div>",
                           unsafe_allow_html=True)
            with rc[6]:
                if st.button("✕", key=f"del_{e['id']}", help="Delete entry"):
                    data["entries"] = [x for x in data["entries"] if x["id"] != e["id"]]
                    persist()
                    st.rerun()

            if e.get("notes"):
                st.markdown(f"<div style='font-size:11px;color:#9C9890;padding:1px 0 4px 0;'>"
                            f"📝 {e['notes']}</div>", unsafe_allow_html=True)
            st.markdown("<div style='border-top:1px solid #F0EDE8;margin:4px 0;'></div>",
                        unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────
view = st.session_state.current_view
if view == "admin":
    render_admin()
else:
    render_member(view)
