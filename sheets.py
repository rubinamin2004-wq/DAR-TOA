"""
Google Sheets integration for DAR Portal.

Authentication:
    Place your Google service account JSON key file at one of:
        - ./credentials.json
        - ./service_account.json

    OR set the following in your .streamlit/secrets.toml:
        [gcp_service_account]
        type = "service_account"
        project_id = "..."
        private_key_id = "..."
        private_key = "..."
        client_email = "..."
        client_id = "..."
        auth_uri = "..."
        token_uri = "..."
        auth_provider_x509_cert_url = "..."
        client_x509_cert_url = "..."

    And set SPREADSHEET_ID in secrets.toml:
        SPREADSHEET_ID = "your_google_sheet_id_here"

Google Sheet Setup:
    Sheet 1 name: USERS
    Columns: Username | Password | Role

    Sheet 2 name: REPORTS
    Columns: ID | Username | Date | Daily Task / Activity | Status |
             Director | Designer | Project | New Project | Notes |
             Time From | Time To | Created Timestamp
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

# ─── Config ───────────────────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_ID = None  # Will be loaded from secrets or env

# Sheet names
USERS_SHEET = "USERS"
REPORTS_SHEET = "REPORTS"

REPORT_COLUMNS = [
    "ID", "Username", "Date", "Daily Task / Activity", "Status",
    "Director", "Designer", "Project", "New Project", "Notes",
    "Time From", "Time To", "Created Timestamp"
]

USER_COLUMNS = ["Username", "Password", "Role"]


# ─── Connection ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_client():
    """Return an authenticated gspread client, or None if credentials missing."""
    if not GSPREAD_AVAILABLE:
        return None

    creds_dict = None

    # 1. Try Streamlit secrets
    try:
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
    except Exception:
        pass

    # 2. Try local JSON files
    if creds_dict is None:
        for path in ["credentials.json", "service_account.json"]:
            if os.path.exists(path):
                with open(path) as f:
                    creds_dict = json.load(f)
                break

    if creds_dict is None:
        st.error(
            "Google Sheets credentials not found. Add a [gcp_service_account] "
            "section to .streamlit/secrets.toml, or place credentials.json / "
            "service_account.json in the app's working directory."
        )
        return None

    try:
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Google Sheets auth error: {e}")
        return None


def get_spreadsheet_id():
    try:
        return st.secrets.get("SPREADSHEET_ID", None)
    except Exception:
        return os.environ.get("SPREADSHEET_ID", None)


def get_sheet(sheet_name: str):
    """Return a gspread worksheet object."""
    client = get_client()
    if client is None:
        return None
    sid = get_spreadsheet_id()
    if not sid:
        return None
    try:
        spreadsheet = client.open_by_key(sid)
        return spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        # Create sheet with headers
        spreadsheet = client.open_by_key(sid)
        cols = REPORT_COLUMNS if sheet_name == REPORTS_SHEET else USER_COLUMNS
        ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(cols))
        ws.append_row(cols)
        return ws
    except Exception as e:
        st.error(f"Error accessing sheet '{sheet_name}': {e}")
        return None


def sheet_to_df(ws) -> pd.DataFrame | None:
    """Convert worksheet to DataFrame, returning None on failure."""
    try:
        data = ws.get_all_records()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except Exception:
        return None


# ─── Authentication ───────────────────────────────────────────────────────────
def debug_users_sheet() -> dict:
    """Diagnostic helper: shows exactly what authenticate_user sees.
    Call this from app.py (e.g. behind a temporary debug button) to see
    why login is failing."""
    ws = get_sheet(USERS_SHEET)
    if ws is None:
        return {"error": "Could not open USERS worksheet (check sheet name and SPREADSHEET_ID)"}
    df = sheet_to_df(ws)
    if df is None:
        return {"error": "sheet_to_df failed (check sheet has a header row)"}
    if df.empty:
        return {"error": "USERS sheet returned no rows"}
    df.columns = [c.strip() for c in df.columns]
    return {
        "worksheet_title": ws.title,
        "columns_found": list(df.columns),
        "row_count": len(df),
        "sample_rows": [
            {
                "username_repr": repr(str(r.get("Username", "<missing>"))),
                "password_repr": repr(str(r.get("Password", "<missing>"))),
                "role": r.get("Role", "<missing>"),
            }
            for _, r in df.head(5).iterrows()
        ],
    }


def authenticate_user(username: str, password: str) -> dict | None:
    """Return user dict if credentials match, else None."""
    ws = get_sheet(USERS_SHEET)
    if ws is None:
        return None

    df = sheet_to_df(ws)
    if df is None or df.empty:
        return None

    df.columns = [c.strip() for c in df.columns]
    if "Username" not in df.columns or "Password" not in df.columns:
        st.error("USERS sheet is missing required 'Username' or 'Password' columns.")
        return None
    match = df[
        (df["Username"].astype(str).str.strip() == username.strip()) &
        (df["Password"].astype(str).str.strip() == password.strip())
    ]
    if match.empty:
        return None
    row = match.iloc[0]
    return {"username": row["Username"], "role": row["Role"]}


# ─── Users ────────────────────────────────────────────────────────────────────
def get_all_users() -> pd.DataFrame | None:
    ws = get_sheet(USERS_SHEET)
    if ws is None:
        return None
    return sheet_to_df(ws)


def add_user(username: str, password: str, role: str) -> bool:
    ws = get_sheet(USERS_SHEET)
    if ws is None:
        return False
    try:
        df = sheet_to_df(ws)
        if df is not None and not df.empty:
            if username in df["Username"].astype(str).values:
                return False
        ws.append_row([username, password, role])
        return True
    except Exception:
        return False


def delete_user(username: str) -> bool:
    ws = get_sheet(USERS_SHEET)
    if ws is None:
        return False
    try:
        df = sheet_to_df(ws)
        if df is None:
            return False
        # Find row index (gspread rows are 1-indexed, +1 for header)
        match_idx = df.index[df["Username"].astype(str) == username].tolist()
        if not match_idx:
            return False
        row_num = match_idx[0] + 2  # +1 for header, +1 for 0-index
        ws.delete_rows(row_num)
        return True
    except Exception:
        return False


def update_password(username: str, new_password: str) -> bool:
    ws = get_sheet(USERS_SHEET)
    if ws is None:
        return False
    try:
        df = sheet_to_df(ws)
        if df is None:
            return False
        match_idx = df.index[df["Username"].astype(str) == username].tolist()
        if not match_idx:
            return False
        row_num = match_idx[0] + 2
        # Password is column B (col index 2)
        ws.update_cell(row_num, 2, new_password)
        return True
    except Exception:
        return False


# ─── Reports ──────────────────────────────────────────────────────────────────
def get_all_reports() -> pd.DataFrame | None:
    ws = get_sheet(REPORTS_SHEET)
    if ws is None:
        return None
    df = sheet_to_df(ws)
    if df is None:
        return pd.DataFrame(columns=REPORT_COLUMNS)
    return df


def get_user_reports(username: str) -> pd.DataFrame | None:
    df = get_all_reports()
    if df is None or df.empty:
        return df
    if "Username" not in df.columns:
        return pd.DataFrame(columns=REPORT_COLUMNS)
    return df[df["Username"].astype(str) == username].copy()


def get_report_by_id(report_id: str) -> dict | None:
    df = get_all_reports()
    if df is None or df.empty:
        return None
    match = df[df["ID"].astype(str) == str(report_id)]
    if match.empty:
        return None
    return match.iloc[0].to_dict()


def submit_report(report_id, username, date, task, status, director,
                  designer, project, new_project, notes, time_from, time_to) -> bool:
    ws = get_sheet(REPORTS_SHEET)
    if ws is None:
        return False  # Demo mode: pretend success

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        report_id, username, date, task, status, director,
        designer, project, new_project, notes, time_from, time_to, timestamp
    ]
    try:
        ws.append_row(row)
        return True
    except Exception:
        return False


def update_report(report_id, date, task, status, director,
                  designer, project, new_project, notes, time_from, time_to) -> bool:
    ws = get_sheet(REPORTS_SHEET)
    if ws is None:
        return False  # Demo mode

    try:
        df = sheet_to_df(ws)
        if df is None:
            return False
        match_idx = df.index[df["ID"].astype(str) == str(report_id)].tolist()
        if not match_idx:
            return False
        row_num = match_idx[0] + 2  # +1 header, +1 0-index

        # Map column names to column numbers
        col_map = {col: i+1 for i, col in enumerate(REPORT_COLUMNS)}

        updates = {
            "Date": date, "Daily Task / Activity": task, "Status": status,
            "Director": director, "Designer": designer, "Project": project,
            "New Project": new_project, "Notes": notes,
            "Time From": time_from, "Time To": time_to,
        }
        for col_name, val in updates.items():
            if col_name in col_map:
                ws.update_cell(row_num, col_map[col_name], val)
        return True
    except Exception:
        return False


