import streamlit as st
import smtplib
import pandas as pd
from datetime import datetime
from email.message import EmailMessage

# ═════════════════ CONFIGURATION ═════════════════
SENDER_EMAIL = "garryboypepito71@gmail.com"
SENDER_PASSWORD = "fhyv cimp gync wjmj"
# ailyn_peps0678@yahoo.com temporarily removed as per command
RECEIVER_EMAILS = ["garryboypepito2004@gmail.com"] 
# ═════════════════════════════════════════════════

st.set_page_config(page_title="AILYN CONSTRUCTION PRO", layout="centered")

# --- HIGH-VISIBILITY COMMERCIAL STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .pro-header {
        background-color: #2e7d32;
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }
    .logo-text { font-size: 36px; font-weight: 900; letter-spacing: 1px; text-transform: uppercase; margin: 0; }
    .sub-logo { font-size: 12px; opacity: 0.9; letter-spacing: 4px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; }
    
    .stat-card {
        background: #ffffff;
        color: #1b5e20;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        display: flex;
        justify-content: space-around;
        font-weight: 900;
        font-size: 18px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }

    .stButton>button {
        width: 100%; border-radius: 10px; border: 2px solid #2e7d32 !important; 
        height: 4em; background-color: #ffffff !important; color: #2e7d32 !important; 
        transition: all 0.3s ease; font-weight: 800; font-size: 14px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { 
        background-color: #2e7d32 !important; color: white !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for records and funds
if 'records' not in st.session_state: st.session_state.records = []
if 'budget_money' not in st.session_state: st.session_state.budget_money = 0.0
if 'leftover_money' not in st.session_state: st.session_state.leftover_money = 0.0

# --- CALCULATIONS ---
now = datetime.now()
total_funds = st.session_state.budget_money + st.session_state.leftover_money
mat_total = sum(r['Total'] for r in st.session_state.records)
final_balance = total_funds - mat_total

# --- EMAIL ENGINE ---
def send_email_report():
    msg = EmailMessage()
    msg["Subject"] = f"AILYN CONSTRUCTION - INVENTORY RECEIPT - {datetime.now().strftime('%b %d, %Y')}"
    msg["From"] = f"AILYN PRO SYSTEM <{SENDER_EMAIL}>"
    msg["To"] = ", ".join(RECEIVER_EMAILS)

    exp_rows = ""
    for r in st.session_state.records:
        exp_rows += f"<tr><td style='padding:10px; border-bottom:1px solid #eee;'>{r['Date']}</td><td style='text-align:center;'>{r['Qty']}</td><td>{r['Description']}</td><td style='text-align:right;'>PHP {r['Total']:,.2f}</td></tr>"

    html = f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 800px; margin: auto; border: 1px solid #ddd; padding: 30px; background: #fff;">
            <div style="background-color: #2e7d32; color: white; padding: 20px; text-align: center;">
                <h1 style="margin:0;">AILYN CONSTRUCTION</h1>
                <p>INVENTORY RECEIPT</p>
            </div>
            <div style="margin-top:20px; padding:15px; background:#f9f9f9;">
                <p><b>Budget Money:</b> PHP {st.session_state.budget_money:,.2f}</p>
                <p><b>Leftover Money:</b> PHP {st.session_state.leftover_money:,.2f}</p>
                <p style="border-top:1px solid #ccc; padding-top:10px;"><b>Total Starting Funds:</b> PHP {total_funds:,.2f}</p>
                <h2 style="color:#2e7d32;">FINAL BALANCE: PHP {final_balance:,.2f}</h2>
            </div>
            <h4>PURCHASED MATERIALS</h4>
            <table style="width:100%; border-collapse:collapse;">{exp_rows}</table>
        </div>
    </body></html>
    """
    msg.add_alternative(html, subtype='html')
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        st.success("✅ SYSTEM: REPORT SENT SUCCESSFULLY")
    except Exception as e: st.error(f"❌ ERROR: {e}")

# --- DASHBOARD HEADER ---
st.markdown(f"""
    <div class="pro-header">
        <div class="sub-logo">Engineering & Construction</div>
        <div class="logo-text">AILYN CONSTRUCTION</div>
        <div style="font-size: 14px; margin-top: 10px; font-weight: 700;">{now.strftime('%B %d, %Y | %I:%M %p')}</div>
        <div class="stat-card">
            <div>ALLOCATION: PHP {total_funds:,.2f}</div>
            <div style="border-left: 2px solid #2e7d32; padding-left: 20px;">
                BALANCE: PHP {final_balance:,.2f}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- VISIBLE MENU BUTTONS ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📊 SET FUNDS"): st.session_state.mode = "funds"
with c2:
    if st.button("➕ NEW MATERIAL"): st.session_state.mode = "entry"
with c3:
    if st.button("✉️ SEND REPORT"): send_email_report()

c4, c5, c6 = st.columns(3)
with c4:
    if st.button("💸 OTHER COSTS"): st.session_state.mode = "entry"
with c5:
    if st.button("🔄 RESET SYSTEM"):
        st.session_state.records = []
        st.session_state.budget_money = 0.0
        st.session_state.leftover_money = 0.0
        st.rerun()

st.write("---")

# --- INPUT SECTION ---
current_mode = st.session_state.get("mode", "entry")

if current_mode == "funds":
    st.subheader("💰 FUND MANAGEMENT")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        new_budget = st.number_input("BUDGET MONEY (PHP)", value=st.session_state.budget_money)
    with col_b2:
        new_leftover = st.number_input("LEFTOVER MONEY (PHP)", value=st.session_state.leftover_money)
    
    if st.button("UPDATE TOTAL FUNDS"):
        st.session_state.budget_money = new_budget
        st.session_state.leftover_money = new_leftover
        st.success("Funds Combined Successfully")
        st.rerun()

else:
    st.subheader(f"📝 ENTRY MODE")
    with st.form("entry_form", clear_on_submit=True):
        col_item, col_qty = st.columns([3, 1])
        with col_item:
            item = st.text_input("MATERIAL DESCRIPTION").upper()
        with col_qty:
            q = st.number_input("QTY", min_value=1, value=1)
        
        price = st.number_input("UNIT PRICE (PHP)", min_value=0.0)
        
        if st.form_submit_button("PROCESS TRANSACTION"):
            if item and price >= 0:
                st.session_state.records.append({
                    "Date": now.strftime("%Y-%m-%d"),
                    "Description": item,
                    "Qty": q,
                    "Unit Price": price,
                    "Total": q * price
                })
                st.rerun()

# --- PURCHASE LOG TABLE ---
if st.session_state.records:
    st.write("### 📋 PURCHASE LOGS")
    st.table(pd.DataFrame(st.session_state.records))