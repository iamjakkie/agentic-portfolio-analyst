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
    instructions="You calculate the current value of a portfolio.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4.0"
)

risk_analyst_assistant = client.beta.assistants.create(
    name="Risk Analyst",
    instructions="You analyze the portfolio and provide risk analysis and investment suggestions.",
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


def main():
    # Fetch Data
    fetch_data_response = chain.call_assistant("coder", fetch_data_prompt)
    exec(fetch_data_response['choices'][0]['message']['content'])
    
    current_prices = {
        'BTC': 57300,
        'ETH': 3100,
        'AAPL': 227.5,
    }

    

if __name__ == "__main__":
    main()