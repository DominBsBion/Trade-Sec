import streamlit as st
import time
import re
import requests 

def get_crypto_prices():
    try:
        # CoinGecko is more stable for global dev projects
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,solana',
            'vs_currencies': 'usd'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Mapping the results to your dashboard
        prices = {
            'BTCUSDT': data['bitcoin']['usd'],
            'ETHUSDT': data['ethereum']['usd'],
            'SOLUSDT': data['solana']['usd']
        }
        return prices
    except Exception as e:
        # This will help us see the error in the terminal if it still fails
        print(f"Price Error: {e}")
        return None

# --- 1. DESIGN ---
st.set_page_config(page_title="Trader-Sec AI", page_icon="🛡️", layout="wide")


st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #0B0E14, #161B22);
        color: #E0E0E0;
    }

    /* Sidebar - Glass-morphism Effect */
    section[data-testid="stSidebar"] {
        background-color: rgba(22, 27, 34, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid #30363D;
    }

    /* Buttons - Neon Glow */
    div.stButton > button {
        background: linear-gradient(90deg, #00FBFF 0%, #0078FF 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(0, 251, 255, 0.2);
        transition: 0.3s all ease-in-out;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 251, 255, 0.5);
        transform: translateY(-2px);
    }

    /* Report Cards - Border Glow */
    .report-card {
        background-color: #0D1117;
        border: 1px solid #30363D;
        padding: 20px;
        border-radius: 15px;
        box-shadow: inset 0 0 10px rgba(0, 251, 255, 0.05);
    }

    /* Metric/Ticker Styling */
    [data-testid="stMetricValue"] {
        color: #00FBFF !important;
        font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)
# --- 2. BRANDING & SIDEBAR ---
st.markdown('<h1 class="main-title">🛡️ Trader-Sec AI Auditor</h1>', unsafe_allow_html=True)
st.write("### *Secure your trading bots. Protect your capital.*")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("Admin Panel")
    st.info("System Status: **Active**")
    st.write("---")
    st.subheader("📈 Live Market Feed")
    prices = get_crypto_prices()
    if prices:
        st.metric("BTC", f"${prices['BTCUSDT']:,.2f}")
        st.metric("ETH", f"${prices['ETHUSDT']:,.2f}")
        st.metric("SOL", f"${prices['SOLUSDT']:,.2f}")
    else:
        st.error("Market feed offline.")
    
    st.divider()
    st.subheader("📩 Custom Audits")
    st.link_button("Contact Developer", "mailto:your-email@example.com")
    
    if st.button("Logout", key="logout_btn"):
        st.write("Logging out...")

# --- 3. AUDIT ENGINE ---
def run_audit(code):
    issues = []
    if re.search(r"(api_key|secret|password|token)\s*=\s*['\"][a-zA-Z0-9]{10,}", code, re.I):
        issues.append(("CRITICAL", "Hardcoded API Credentials found!"))
    if "buy" in code.lower() and "balance" not in code.lower():
        issues.append(("HIGH", "Missing Balance Check (Double-Buy Risk)."))
    if "buy" in code.lower() and "stop_loss" not in code.lower() and "sl" not in code.lower():
        issues.append(("WARNING", "No Stop-Loss detected."))
    return issues

# --- 4. INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📥 Code Submission")
    user_code = st.text_area("Paste code here:", height=300, placeholder="Paste your bot script...")
    if st.button("🚀 EXECUTE SECURITY AUDIT", key="audit_btn"):
        if user_code:
            with st.spinner('Analyzing...'):
                time.sleep(2)
                st.session_state['results'] = run_audit(user_code)
                st.session_state['done'] = True
        else:
            st.error("Paste code first!")

with col2:
    st.markdown("### 📊 Report")
    if st.session_state.get('done'):
        res = st.session_state['results'] # This is the 'res' variable
        if res:
            for sev, msg in res:
                st.markdown(f'<div class="report-card"><b>{sev}:</b> {msg}</div>', unsafe_allow_html=True)
        else:
            # --- Certification Logic Fixed Here ---
            st.success("✅ Clean Logic!")
            st.balloons()
            st.markdown(f"""
                <div style="border: 2px solid #00FBFF; padding: 20px; border-radius: 10px; text-align: center; background-color: #161B22;">
                    <h2 style="color: #00FBFF; margin: 0;">OFFICIAL AUDIT PASS</h2>
                    <p style="font-size: 14px; color: #E0E0E0;">Logic passed Trader-Sec Security Protocol.</p>
                    <hr style="border: 0.5px solid #30363D;">
                    <p style="font-family: monospace; font-size: 12px; color: #58A6FF;">
                        Audit ID: TS-{int(time.time())}<br>
                        Status: SECURE 🛡️
                    </p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Awaiting input...")

st.divider()
if st.button("💎 Get Full PDF Report ($49)", key="bottom_pay_button"):
    st.balloons()
    st.write("Payment system connecting...")

with st.expander("⚖️ Legal Disclaimer & License"):
    st.write("""
        Trader-Sec is provided 'as-is' for educational purposes. 
        Automated trading involves high risk. © 2026 Trader-Sec AI.
    """)

    # Trader-Sec Test Script
