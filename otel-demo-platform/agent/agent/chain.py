"""LangChain pipeline: Ollama chat model + stub tools."""
import os
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda


@tool
def search(query: str) -> str:
    """Search for information. (Stub for demo.)"""
    return f"[stub search result for: {query}]"


def get_llm():
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    return ChatOllama(base_url=base_url, model=model, temperature=0)


def _summarize_step(msg):
    """Runnable step after LLM: pass-through, ensuring result has .content for _Executor."""
    if hasattr(msg, "content"):
        return AIMessage(content=msg.content)
    return AIMessage(content=str(msg))


def get_agent_executor():
    """Return a runnable that invokes the LLM (and can use tools). Simple pipeline for demo."""
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Reply briefly."),
        ("human", "{input}"),
    ])
    new_step = RunnableLambda(_summarize_step)
    chain = prompt | llm | new_step
    return _Executor(chain)


class _Executor:
    """Minimal executor: run the chain and return output content."""
    def __init__(self, chain):
        self._chain = chain

    def invoke(self, inputs: dict) -> dict:
        result = self._chain.invoke({"input": inputs["input"]})
        content = result.content if hasattr(result, "content") else str(result)
        return {"output": content}
