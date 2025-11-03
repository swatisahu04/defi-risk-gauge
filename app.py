"""
DeFi Risk Gauge - A comprehensive risk assessment tool for DeFi protocols
Bridges Traditional Finance (TradFi) risk metrics with DeFi transparency data
"""

import streamlit as st
import requests
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import logging
import os
from pathlib import Path

# -----------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------
def setup_logging():
    """Configure logging to both file and console"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    log_file = log_dir / f"defi_risk_gauge_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    
    # Set lower level for third-party libraries to reduce noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger

# Initialize logging
logger = setup_logging()

logger.info("=" * 80)
logger.info("DeFi Risk Gauge Application Starting")
logger.info("=" * 80)

st.set_page_config(
    page_title="DeFi Risk Gauge",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .risk-badge {
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💠 DeFi Risk Gauge</div>', unsafe_allow_html=True)
st.write("A comprehensive dashboard that estimates relative risk for selected DeFi protocols using public on-chain analytics sources (DeFiLlama, CoinGecko).")

# -----------------------------------------------------------
# 1. Define protocol list (expanded)
# -----------------------------------------------------------
PROTOCOLS = {
    "Aave": {
        "defillama_slug": "aave",
        "coingecko_id": "aave",
        "audit_score": 0.85,   # 0-1, higher = safer
        "description": "Decentralized lending and borrowing protocol"
    },
    "Uniswap": {
        "defillama_slug": "uniswap",
        "coingecko_id": "uniswap",
        "audit_score": 0.80,
        "description": "Largest decentralized exchange (DEX)"
    },
    "Curve": {
        "defillama_slug": "curve",
        "coingecko_id": "curve-dao-token",
        "audit_score": 0.82,
        "description": "Stablecoin and pegged asset exchange"
    },
    "Lido": {
        "defillama_slug": "lido",
        "coingecko_id": "lido-dao",
        "audit_score": 0.80,
        "description": "Liquid staking protocol for Ethereum"
    },
    "Compound": {
        "defillama_slug": "compound",
        "coingecko_id": "compound-governance-token",
        "audit_score": 0.83,
        "description": "Algorithmic money market protocol"
    },
    "MakerDAO": {
        "defillama_slug": "makerdao",
        "coingecko_id": "maker",
        "audit_score": 0.85,
        "description": "Decentralized stablecoin (DAI) protocol"
    },
    "Yearn Finance": {
        "defillama_slug": "yearn-finance",
        "coingecko_id": "yearn-finance",
        "audit_score": 0.75,
        "description": "Yield aggregator and vault optimizer"
    },
    "Balancer": {
        "defillama_slug": "balancer",
        "coingecko_id": "balancer",
        "audit_score": 0.78,
        "description": "Automated market maker with customizable pools"
    },
}

# Sidebar
st.sidebar.header("🔧 Configuration")
protocol_name = st.sidebar.selectbox("Select a DeFi Protocol", list(PROTOCOLS.keys()))
proto_conf = PROTOCOLS[protocol_name]

logger.info(f"User selected protocol: {protocol_name}")
logger.debug(f"Protocol configuration: {proto_conf}")

# Display protocol description
st.sidebar.markdown(f"**Description:** {proto_conf['description']}")
st.sidebar.markdown("---")

# Comparison mode toggle
compare_mode = st.sidebar.checkbox("Compare with other protocols", value=False)
if compare_mode:
    logger.info("Comparison mode enabled")

# Auto-refresh
auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)
if auto_refresh:
    logger.info("Auto-refresh enabled, waiting 30 seconds...")
    time.sleep(30)
    logger.info("Auto-refresh triggered, reloading app...")
    st.rerun()

# About section
st.sidebar.markdown("---")
st.sidebar.header("About this app")
st.sidebar.info(
    "This DeFi Risk Gauge demonstrates how public on-chain analytics "
    "can be combined with market-risk thinking from TradFi (liquidity, volatility, audit). "
    "Built in Streamlit for rapid prototyping (vibe coding)."
)

# -----------------------------------------------------------
# 2. Helper functions to call APIs
# -----------------------------------------------------------

@st.cache_data(ttl=600)  # Increased cache TTL to 10 minutes to reduce API calls
def fetch_tvl(slug: str):
    """
    Get protocol-level TVL from DeFiLlama with retry logic.
    Docs: https://defillama.com/docs/api
    """
    url = f"https://api.llama.fi/protocol/{slug}"
    logger.info(f"Fetching TVL data for protocol: {slug}")
    logger.debug(f"TVL API URL: {url}")
    
    # Retry logic for Streamlit Cloud
    max_retries = 3
    timeout = 30  # Increased timeout for Streamlit Cloud (was 10)
    
    headers = {
        'User-Agent': 'DeFi-Risk-Gauge/1.0',
        'Accept': 'application/json'
    }
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Attempt {attempt + 1}/{max_retries} for fetching TVL for {slug}")
            resp = requests.get(url, timeout=timeout, headers=headers)
            
            # Log response status before raising
            logger.debug(f"TVL API response status: {resp.status_code}")
            
            # Check for non-2xx status codes before raising
            if not resp.ok:
                logger.warning(f"Non-OK response for {slug}: Status {resp.status_code}, Response: {resp.text[:200]}")
            
            resp.raise_for_status()
            
            data = resp.json()
            logger.debug(f"TVL API response keys: {list(data.keys())[:5]}...")  # Log first 5 keys
            
            # Data sometimes has 'tvl' as list over time; sometimes there is 'currentChainTvls'
            if "tvl" in data and isinstance(data["tvl"], list) and len(data["tvl"]) > 0:
                latest = data["tvl"][-1].get("totalLiquidityUSD", 0)
                logger.info(f"Successfully fetched TVL for {slug}: ${latest:,.0f}")
                return latest
            elif "tvl" in data and isinstance(data["tvl"], (int, float)):
                tvl_value = data["tvl"]
                logger.info(f"Successfully fetched TVL for {slug} (direct value): ${tvl_value:,.0f}")
                return tvl_value
            else:
                # fallback
                fallback_value = data.get("tvl", 0)
                logger.warning(f"Using fallback TVL value for {slug}: ${fallback_value:,.0f}")
                return fallback_value
                
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(f"Timeout while fetching TVL for {slug} (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Timeout while fetching TVL for {slug} after {max_retries} attempts: {e}")
                st.warning(f"Could not fetch TVL for {slug}: Request timeout after {max_retries} attempts. Please try again later.")
                return 0
        except requests.exceptions.HTTPError as e:
            # Extract status code more reliably
            try:
                status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else None
                response_text = e.response.text[:200] if hasattr(e, 'response') and e.response is not None else "No response text"
                logger.error(f"HTTP error while fetching TVL for {slug}: Status {status_code}, Response: {response_text}")
                
                if status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt * 2  # Longer wait for rate limits
                        logger.warning(f"Rate limited for {slug} (attempt {attempt + 1}/{max_retries}). Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                elif status_code == 404:
                    logger.error(f"Protocol {slug} not found (404). This may be a typo or removed protocol.")
                    st.warning(f"Could not find protocol '{slug}'. Please check the protocol name.")
                    return 0
                elif status_code == 503 or status_code == 502:
                    # Service unavailable or bad gateway - retry
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt * 2
                        logger.warning(f"Service unavailable for {slug} (attempt {attempt + 1}/{max_retries}). Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                status_msg = f"HTTP {status_code}" if status_code else "HTTP error"
                st.warning(f"Could not fetch TVL for {slug}: {status_msg}. Please try again later.")
            except Exception as parse_error:
                logger.error(f"Error parsing HTTP error for {slug}: {parse_error}. Original error: {e}")
                st.warning(f"Could not fetch TVL for {slug}: HTTP error. Please try again later.")
            return 0
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Connection error for {slug} (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Connection error while fetching TVL for {slug} after {max_retries} attempts: {e}")
                st.warning(f"Could not fetch TVL for {slug}: Connection error. Please check your internet connection.")
                return 0
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception while fetching TVL for {slug}: {type(e).__name__} - {str(e)}")
            st.warning(f"Could not fetch TVL for {slug}: {e}")
            return 0
        except Exception as e:
            logger.exception(f"Unexpected error processing TVL data for {slug}: {type(e).__name__} - {str(e)}")
            st.warning(f"Error processing TVL data for {slug}: {e}")
            return 0
    
    logger.error(f"Failed to fetch TVL for {slug} after {max_retries} attempts")
    return 0

@st.cache_data(ttl=600)  # Increased cache TTL to 10 minutes
def fetch_tvl_history(slug: str):
    """Fetch historical TVL data for charting with retry logic"""
    url = f"https://api.llama.fi/protocol/{slug}"
    logger.info(f"Fetching TVL history for protocol: {slug}")
    
    max_retries = 3
    timeout = 30  # Increased timeout for Streamlit Cloud
    
    headers = {
        'User-Agent': 'DeFi-Risk-Gauge/1.0',
        'Accept': 'application/json'
    }
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Attempt {attempt + 1}/{max_retries} for fetching TVL history for {slug}")
            resp = requests.get(url, timeout=timeout, headers=headers)
            resp.raise_for_status()
            logger.debug(f"TVL history API response status: {resp.status_code}")
            
            data = resp.json()
            if "tvl" in data and isinstance(data["tvl"], list):
                df = pd.DataFrame(data["tvl"])
                logger.debug(f"TVL history data shape: {df.shape}, columns: {list(df.columns)}")
                
                if "date" in df.columns and "totalLiquidityUSD" in df.columns:
                    df["date"] = pd.to_datetime(df["date"], unit="s")
                    logger.info(f"Successfully fetched TVL history for {slug}: {len(df)} data points")
                    return df[["date", "totalLiquidityUSD"]].rename(columns={"totalLiquidityUSD": "TVL (USD)"})
                else:
                    logger.warning(f"Missing required columns in TVL history for {slug}. Available: {list(df.columns)}")
                    return None
            else:
                logger.warning(f"No TVL history list found in response for {slug}")
                return None
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Timeout while fetching TVL history for {slug} (attempt {attempt + 1}/{max_retries}). Retrying...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Timeout while fetching TVL history for {slug} after {max_retries} attempts")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Request error for {slug} history (attempt {attempt + 1}/{max_retries}). Retrying...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Request exception while fetching TVL history for {slug}: {type(e).__name__} - {str(e)}")
                return None
        except Exception as e:
            logger.exception(f"Unexpected error fetching TVL history for {slug}: {type(e).__name__} - {str(e)}")
            return None
    
    return None

@st.cache_data(ttl=600)  # Increased cache TTL to 10 minutes
def fetch_volatility(coingecko_id: str):
    """
    Fetch comprehensive volatility and market data from CoinGecko with retry logic.
    Docs: https://www.coingecko.com/en/api/documentation
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coingecko_id}"
    params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }
    logger.info(f"Fetching volatility data for CoinGecko ID: {coingecko_id}")
    logger.debug(f"CoinGecko API URL: {url}")
    
    max_retries = 3
    timeout = 30  # Increased timeout for Streamlit Cloud
    
    headers = {
        'User-Agent': 'DeFi-Risk-Gauge/1.0',
        'Accept': 'application/json'
    }
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Attempt {attempt + 1}/{max_retries} for fetching volatility for {coingecko_id}")
            resp = requests.get(url, params=params, timeout=timeout, headers=headers)
            resp.raise_for_status()
            logger.debug(f"CoinGecko API response status: {resp.status_code}")
            
            data = resp.json()
            market_data = data.get("market_data", {})
            
            if not market_data:
                logger.warning(f"No market_data found in CoinGecko response for {coingecko_id}")
            
            vol_24h = abs(market_data.get("price_change_percentage_24h", 0) or 0)
            vol_7d = abs(market_data.get("price_change_percentage_7d", 0) or 0)
            current_price = market_data.get("current_price", {}).get("usd", 0) if isinstance(market_data.get("current_price"), dict) else market_data.get("current_price", 0)
            market_cap = market_data.get("market_cap", {}).get("usd", 0) if isinstance(market_data.get("market_cap"), dict) else market_data.get("market_cap", 0)
            
            # Composite volatility (weighted)
            composite_vol = (vol_24h * 0.7) + (vol_7d * 0.3 / 7)
            
            logger.info(f"Successfully fetched volatility data for {coingecko_id}: "
                       f"24h={vol_24h:.2f}%, 7d={vol_7d:.2f}%, composite={composite_vol:.2f}%, "
                       f"price=${current_price:.4f}, market_cap=${market_cap:,.0f}")
            
            return {
                "volatility_24h": vol_24h,
                "volatility_7d": vol_7d,
                "composite_volatility": composite_vol,
                "current_price": current_price,
                "market_cap": market_cap
            }
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Timeout while fetching volatility for {coingecko_id} (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Timeout while fetching volatility for {coingecko_id} after {max_retries} attempts: {e}")
                st.warning(f"Could not fetch volatility for {coingecko_id}: Request timeout after {max_retries} attempts. Please try again later.")
                return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}
        except requests.exceptions.HTTPError as e:
            # Extract status code more reliably
            try:
                status_code = e.response.status_code if hasattr(e, 'response') and e.response is not None else None
                response_text = e.response.text[:200] if hasattr(e, 'response') and e.response is not None else "No response text"
                logger.error(f"HTTP error while fetching volatility for {coingecko_id}: Status {status_code}, Response: {response_text}")
                
                if status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt * 2
                        logger.warning(f"Rate limited for {coingecko_id} (attempt {attempt + 1}/{max_retries}). Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                elif status_code == 404:
                    logger.error(f"Coin {coingecko_id} not found (404). This may be a typo or removed coin.")
                    st.warning(f"Could not find coin '{coingecko_id}'. Please check the coin ID.")
                    return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}
                elif status_code == 503 or status_code == 502:
                    # Service unavailable or bad gateway - retry
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt * 2
                        logger.warning(f"Service unavailable for {coingecko_id} (attempt {attempt + 1}/{max_retries}). Waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                status_msg = f"HTTP {status_code}" if status_code else "HTTP error"
                st.warning(f"Could not fetch volatility for {coingecko_id}: {status_msg}. Please try again later.")
            except Exception as parse_error:
                logger.error(f"Error parsing HTTP error for {coingecko_id}: {parse_error}. Original error: {e}")
                st.warning(f"Could not fetch volatility for {coingecko_id}: HTTP error. Please try again later.")
            return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Connection error for {coingecko_id} (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Connection error while fetching volatility for {coingecko_id} after {max_retries} attempts: {e}")
                st.warning(f"Could not fetch volatility for {coingecko_id}: Connection error. Please check your internet connection.")
                return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception while fetching volatility for {coingecko_id}: {type(e).__name__} - {str(e)}")
            st.warning(f"Could not fetch volatility for {coingecko_id}: {e}")
            return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}
        except Exception as e:
            logger.exception(f"Unexpected error processing volatility data for {coingecko_id}: {type(e).__name__} - {str(e)}")
            st.warning(f"Error processing volatility data for {coingecko_id}: {e}")
            return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}
    
    logger.error(f"Failed to fetch volatility for {coingecko_id} after {max_retries} attempts")
    return {"volatility_24h": 0, "volatility_7d": 0, "composite_volatility": 0, "current_price": 0, "market_cap": 0}

# -----------------------------------------------------------
# 3. Fetch data
# -----------------------------------------------------------
st.header(f"📊 Risk Analysis: {protocol_name}")

logger.info(f"Starting data fetch for {protocol_name}...")
fetch_start_time = time.time()

with st.spinner("Fetching real-time data..."):
    tvl_usd = fetch_tvl(proto_conf["defillama_slug"])
    vol_data = fetch_volatility(proto_conf["coingecko_id"])
    tvl_history = fetch_tvl_history(proto_conf["defillama_slug"])
    audit_score = proto_conf["audit_score"]
    
fetch_duration = time.time() - fetch_start_time
logger.info(f"Data fetch completed in {fetch_duration:.2f} seconds for {protocol_name}")

vol_24h = vol_data["volatility_24h"]
vol_7d = vol_data["volatility_7d"]
composite_vol = vol_data["composite_volatility"]
current_price = vol_data["current_price"]
market_cap = vol_data["market_cap"]

# Validate data before proceeding
if vol_data["volatility_24h"] == 0 and vol_data["volatility_7d"] == 0:
    logger.warning(f"Zero volatility data received for {protocol_name}, may indicate API issue")

if tvl_usd == 0:
    logger.warning(f"Zero TVL received for {protocol_name}, may indicate API issue or new protocol")

# -----------------------------------------------------------
# 4. Risk score model (enhanced, explainable)
# -----------------------------------------------------------
def compute_risk_score(tvl, vol, audit):
    """
    Enhanced risk score calculation with TradFi-inspired methodology
    
    Components:
    - Market Risk (40%): Volatility-based risk
    - Liquidity Risk (30%): TVL-based confidence
    - Protocol Risk (30%): Audit-based security
    """
    logger.debug(f"Computing risk score - TVL: ${tvl:,.0f}, Volatility: {vol:.2f}%, Audit: {audit:.2f}")
    
    # Avoid log(0)
    tvl_term = max(np.log(tvl + 1), 1)
    
    # Normalize TVL risk (higher TVL = lower risk)
    if tvl >= 1e9:  # > $1B
        tvl_risk = 0.2
        tvl_tier = "High (>$1B)"
    elif tvl >= 100e6:  # > $100M
        tvl_risk = 0.4
        tvl_tier = "Medium ($100M-$1B)"
    elif tvl >= 10e6:  # > $10M
        tvl_risk = 0.6
        tvl_tier = "Low-Medium ($10M-$100M)"
    else:
        tvl_risk = 0.8
        tvl_tier = "Low (<$10M)"
    
    logger.debug(f"TVL risk tier: {tvl_tier}, TVL risk factor: {tvl_risk}")
    
    # Normalize volatility risk (0-1 scale)
    vol_risk = min(vol / 100.0, 1.0) if vol > 0 else 0
    logger.debug(f"Volatility risk factor: {vol_risk:.4f}")
    
    # Protocol risk (higher audit = lower risk)
    protocol_risk = 1.0 - audit
    logger.debug(f"Protocol risk factor: {protocol_risk:.4f}")
    
    # Weighted composite risk score (0-100)
    risk_score = (vol_risk * 40) + (tvl_risk * 30) + (protocol_risk * 30)
    risk_score = min(max(risk_score, 0), 100)
    
    logger.info(f"Risk score calculated: {risk_score:.2f} "
               f"(Market: {vol_risk*40:.2f}, Liquidity: {tvl_risk*30:.2f}, Protocol: {protocol_risk*30:.2f})")
    
    return risk_score

risk_score = compute_risk_score(tvl_usd, composite_vol, audit_score)
logger.info(f"Final risk score for {protocol_name}: {risk_score:.2f}")

# -----------------------------------------------------------
# 5. Display main metrics
# -----------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("TVL (USD)", f"${tvl_usd:,.0f}")
col2.metric("24h Volatility (%)", f"{vol_24h:.2f}")
col3.metric("Audit Score", f"{audit_score:.2f}")
col4.metric("7d Volatility (%)", f"{vol_7d:.2f}")

# -----------------------------------------------------------
# 6. Risk score display with gauge visualization
# -----------------------------------------------------------
st.markdown("---")
col_gauge, col_info = st.columns([2, 1])

with col_gauge:
    st.subheader("Risk Score")
    
    # Create interactive Plotly gauge
    if risk_score < 30:
        risk_level = "Low Risk"
        color = "#28a745"
    elif risk_score < 60:
        risk_level = "Moderate Risk"
        color = "#ffc107"
    else:
        risk_level = "High Risk"
        color = "#dc3545"
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"<b>Risk Score</b><br><span style='font-size:0.8em'>{risk_level}</span>", 'font': {'size': 20}},
        delta = {'reference': 50, 'position': "top"},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': "#e8f5e9"},
                {'range': [30, 60], 'color': "#fff9c4"},
                {'range': [60, 100], 'color': "#ffebee"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor="white"
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Risk level badge
    st.markdown(f"""
    <div class="risk-badge" style="background-color: {color}20; color: {color}; border: 2px solid {color};">
        {risk_level} — {risk_score:.1f}
    </div>
    """, unsafe_allow_html=True)

with col_info:
    st.subheader("Risk Breakdown")
    
    # Calculate component risks
    if tvl_usd >= 1e9:
        tvl_risk_score = 20
    elif tvl_usd >= 100e6:
        tvl_risk_score = 40
    elif tvl_usd >= 10e6:
        tvl_risk_score = 60
    else:
        tvl_risk_score = 80
    
    vol_risk_score = min(composite_vol, 100)
    protocol_risk_score = (1 - audit_score) * 100
    
    risk_breakdown = pd.DataFrame({
        "Component": ["Market Risk", "Liquidity Risk", "Protocol Risk"],
        "Score": [f"{vol_risk_score:.1f}", f"{tvl_risk_score:.1f}", f"{protocol_risk_score:.1f}"],
        "Weight": ["40%", "30%", "30%"]
    })
    
    st.dataframe(risk_breakdown, use_container_width=True, hide_index=True)
    
    # Additional info
    st.markdown("---")
    st.metric("Current Price", f"${current_price:.4f}")
    if market_cap > 0:
        st.metric("Market Cap", f"${market_cap:,.0f}")

# -----------------------------------------------------------
# 7. Historical TVL Chart
# -----------------------------------------------------------
if tvl_history is not None and len(tvl_history) > 0:
    st.markdown("---")
    st.subheader("📈 Historical TVL Trend")
    logger.debug(f"Rendering TVL history chart with {len(tvl_history)} data points")
    
    try:
        fig_tvl = px.line(
            tvl_history,
            x="date",
            y="TVL (USD)",
            title=f"{protocol_name} TVL Over Time",
            labels={"TVL (USD)": "TVL (USD)", "date": "Date"}
        )
        fig_tvl.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="TVL (USD)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_tvl, use_container_width=True)
        logger.debug("TVL history chart rendered successfully")
    except Exception as e:
        logger.exception(f"Error rendering TVL history chart: {type(e).__name__} - {str(e)}")
        st.error(f"Error rendering TVL history chart: {e}")
else:
    logger.warning(f"No TVL history data available for {protocol_name}")

# -----------------------------------------------------------
# 8. Scenario Analysis: Volatility Shock
# -----------------------------------------------------------
st.markdown("---")
st.subheader("🔬 Scenario Analysis: Volatility Shock")

vol_scenarios = [composite_vol * m for m in [0.5, 1, 1.5, 2, 3]]
risk_values = [compute_risk_score(tvl_usd, v, audit_score) for v in vol_scenarios]

scenario_data = pd.DataFrame({
    "Volatility Multiplier": ["0.5x", "1x", "1.5x", "2x", "3x"],
    "Volatility (%)": [f"{v:.2f}" for v in vol_scenarios],
    "Risk Score": [f"{r:.1f}" for r in risk_values]
})

col_chart, col_table = st.columns([2, 1])

with col_chart:
    fig_scenario = px.line(
        x=vol_scenarios,
        y=risk_values,
        markers=True,
        title="Risk Score Sensitivity to Volatility Changes",
        labels={"x": "Volatility (%)", "y": "Risk Score (0-100)"}
    )
    fig_scenario.update_layout(height=400)
    st.plotly_chart(fig_scenario, use_container_width=True)

with col_table:
    st.write("**Scenario Results**")
    st.dataframe(scenario_data, use_container_width=True, hide_index=True)

# -----------------------------------------------------------
# 9. Protocol Comparison (if enabled)
# -----------------------------------------------------------
if compare_mode:
    st.markdown("---")
    st.subheader("📊 Protocol Comparison")
    
    selected_protocols = st.multiselect(
        "Select protocols to compare",
        [p for p in PROTOCOLS.keys() if p != protocol_name],
        default=[p for p in list(PROTOCOLS.keys())[:3] if p != protocol_name]
    )
    
    if selected_protocols:
        logger.info(f"Starting protocol comparison: {[protocol_name] + selected_protocols}")
        comparison_data = []
        
        with st.spinner("Fetching comparison data..."):
            for proto_name in [protocol_name] + selected_protocols:
                logger.debug(f"Fetching comparison data for {proto_name}")
                proto = PROTOCOLS[proto_name]
                comp_tvl = fetch_tvl(proto["defillama_slug"])
                comp_vol = fetch_volatility(proto["coingecko_id"])
                comp_audit = proto["audit_score"]
                comp_risk = compute_risk_score(comp_tvl, comp_vol["composite_volatility"], comp_audit)
                
                comparison_data.append({
                    "Protocol": proto_name,
                    "Risk Score": comp_risk,
                    "TVL (USD)": comp_tvl,
                    "24h Volatility (%)": comp_vol["volatility_24h"],
                    "Audit Score": comp_audit
                })
                logger.debug(f"Added comparison data for {proto_name}: Risk={comp_risk:.2f}")
        
        try:
            comp_df = pd.DataFrame(comparison_data)
            
            # Sort by risk score
            comp_df = comp_df.sort_values("Risk Score")
            logger.info(f"Comparison completed for {len(comparison_data)} protocols")
            
            # Display comparison table
            st.dataframe(comp_df, use_container_width=True, hide_index=True)
            
            # Comparison chart
            fig_compare = px.bar(
                comp_df,
                x="Protocol",
                y="Risk Score",
                color="Risk Score",
                color_continuous_scale=["green", "yellow", "red"],
                title="Risk Score Comparison",
                labels={"Risk Score": "Risk Score (0-100)"}
            )
            fig_compare.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_compare, use_container_width=True)
            logger.debug("Comparison chart rendered successfully")
        except Exception as e:
            logger.exception(f"Error rendering comparison: {type(e).__name__} - {str(e)}")
            st.error(f"Error rendering comparison: {e}")

# -----------------------------------------------------------
# 10. AI-style explanation (enhanced)
# -----------------------------------------------------------
st.markdown("---")
with st.expander("🤖 AI-Style Explanation"):
    st.markdown(f"""
    For **{protocol_name}**, the model observed:
    
    - **TVL of ${tvl_usd:,.0f}** → {"High liquidity indicates strong confidence and lower liquidity risk." if tvl_usd >= 100e6 else "Moderate liquidity may indicate some liquidity risk."}
    
    - **24h volatility of {vol_24h:.2f}%** → {"Recent price movement is relatively stable." if vol_24h < 10 else "Recent price movement introduces moderate market risk." if vol_24h < 25 else "High volatility indicates elevated market risk."}
    
    - **7d volatility of {vol_7d:.2f}%** → {"Weekly price movement shows stability." if vol_7d < 15 else "Weekly volatility indicates ongoing market uncertainty."}
    
    - **Audit score of {audit_score:.2f}** → {"Strong security posture reduces protocol risk." if audit_score >= 0.8 else "Moderate audit quality requires additional scrutiny."}
    
    The combined risk score of **{risk_score:.1f}** suggests that current risk is 
    **{"low" if risk_score < 30 else "moderate" if risk_score < 60 else "elevated"}**.
    
    ### Model Enhancement Opportunities:
    1. **Oracle risk** assessment for price feed reliability
    2. **Chain-level risk** for multi-chain protocols
    3. **Smart contract exploit history** tracking
    4. **Stablecoin depeg exposure** analysis
    5. **Governance token concentration** metrics
    6. **Liquidity depth** beyond TVL (DEX-specific metrics)
    7. **Time-weighted metrics** for volatility (not just absolute changes)
    """)

# -----------------------------------------------------------
# 11. Methodology explanation
# -----------------------------------------------------------
with st.expander("📖 How Risk Score is Calculated"):
    st.markdown("""
    **Risk Score Methodology (0-100 scale):**
    
    The composite risk score combines three key risk factors using TradFi-inspired methodology:
    
    1. **Market Risk (40% weight)**: Based on price volatility over 24h and 7d periods
       - Composite volatility = (24h vol × 0.7) + (7d vol × 0.3 / 7)
       - Higher volatility indicates greater price risk and market uncertainty
    
    2. **Liquidity Risk (30% weight)**: Based on Total Value Locked (TVL)
       - TVL > $1B: Low risk (20 points)
       - TVL $100M-$1B: Moderate risk (40 points)
       - TVL $10M-$100M: Higher risk (60 points)
       - TVL < $10M: High risk (80 points)
       - Higher TVL indicates greater liquidity confidence
    
    3. **Protocol Risk (30% weight)**: Based on audit score and security assessments
       - Higher audit quality (0.8+) indicates lower protocol risk
       - Reflects smart contract security and governance quality
    
    **Risk Categories:**
    - 🟢 **Low Risk** (0-30): Stable protocols with high TVL, low volatility, strong audits
    - 🟡 **Moderate Risk** (30-60): Protocols with mixed risk indicators
    - 🔴 **High Risk** (60-100): Protocols with high volatility, low TVL, or security concerns
    
    This methodology bridges traditional finance risk assessment with DeFi transparency data.
    """)

st.markdown("---")
st.caption("💡 **DeFi Risk Gauge** - Bridging TradFi risk metrics with DeFi transparency data. Data sources: DeFiLlama API, CoinGecko API")

# Log page rendering completion
logger.info(f"Page rendered successfully for protocol: {protocol_name}")
logger.debug("=" * 80)
