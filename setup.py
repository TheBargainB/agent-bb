from setuptools import setup, find_packages

setup(
    name="assistants-demo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "dotenv",
        "langchain",
        "langchain-core",
        "langchain-anthropic",
        "langchain-community",
        "langchain-openai",
        "langchain-tavily",
        "langgraph",
        "langgraph-cli[inmem]",
        "langgraph-sdk",
        "langgraph-supervisor",
        "pydantic",
        "python-dotenv",
        "typing-extensions",
        "yfinance",
    ],
) 