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

# --- 2. ADVANCED CYBER DESIGN ---
st.set_page_config(page_title="Trader-Sec AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #00FBFF33; }
    
    /* Connect Wallet Button Styling */
    .wallet-btn {
        background: transparent;
        border: 2px solid #00FBFF;
        color: #00FBFF;
        padding: 10px 20px;
        border-radius: 30px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 0 10px rgba(0, 251, 255, 0.2);
        margin-bottom: 20px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00FBFF 0%, #0078FF 100%);
        color: white; border-radius: 12px; font-weight: 800; border: none;
        box-shadow: 0 4px 15px rgba(0, 251, 255, 0.3);
    }

    .history-item {
        background: #161B22;
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 5px;
        border-left: 3px solid #00FBFF;
        font-size: 0.8em;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. PRO SIDEBAR ---
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    # Connect Wallet UI
    st.markdown('<div class="wallet-btn">🦊 Connect Wallet</div>', unsafe_allow_html=True)
    
    st.title("🛡️ Admin Panel")
    st.markdown("● <span style='color:#00FF41;'>AI Nodes: Active</span>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📈 Live Market")
    p = get_crypto_prices()
    if p:
        st.metric("BTC", f"${p['BTC']:,.2f}")
        st.metric("SOL", f"${p['SOL']:,.2f}")
    
    st.write("---")
    
    # SCAN HISTORY
    st.subheader("🕒 Recent Scans")
    if not st.session_state.history:
        st.caption("No recent scans")
    for item in st.session_state.history[-3:]: # Show last 3
        st.markdown(f'<div class="history-item">{item}</div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("⚠️ Security Tips")
    st.warning("1. Never share Private Keys.")
    st.error("2. Test on Paper Trading.")

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Trader-Sec AI Intelligence")
t1, t2 = st.tabs(["🔍 REAL-TIME SCANNER", "💻 CODE AUDITOR"])

with t1:
    addr = st.text_input("Token Address:", placeholder="0x...", key="main_scan")
    if st.button("🔍 RUN DEEP SCAN"):
        if addr:
            with st.spinner("Analyzing..."):
                rep = scan_contract_real(addr, "1")
                if rep:
                    # Save to history
                    if rep['name'] not in st.session_state.history:
                        st.session_state.history.append(f"{rep['name']} ({rep['symbol']})")
                    
                    st.markdown(f"""
                        <div style="background:#0D1117; border:1px solid #00FBFF; padding:25px; border-radius:15px;">
                            <h2 style="color:#00FBFF;">{rep['name']} Report</h2>
                            <p>🍯 Honeypot: {rep['honeypot']}</p>
                            <p>💰 Taxes: {rep['buy_tax']}%/{rep['sell_tax']}%</p>
                            <h2 style="text-align:center; color:#00FBFF;">TRUST SCORE: {rep['trust_score']}/100</h2>
                        </div>
                    """, unsafe_allow_html=True)

with t2:
    st.markdown("### 📥 Code Security Audit")
    code = st.text_area("Paste code here:", height=200)
    if st.button("🚀 AUDIT"):
        st.balloons()
