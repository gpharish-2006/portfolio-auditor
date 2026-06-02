from agentspan.agents import Agent
from tools import get_dividend_data,suggest_rebalance

auditor = Agent(
    name="dividend_specialist",
    model="ollama/qwen2.5:3b",
    instructions=(
        """You are a Senior Portfolio Auditor. Your goal is to find upcoming 
        dividend dates and suggest if a user should hold or sell to optimize tax.
        Always use the suggest_rebalance tool for any final recommendation."""
    ),
    tools=[get_dividend_data,suggest_rebalance]
)