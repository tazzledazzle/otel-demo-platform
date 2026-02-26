"""
Minimal LCEL chain: prompt | llm | parser. Run with: python 01_hello_chain.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Reply briefly."),
    ("human", "{input}"),
])
llm = ChatOllama(model="llama3.1", temperature=0)
parser = StrOutputParser()

chain = prompt | llm | parser

if __name__ == "__main__":
    result = chain.invoke({"input": "Say hello in one sentence."})
    print(result)
