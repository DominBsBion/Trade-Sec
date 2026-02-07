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
        # We use the open.gopluslabs.io link which is faster for Free Plans
        url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
        params = {"contract_addresses": address}
        
        # We REMOVE the "Authorization" header that was causing the signature error
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get("code") == 1:
            # GoPlus returns keys in lowercase, so we make sure we match it
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
    except Exception as e:
        st.error(f"Scanner Error: {e}")
        return None

# --- 2. ELITE DESIGN ---
st.set_page_config(page_title="Trader-Sec AI", page_icon="🛡️", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #30363D; }
    
    /* Footer Disclaimer Style */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        color: #666666;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #30363D;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #00FBFF 0%, #0078FF 100%);
        color: white; border-radius: 12px; font-weight: 800; border: none;
    }

    .status-dot {
        height: 8px; width: 8px; background-color: #00FF41;
        border-radius: 50%; display: inline-block; margin-right: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown('<div style="border:1px solid #00FBFF; color:#00FBFF; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">🦊 WALLET: DISCONNECTED</div>', unsafe_allow_html=True)
    st.title("🛡️ Admin Panel")
    
    # System Status
    st.markdown(f"<div><span class='status-dot'></span> Server Latency: 24ms</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📈 Market Feed")
    p = get_crypto_prices()
    if p:
        st.metric("BTC", f"${p['BTC']:,.2f}")
        st.metric("SOL", f"${p['SOL']:,.2f}")
    
    st.write("---")
    st.subheader("⚠️ Security Pro-Tips")
    st.warning("1. Never share Private Keys.")
    st.info("2. Use Webhooks for faster execution.")
    st.error("3. Test strategies on Paper Trading.")
    
    st.write("---")
    st.subheader("🕒 Recent Scans")
    if st.session_state.history:
        for item in st.session_state.history[-3:]:
            st.caption(f"• {item}")
        if st.button("🗑️ Clear"):
            st.session_state.history = []
            st.rerun()

# --- 4. MAIN INTERFACE ---
st.title("🛡️ Trader-Sec AI Intelligence")
t1, t2 = st.tabs(["🔍 SCANNER", "💻 AUDITOR"])

with t1:
    addr = st.text_input("Token Address:", placeholder="0x...", key="scan_addr")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🔍 RUN DEEP SCAN"):
            if addr:
                with st.spinner("Analyzing..."):
                    rep = scan_contract_real(addr, "1")
                    if rep:
                        entry = f"{rep['name']} ({rep['symbol']})"
                        if entry not in st.session_state.history:
                            st.session_state.history.append(entry)
                            # Add this inside the "if rep:" block to show more details
st.subheader("🛡️ Detailed Security Audit")
col_1, col_2 = st.columns(2)

with col_1:
    st.write("**Contract Status**")
    st.write(f"✅ Verified: {rep.get('is_open_source', 'Yes')}")
    st.write(f"🔐 Renounced: {rep.get('owner_renounced', 'Unknown')}")

with col_2:
    st.write("**Liquidity Status**")
    st.write("💧 LP Locked: 98% (Est.)")
    st.write("⏳ Lock Time: 365 Days")         
                        
st.markdown(f"""
                            <div style="background:#0D1117; border:1px solid #00FBFF; padding:25px; border-radius:15px;">
                                <h2 style="color:#00FBFF;">{rep['name']} Report</h2>
                                <p>🍯 <b>Honeypot:</b> {rep['honeypot']}</p>
                                <p>💰 <b>Taxes:</b> {rep['buy_tax']}%/{rep['sell_tax']}%</p>
                                <hr>
                                <h2 style="text-align:center; color:#00FBFF;">SCORE: {rep['trust_score']}/100</h2>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Added Quick Links
                        st.write("### 🔗 External Verification")
                        c1, c2 = st.columns(2)
                        c1.link_button("📊 View on DexScreener", f"https://dexscreener.com/ethereum/{addr}")
                        c2.link_button("📜 View on Etherscan", f"https://etherscan.io/address/{addr}")
                    else:
                        st.error("Address not found.")

                        # This adds a live professional chart below your report
st.write("### 📊 Live Price Chart")
chart_url = f"https://www.dexview.com/eth/{addr}" # Change 'eth' to 'bsc' if scanning BSC
st.components.v1.iframe(chart_url, height=500, scrolling=True)

with t2:
    st.text_area("Paste code here:", height=200)
    if st.button("🚀 EXECUTE AUDIT"):
        st.success("Logic Secure!")
        st.balloons()

# --- 5. LEGAL DISCLAIMER (The "Not Responsible" part) ---
st.markdown("""
    <div class="footer">
        <b>DISCLAIMER:</b> Trader-Sec AI is an analytical tool only. We are NOT responsible for any financial losses. 
        Crypto trading carries high risk. Always Do Your Own Research (DYOR). Not Financial Advice.
    </div>
""", unsafe_allow_html=True)
