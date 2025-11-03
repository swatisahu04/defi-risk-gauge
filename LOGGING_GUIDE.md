# Logging Guide - DeFi Risk Gauge

## Overview

The DeFi Risk Gauge application includes comprehensive logging to help you debug issues and monitor application behavior. All logs are written to both a file and the console.

## Log File Location

Logs are stored in the `logs/` directory with the following naming convention:
```
logs/defi_risk_gauge_YYYYMMDD.log
```

For example: `logs/defi_risk_gauge_20241215.log`

Each day gets a new log file, making it easy to track issues over time.

## Log Levels

The application uses standard Python logging levels:

- **INFO**: General informational messages (default level)
  - App startup/shutdown
  - Protocol selection
  - Successful API calls
  - Risk score calculations
  
- **DEBUG**: Detailed diagnostic information
  - API URLs
  - Response status codes
  - Data processing steps
  - Component values
  
- **WARNING**: Warning messages that may indicate issues
  - Zero TVL/volatility data
  - Missing data fields
  - Fallback values used
  
- **ERROR**: Error messages for recoverable failures
  - API timeouts
  - HTTP errors
  - Request exceptions
  
- **EXCEPTION**: Full stack traces for unexpected errors
  - Unexpected exceptions
  - Critical failures

## What Gets Logged

### Application Lifecycle
- App initialization and startup
- Protocol selection changes
- Page rendering completion

### API Calls
- **TVL Data (DeFiLlama)**:
  - API URL
  - Response status
  - Success/failure
  - TVL values retrieved
  - Data processing steps
  
- **Price Data (CoinGecko)**:
  - API URL
  - Response status
  - Volatility metrics (24h, 7d)
  - Price and market cap
  - Composite volatility calculation

### Data Processing
- Risk score calculation steps
- Component risk factors
- Final risk scores
- Data validation warnings

### Error Handling
- Timeout errors with details
- HTTP errors with status codes
- Request exceptions with types
- Unexpected errors with full stack traces

### User Interactions
- Protocol selection
- Comparison mode activation
- Auto-refresh status
- Feature usage

### Performance
- Data fetch duration
- API call timing

## Example Log Entries

```
2024-12-15 14:30:45 - __main__ - INFO - setup_logging:52 - Logging initialized. Log file: logs/defi_risk_gauge_20241215.log
2024-12-15 14:30:45 - __main__ - INFO - <module>:59 - ================================================================================
2024-12-15 14:30:45 - __main__ - INFO - <module>:60 - DeFi Risk Gauge Application Starting
2024-12-15 14:30:45 - __main__ - INFO - <module>:150 - User selected protocol: Aave
2024-12-15 14:30:45 - __main__ - INFO - fetch_tvl:174 - Fetching TVL data for protocol: aave
2024-12-15 14:30:46 - __main__ - INFO - fetch_tvl:188 - Successfully fetched TVL for aave: $5,234,567,890
2024-12-15 14:30:46 - __main__ - INFO - fetch_volatility:264 - Fetching volatility data for CoinGecko ID: aave
2024-12-15 14:30:47 - __main__ - INFO - fetch_volatility:286 - Successfully fetched volatility data for aave: 24h=2.34%, 7d=5.67%, composite=2.45%, price=$98.1234, market_cap=$1,234,567,890
2024-12-15 14:30:47 - __main__ - INFO - compute_risk_score:377 - Risk score calculated: 25.50 (Market: 10.20, Liquidity: 6.00, Protocol: 4.50)
2024-12-15 14:30:47 - __main__ - INFO - <module>:403 - Final risk score for Aave: 25.50
```

## Using Logs to Debug Issues

### Issue: API Timeout
Look for entries like:
```
ERROR - fetch_tvl:199 - Timeout while fetching TVL for aave: ...
```

**Solution**: Check network connectivity or API availability.

### Issue: Zero Data Received
Look for entries like:
```
WARNING - <module>:346 - Zero volatility data received for Aave, may indicate API issue
WARNING - <module>:349 - Zero TVL received for Aave, may indicate API issue or new protocol
```

**Solution**: Verify API is returning data, check protocol slug/ID correctness.

### Issue: Risk Score Calculation
Look for entries like:
```
DEBUG - compute_risk_score:344 - Computing risk score - TVL: $5,234,567,890, Volatility: 2.45%, Audit: 0.85
DEBUG - compute_risk_score:363 - TVL risk tier: High (>$1B), TVL risk factor: 0.2
DEBUG - compute_risk_score:367 - Volatility risk factor: 0.0245
DEBUG - compute_risk_score:371 - Protocol risk factor: 0.1500
INFO - compute_risk_score:377 - Risk score calculated: 25.50 (Market: 10.20, Liquidity: 6.00, Protocol: 4.50)
```

**Solution**: Review component calculations to verify formula logic.

### Issue: Chart Rendering Error
Look for entries like:
```
ERROR - <module>:529 - Error rendering TVL history chart: ValueError - ...
```

**Solution**: Check data format, verify Plotly chart requirements.

## Changing Log Level

To see more detailed logs, modify the logging level in `app.py`:

```python
# In setup_logging() function, change:
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG
    ...
)
```

## Log File Management

- Logs are automatically created daily
- Old log files are not automatically deleted
- Consider periodically archiving or deleting old logs to save disk space
- Logs are excluded from git (see `.gitignore`)

## Best Practices

1. **Check logs first** when encountering issues
2. **Look for ERROR or WARNING entries** around the time of the issue
3. **Review DEBUG logs** for detailed diagnostic information
4. **Search for specific protocol names** to track issues per protocol
5. **Check timestamps** to correlate issues with specific user actions

## Log Format

Each log entry follows this format:
```
TIMESTAMP - LOGGER_NAME - LEVEL - FUNCTION:LINE - MESSAGE
```

Example:
```
2024-12-15 14:30:45 - __main__ - INFO - fetch_tvl:188 - Successfully fetched TVL for aave: $5,234,567,890
```

This format includes:
- **Timestamp**: When the event occurred
- **Logger Name**: Which logger created the entry
- **Level**: Severity of the message
- **Function:Line**: Where in the code the log was generated
- **Message**: The actual log message

## Tips for Troubleshooting

1. **Start with ERROR level**: Look for error messages first
2. **Check WARNING messages**: These indicate potential issues
3. **Review INFO messages**: Understand the flow of execution
4. **Use DEBUG when needed**: Enable DEBUG level for detailed diagnosis
5. **Search for keywords**: Use grep/search to find specific issues
6. **Compare timestamps**: Correlate log entries with user actions

## Example Troubleshooting Session

```
# Find all errors
grep ERROR logs/defi_risk_gauge_20241215.log

# Find issues for a specific protocol
grep "Aave" logs/defi_risk_gauge_20241215.log

# Find all API timeouts
grep "Timeout" logs/defi_risk_gauge_20241215.log

# Find all risk score calculations
grep "Risk score calculated" logs/defi_risk_gauge_20241215.log
```

