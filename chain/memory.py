from typing import List, Optional

from langchain.llms.base import LLM
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import AIMessage, HumanMessage

from app.utils.helpers import call_ollama_api


class OllamaLangChainLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return call_ollama_api(prompt)

    @property
    def _llm_type(self) -> str:
        return "ollama"


class MemoryManager:
    def __init__(self, max_token_limit=4096):
        self.ollama_llm = OllamaLangChainLLM()
        self.memory = ConversationSummaryBufferMemory(
            llm=self.ollama_llm, max_token_limit=max_token_limit
        )

    def summarize_with_ollama(self, text: str) -> str:
        prompt = f"Summarize this conversation history concisely:\n{text}"
        return call_ollama_api(prompt)

    def add_message(self, role: str, content: str) -> None:
        if role == "user":
            self.memory.chat_memory.add_message(HumanMessage(content=content))
        elif role == "assistant":
            self.memory.chat_memory.add_message(AIMessage(content=content))
        else:
            raise ValueError("Invalid role. Must be 'user' or 'assistant'.")

    def get_summary(self) -> str:
        return self.memory.load_memory_variables({})["history"]

    def clear(self) -> None:
        self.memory.clear()
