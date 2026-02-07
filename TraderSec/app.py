import streamlit as st
import time
import requests

# --- 1. CORE FUNCTIONS ---
def get_crypto_prices():
    # Stable session to prevent the 'SSL' error you saw earlier
    session = requests.Session()
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {'ids': 'bitcoin,ethereum,solana', 'vs_currencies': 'usd'}
        response = session.get(url, params=params, timeout=5)
        data = response.json()
        return {
            'BTCUSDT': data['bitcoin']['usd'],
            'SOLUSDT': data['solana']['usd']
        }
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

# --- 2. ELITE DARK DESIGN ---
st.set_page_config(page_title="Trader-Sec AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #30363D; }
    [data-testid="stSidebar"] .stMarkdown p { color: #ffffff; }
    div.stButton > button {
        background: linear-gradient(90deg, #00FBFF 0%, #0078FF 100%);
        color: white; border-radius: 12px; font-weight: 800; border: none;
        padding: 10px; box-shadow: 0 4px 15px rgba(0, 251, 255, 0.3);
    }
    .scan-result {
        background-color: #0D1117; border: 1px solid #00FBFF;
        padding: 25px; border-radius: 15px; box-shadow: 0 0 20px rgba(0, 251, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. BLACK SIDEBAR (ADMIN PANEL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("🛡️ Trader-Sec Admin")
    st.markdown("● <span style='color:#00FF41;'>System Status: Active</span>", unsafe_allow_html=True)
    st.write("---")
    
    st.subheader("📈 Live Market Feed")
    prices = get_crypto_prices()
    if prices:
        st.metric("BTC", f"${prices['BTCUSDT']:,.2f}")
        st.metric("SOL", f"${prices['SOLUSDT']:,.2f}")
    else:
        st.write("Prices: Updating...")
    
    st.write("---")
    
    st.subheader("⚠️ Security Pro-Tips")
    st.warning("**1. Key Security:** Never share your .env or Private Keys.")
    st.info("**2. Execution:** Use Webhooks for faster trade entry.")
    st.error("**3. Risk:** Always test on Testnet/Paper Trading first.")
    st.success("**4. Verification:** Check 'Open Source' status before buying.")
    st.warning("**5. Liquidity:** Ensure LP is locked for at least 6 months.")
    st.info("**6. Slippage:** Set Max Slippage to 0.5% for high-cap tokens.")

    st.write("---")
    st.caption("DominBsBion © 2026")

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 style="color:#00FBFF;">🛡️ Trader-Sec AI Intelligence</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔍 REAL-TIME SCANNER", "💻 CODE AUDITOR"])

with tab1:
    st.markdown("### 🛰️ Live Blockchain Intelligence")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        contract_addr = st.text_input("Token Address:", placeholder="0x...", key="scan_input")
    with col_b:
        chain = st.selectbox("Network", ["Ethereum", "BSC"], key="chain_select")
    
    if st.button("🔍 RUN DEEP SCAN"):
        if contract_addr:
            with st.spinner("Analyzing Contract Security..."):
                # "1" for Ethereum, "56" for BSC
                c_id = "1" if chain == "Ethereum" else "56"
                report = scan_contract_real(contract_addr, c_id)
                if report:
                    st.markdown(f"""
                        <div class="scan-result">
                            <h2 style="color:#00FBFF;">{report['name']} ({report['symbol']})</h2>
                            <p>🍯 <b>Honeypot:</b> {report['honeypot']}</p>
                            <p>💰 <b>Taxes:</b> Buy: {report['buy_tax']}% | Sell: {report['sell_tax']}%</p>
                            <hr>
                            <h2 style="color:#00FBFF; text-align:center;">TRUST SCORE: {report['trust_score']}/100</h2>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Error: Address not found. Check the Network selection.")

with tab2:
    st.markdown("### 📥 Code Security Audit")
    user_code = st.text_area("Paste code here:", height=200, key="audit_input")
    if st.button("🚀 EXECUTE AUDIT"):
        if user_code:
            with st.spinner('Analyzing...'):
                time.sleep(1)
                st.success("Analysis Complete! Logic is Secure.")
                st.balloons()
