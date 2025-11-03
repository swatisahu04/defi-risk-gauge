# Deployment Guide: DeFi Risk Gauge

## Quick Start - Deploy to Streamlit Cloud

### Step 1: Create GitHub Repository

1. **Initialize Git repository:**
   ```bash
   cd defi-risk-gauge
   git init
   git add .
   git commit -m "Initial commit: DeFi Risk Gauge application"
   ```

2. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it `defi-risk-gauge` (or your preferred name)
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push code to GitHub:**
   ```bash
   git remote add origin https://github.com/swatisahu04/defi-risk-gauge.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Select your GitHub account
   - Select the `defi-risk-gauge` repository
   - Select the `main` branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment:**
   - Streamlit Cloud will install dependencies from `requirements.txt`
   - The app will be available at: `https://YOUR_APP_NAME.streamlit.app`
   - Bookmark this URL for your assignment submission

### Step 3: Verify Deployment

1. **Test the Application:**
   - Open the deployed URL
   - Select different protocols from the dropdown
   - Verify risk scores are calculated correctly
   - Check that gauges display properly
   - Ensure all metrics are showing

2. **Check Public Access:**
   - Share the URL with a friend/classmate
   - Confirm they can access without special permissions
   - Verify no authentication is required

## Local Testing Before Deployment

### Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Verify Everything Works

1. **Test Protocol Selection:**
   - Select each protocol from the dropdown
   - Verify data loads correctly

2. **Test API Calls:**
   - Check that TVL data is fetched
   - Verify price data is retrieved
   - Ensure error handling works (try disconnecting internet briefly)

3. **Test Visualizations:**
   - Confirm gauge chart displays
   - Check color coding is correct
   - Verify risk levels match scores

## Files Required for Deployment

Ensure these files are in your repository:

- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `README.md` - Project documentation

## Troubleshooting

### Issue: App won't deploy on Streamlit Cloud

**Solutions:**
- Ensure `requirements.txt` has all dependencies
- Check that `app.py` is in the root directory
- Verify Python version is compatible (Streamlit Cloud uses Python 3.11)

### Issue: API errors in deployed app

**Solutions:**
- Check that APIs (DeFiLlama, CoinGecko) are publicly accessible
- Verify no authentication is required
- Review error handling in `app.py`

### Issue: Import errors

**Solutions:**
- Ensure all dependencies are in `requirements.txt`
- Check that package names are correct
- Verify version constraints are compatible

## Environment Variables (Not Required)

This application doesn't require environment variables or API keys, as it uses publicly accessible APIs. However, if you need to add API keys in the future:

1. Add to Streamlit Cloud:
   - Go to your app settings
   - Click "Secrets"
   - Add environment variables

2. Access in code:
   ```python
   import streamlit as st
   api_key = st.secrets["API_KEY"]
   ```

## Production Considerations

For production deployment:

1. **Rate Limiting:**
   - Current implementation uses caching (5-minute TTL)
   - Consider increasing TTL if needed
   - Monitor API rate limits

2. **Error Monitoring:**
   - Add logging for production debugging
   - Monitor API failures
   - Track user analytics

3. **Performance:**
   - Current implementation is optimized for Streamlit Cloud
   - Consider CDN for static assets if needed

## Support

For issues or questions:
- Check Streamlit Cloud logs in the app dashboard
- Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- DeFiLlama API docs: [docs.llama.fi](https://docs.llama.fi)
- CoinGecko API docs: [coingecko.com/api](https://www.coingecko.com/api)

