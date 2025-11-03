# DeFi Risk Gauge

A comprehensive risk assessment tool that bridges Traditional Finance (TradFi) risk metrics with DeFi transparency data.

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. **Push code to GitHub repository**

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

## 📊 Features

- **Real-time Risk Assessment**: Live data from DeFiLlama and CoinGecko APIs
- **Multi-factor Risk Model**: Combines Market Risk, Liquidity Risk, and Protocol Risk
- **Visual Risk Gauge**: Interactive Plotly gauge chart for easy interpretation
- **Protocol Coverage**: Supports 8+ major DeFi protocols
- **Detailed Metrics**: TVL, volatility, price data, and audit scores

## 🏗️ Architecture

- **Frontend**: Streamlit (Python-based web framework)
- **Data Sources**: 
  - DeFiLlama API for TVL data
  - CoinGecko API for price and volatility data
- **Risk Calculation**: Custom algorithm combining volatility, TVL, and audit scores
- **Visualization**: Plotly for interactive charts

## 📦 Dependencies

- `streamlit`: Web application framework
- `requests`: HTTP library for API calls
- `numpy`: Numerical computations
- `pandas`: Data manipulation
- `plotly`: Interactive visualizations

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize theme and server settings.

## 📝 License

This project is developed for educational purposes as part of a Financial Markets Processes and Technology course.

