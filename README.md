# 📋 DAR Portal — Daily Activity Report System

A Streamlit-based employee reporting portal connected to Google Sheets.

---

## ✅ Features

### Employee
- Login with username & password
- Submit daily activity reports (DAR)
- View own reports only (security enforced)
- Edit own reports
- Search by project, date, and status filter
- Dashboard: personal metrics
- Change own password

### Admin
- View **all** employee reports
- Filter by employee, date, project, status
- Edit any report
- Add / delete employee accounts
- View all passwords (V1 requirement)
- Change any user's password
- Dashboard: system-wide analytics

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Google Sheets

#### Create your Google Sheet
1. Go to [sheets.google.com](https://sheets.google.com) → **New Spreadsheet**
2. Copy the **Sheet ID** from the URL:
   `https://docs.google.com/spreadsheets/d/**<SHEET_ID>**/edit`
3. Create two sheets (tabs):

**Sheet 1 — `USERS`**
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| rahul | rahul123 | Employee |

**Sheet 2 — `REPORTS`**
Add these exact column headers in row 1:
```
ID | Username | Date | Daily Task / Activity | Status | Director | Designer | Project | New Project | Notes | Time From | Time To | Created Timestamp
```

#### Create a Google Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts → Create Service Account**
5. Grant role: **Editor**
6. Create JSON key → Download it
7. **Share your Google Sheet** with the service account email (with Editor access)

### 3. Configure credentials

**Option A — Streamlit Secrets (recommended for deployment)**

Edit `.streamlit/secrets.toml`:
```toml
SPREADSHEET_ID = "your-sheet-id-here"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "your-sa@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

**Option B — Local JSON file**

Place your downloaded JSON key as `credentials.json` in the project root.
Set `SPREADSHEET_ID` as an environment variable:
```bash
export SPREADSHEET_ID="your-sheet-id"
```

### 4. Run the app
```bash
streamlit run app.py
```

Open: `http://localhost:8501`

---

## 🧪 Demo Mode (no Google Sheets)

If no credentials are configured, the app runs in **Demo Mode** with:
- Pre-loaded sample users and reports
- Login works with: `admin/admin123`, `rahul/rahul123`, `priya/priya123`
- All write operations simulate success (data is not persisted)

---

## 📁 Project Structure

```
dar_portal/
├── app.py              ← Main Streamlit app (UI + routing)
├── sheets.py           ← Google Sheets integration layer
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── .streamlit/
    ├── config.toml     ← Theme and server config
    └── secrets.toml    ← Credentials (do not commit)
```

---

## 🔒 Security Rules Enforced

| Rule | Implementation |
|------|---------------|
| Employees see only own reports | `get_user_reports(username)` filters by username |
| Employees edit only own reports | Edit page checks `row.Username == session.username` |
| Admins see all | `get_all_reports()` returns full dataset |
| Admins edit all | No username restriction on admin edit |
| Every report linked to logged-in user | `submit_report()` uses `st.session_state.username` |

---

## 📊 Google Sheets → Power BI Integration

The `REPORTS` sheet is structured for direct Power BI connection:

1. In Power BI Desktop → **Get Data → Web**
2. Use the Google Sheets CSV export URL:
   ```
   https://docs.google.com/spreadsheets/d/<SHEET_ID>/gviz/tq?tqx=out:csv&sheet=REPORTS
   ```
3. Enable scheduled refresh for live dashboards

### Recommended Power BI Pages
- **Employee Productivity Dashboard** — Task count, hours per employee
- **Department Dashboard** — Director-wise activity breakdown  
- **Project Status Dashboard** — Status distribution per project
- **Leave Analysis Dashboard** — Leave/Holiday trends by month
- **Daily Activity Tracking** — Day-by-day submission heatmap
- **Monthly Performance Dashboard** — Month-over-month comparison

---

## 🛠️ Customisation

### Add new Status options
In `app.py`, update the `status_opts` list in `report_form()`.

### Add new Director options
In `app.py`, update the `director_opts` list in `report_form()`.

### Add more sheets (e.g. Projects)
Extend `sheets.py` with new `get_sheet()` calls and helper functions.
