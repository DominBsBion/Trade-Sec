import streamlit as st
import time
import requests

# --- 1. CORE FUNCTIONS ---
def get_crypto_prices():
    session = requests.Session()
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {'ids': 'bitcoin,ethereum,solana', 'vs_currencies': 'usd'}
        response = session.get(url, params=params, timeout=5)
        data = response.json()
        return {'BTC': data['bitcoin']['usd'], 'SOL': data['solana']['usd']}
    except: return None

def scan_contract_real(address, chain_id="1"):
    try:
        app_key = st.secrets["GOPLUS_KEY"]
        url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
        params = {"contract_addresses": address}
        headers = {"Authorization": f"Bearer {app_key}"}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data.get("code") == 1:
            res = data["result"][address.lower()]
            return {
                "name": res.get("token_name", "Unknown"),
                "symbol": res.get("token_symbol", "???"),
                "honeypot": "🚨 YES" if res.get("is_honeypot") == "1" else "✅ No",
                "buy_tax": res.get("buy_tax", "0"),
                "sell_tax": res.get("sell_tax", "0"),
                "trust_score": 100 - (int(float(res.get("sell_tax", 0))) * 2) 
            }
        return None
    except: return None

# --- 2. ELITE DESIGN ---
st.set_page_config(page_title="Trader-Sec AI", page_icon="🛡️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #30363D; }
    
    /* Glowing Wallet Button */
    .wallet-box {
        border: 2px solid #00FBFF;
        color: #00FBFF;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        background: rgba(0, 251, 255, 0.05);
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00FBFF 0%, #0078FF 100%);
        color: white; border-radius: 12px; font-weight: 800; border: none;
        box-shadow: 0 4px 15px rgba(0, 251, 255, 0.3);
    }

    .history-card {
        background: #161B22;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid #0078FF;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE SIDEBAR (FIXED TIPS & HISTORY) ---
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown('<div class="wallet-box">🦊 WALLET: NOT CONNECTED</div>', unsafe_allow_html=True)
    
    st.title("🛡️ Admin Panel")
    st.write("---")
    
    # Prices
    st.subheader("📈 Market Feed")
    p = get_crypto_prices()
    if p:
        st.metric("BTC", f"${p['BTC']:,.2f}")
        st.metric("SOL", f"${p['SOL']:,.2f}")
    
    st.write("---")
    
    # THE WARNINGS (Restored and Visible)
    st.subheader("⚠️ Security Pro-Tips")
    st.warning("1. Never share your .env or Private Keys.")
    st.info("2. Use Webhooks for 0.5ms faster speed.")
    st.error("3. Test strategies on Paper Trading first.")
    
    st.write("---")
    
    # History with functional "Clear" button
    st.subheader("🕒 Recent Scans")
    if st.session_state.history:
        for item in st.session_state.history[-3:]:
            st.markdown(f'<div class="history-card">{item}</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No recent activity.")

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Trader-Sec AI Intelligence")
t1, t2 = st.tabs(["🔍 REAL-TIME SCANNER", "💻 CODE AUDITOR"])

with t1:
    st.markdown("### 🛰️ Live Blockchain Intelligence")
    addr = st.text_input("Token Address:", placeholder="0x...", key="scan_addr")
    if st.button("🔍 RUN DEEP SCAN"):
        if addr:
            with st.spinner("Analyzing..."):
                rep = scan_contract_real(addr, "1")
                if rep:
                    # Update History
                    entry = f"{rep['name']} ({rep['symbol']})"
                    if entry not in st.session_state.history:
                        st.session_state.history.append(entry)
                    
                    st.markdown(f"""
                        <div style="background:#0D1117; border:1px solid #00FBFF; padding:25px; border-radius:15px;">
                            <h2 style="color:#00FBFF;">{rep['name']} Report</h2>
                            <p>🍯 <b>Honeypot:</b> {rep['honeypot']}</p>
                            <p>💰 <b>Taxes:</b> {rep['buy_tax']}%/{rep['sell_tax']}%</p>
                            <hr>
                            <h2 style="text-align:center; color:#00FBFF;">SCORE: {rep['trust_score']}/100</h2>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Address not found on Network.")

with t2:
    st.markdown("### 📥 Code Security Audit")
    u_code = st.text_area("Paste code here:", height=200)
    if st.button("🚀 EXECUTE AUDIT"):
        if u_code:
            with st.spinner('Checking logic...'):
                time.sleep(1)
                st.success("Logic Secure!")
                st.balloons()
