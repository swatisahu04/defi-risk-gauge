# DeFi Risk Gauge - Application Description

## What the App Does

**DeFi Risk Gauge** is a comprehensive risk assessment tool that bridges Traditional Finance (TradFi) risk management methodologies with Decentralized Finance (DeFi) transparency data. The application evaluates major DeFi protocols by calculating a composite risk score based on three critical dimensions:

1. **Market Risk (Volatility)**: Measures price volatility over 24-hour and 7-day periods, reflecting short-to-medium-term market uncertainty and price stability.

2. **Liquidity Risk (Total Value Locked)**: Assesses the protocol's liquidity confidence based on Total Value Locked (TVL), indicating user trust and capital commitment.

3. **Protocol Risk (Audit Quality)**: Evaluates smart contract security and governance quality through audit scores derived from publicly available security assessments.

The application presents these metrics in an intuitive, visual gauge interface that provides immediate risk categorization (Low, Moderate, High) while offering detailed breakdowns for deeper analysis.

## How It Functions

The application operates through the following workflow:

1. **Real-Time Data Fetching**: The app connects to two primary data sources:
   - **DeFiLlama API**: Retrieves current and historical TVL data for selected protocols
   - **CoinGecko API**: Fetches real-time price data and calculates volatility metrics

2. **Risk Score Calculation**: Using a proprietary algorithm inspired by Value at Risk (VaR) models and liquidity risk frameworks from traditional finance:
   - Market Risk (40% weight): Composite volatility score from 24h and 7d price changes
   - Liquidity Risk (30% weight): TVL-based risk factor (higher TVL = lower risk)
   - Protocol Risk (30% weight): Audit score-based security assessment

3. **Visual Presentation**: The risk score is displayed through:
   - Interactive Plotly gauge chart with color-coded risk zones (Green: Low, Yellow: Moderate, Red: High)
   - Detailed metrics dashboard showing individual components
   - Risk breakdown table explaining each factor's contribution

4. **Protocol Comparison**: Users can select from 8+ major DeFi protocols (Aave, Uniswap, Curve, Lido, Compound, MakerDAO, Yearn Finance, Balancer) to compare risk profiles.

## How It Differs from Existing Tools

**DeFi Risk Gauge** distinguishes itself from existing DeFi analytics tools in several key ways:

### 1. **TradFi Risk Framework Integration**
Unlike traditional DeFi dashboards that focus solely on metrics like TVL, volume, or yield, this application applies established TradFi risk management principles—specifically Value at Risk (VaR) and liquidity risk models—to DeFi protocols. This creates a bridge between traditional finance risk assessment and DeFi's transparent, on-chain data.

### 2. **Unified Risk Scoring**
While tools like DeFiLlama, DeFiPulse, or Zapper provide excellent data visualization, they present fragmented metrics. DeFi Risk Gauge synthesizes multiple risk factors into a single, interpretable score (0-100 scale), making it easier for users—especially those with TradFi backgrounds—to understand protocol risk at a glance.

### 3. **Composite Risk Model**
The application doesn't rely on a single metric but combines:
- **Time-weighted volatility** (not just 24h, but composite of 24h and 7d)
- **Liquidity confidence** (TVL-based risk tiers, not absolute values)
- **Protocol security** (audit scores integrated into the model)

This multi-dimensional approach prevents over-reliance on any single indicator.

### 4. **Visual Risk Interpretation**
The gauge interface provides immediate, intuitive risk assessment. Unlike raw data dashboards, users can instantly see whether a protocol falls into Low, Moderate, or High risk categories, with supporting visual cues (color coding, risk zones).

### 5. **Educational Focus**
The app includes explanatory sections that teach users about DeFi risks and how TradFi methodologies apply to decentralized protocols. This makes it valuable for both TradFi professionals exploring DeFi and DeFi natives learning about formal risk assessment.

### 6. **No Wallet Connection Required**
Unlike many DeFi tools that require wallet connections, DeFi Risk Gauge provides risk assessment without requiring user funds or wallet access. This makes it suitable for research, due diligence, and educational purposes.

## Originality and Contribution

**DeFi Risk Gauge** contributes to financial-market processes and problem-solving by:

1. **Bridging Two Worlds**: It translates TradFi risk assessment language into DeFi context, helping institutional investors and risk managers understand DeFi risks using familiar frameworks.

2. **Transparency Enhancement**: By aggregating publicly available but fragmented data (TVL, price volatility, audit reports), it creates a unified risk picture that individual protocols don't always provide.

3. **Standardization**: It proposes a standardized risk scoring methodology that could serve as a foundation for DeFi risk benchmarking and comparative analysis.

4. **Accessibility**: Makes sophisticated risk assessment accessible to users without deep technical knowledge or complex data analysis tools.

5. **Real-Time Decision Support**: Provides actionable risk intelligence that can inform investment decisions, protocol selection, and risk management strategies in real-time.

The application's originality lies not in the individual components (which use established APIs and methodologies) but in their synthesis: creating a TradFi-inspired risk assessment tool specifically designed for the DeFi ecosystem, with its unique characteristics of transparency, composability, and 24/7 operation.

