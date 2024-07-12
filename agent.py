import os
import pandas as pd
from langchain import LangChain
from openai import OpenAI



client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
chain = LangChain()

coder_assistant = client.beta.assistants.create(
    name="Coder Assistant",
    instructions="You are responsible for writing code to fetch the data from files, databases and REST APIs. You also might need to preprocess the data",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4.0"
)

portfolio_manager_assistant = client.beta.assistants.create(
    name="Portfolio Manager",
    instructions="You calculate the current value of a portfolio. Write and run code to calculate portfolio value.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4.0"
)

risk_analyst_assistant = client.beta.assistants.create(
    name="Risk Analyst",
    instructions="You analyze the portfolio and provide risk analysis and investment suggestions. Write and run code for risk analysis.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4.0"
)

chain.register_assistant(coder_assistant, name="coder")
chain.register_assistant(portfolio_manager_assistant, name="portfolio_manager")
chain.register_assistant(risk_analyst_assistant, name="risk_analyst")

# 1. Fetch Data
fetch_data_prompt = """
Write a Python function to load a CSV file named 'portfolio.csv' into a Pandas DataFrame. The CSV file contains columns: Asset, Type, Amount.
"""

# 2. Calculate Portfolio Value
calculate_value_prompt = """
Write a Python function that calculates the current value of each asset in a portfolio. The function should take a DataFrame and a dictionary of current prices as inputs and add a new column 'Current_Value' to the DataFrame.
"""

# 3. Risk Analysis and Suggestions
risk_analysis_prompt = """
Write a Python function that takes a portfolio summary (in DataFrame format) as input and returns risk analysis and investment suggestions using OpenAI's API. Use the 'text-davinci-003' model and generate a prompt based on the portfolio summary.
"""

def main():
    # Fetch Data
    fetch_data_response = chain.call_assistant("coder", fetch_data_prompt)
    exec(fetch_data_response['choices'][0]['message']['content'])
    
    current_prices = {
        'BTC': 57300,
        'ETH': 3100,
        'AAPL': 227.5,
    }

    # Calculate Portfolio Value
    calculate_value_response = chain.call_assistant("portfolio_manager", calculate_value_prompt)
    exec(calculate_value_response['choices'][0]['message']['content'])

    portfolio = load_portfolio('portfolio.csv')
    portfolio = calculate_portfolio_value(portfolio, current_prices)

    total_value = portfolio['Current_Value'].sum()
    print(f"Total Portfolio Value: ${total_value}")

    # Risk Analysis and Suggestions
    portfolio_summary = portfolio.to_string(index=False)
    risk_analysis_response = chain.call_assistant("risk_analyst", risk_analysis_prompt)
    exec(risk_analysis_response['choices'][0]['message']['content'])

    suggestions = get_risk_analysis_and_suggestions(portfolio_summary)
    print("Risk Analysis and Investment Suggestions:")
    print(suggestions)

if __name__ == "__main__":
    main()