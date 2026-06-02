from agentspan.agents import tool
import yfinance as yf

@tool
def get_dividend_data(ticker: str):
    """Fetches ex-dividend dates and yields for a stock ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "ticker": ticker, 
            "ex_date": info.get("exDividendDate", "unknown"),
            "yield": info.get("dividendYield", 0),
            "status": "Found Data"
        }
    except Exception as e:
        return {"error": f"Could not fetch data for {ticker}: {str(e)}"}

@tool(approval_required=True)
def suggest_rebalance(ticker: str, action: str):
    """Suggests a specific Financial move. REQUIRES HUMAN APPROVAL."""
    return f"Suggested Rebalance: {action} {ticker} to optimize dividend tax."