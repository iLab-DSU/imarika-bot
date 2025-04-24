from typing import AsyncIterator, List, Optional

from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage

from app.config import CHAT_SYSTEM_INSTRUCTION
from app.utils.helpers import call_ollama_api


class OllamaLangChainLLM:
    def __call__(self, messages: List[dict], stop: Optional[List[str]] = None) -> str:
        return call_ollama_api(messages)

    async def astream(
        self, messages: List[dict], stop: Optional[List[str]] = None
    ) -> AsyncIterator[str]:
        # stream responses from Ollama API
        async for chunk in call_ollama_api(messages):
            yield chunk


class MemoryManager:
    def __init__(self, max_token_limit: int = 4096):
        self.max_token_limit = max_token_limit
        self.ollama_llm = OllamaLangChainLLM()
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
        )
        self.system_message = SystemMessage(content=CHAT_SYSTEM_INSTRUCTION)

    def update_system_message(self, new_context: str) -> None:
        updated_content = f"{CHAT_SYSTEM_INSTRUCTION}\n\n{new_context}"
        self.system_message = SystemMessage(content=updated_content)

    def add_message(self, role: str, content: str) -> None:
        if not self.memory.chat_memory.messages or not isinstance(
            self.memory.chat_memory.messages[0], SystemMessage
        ):
            self.memory.chat_memory.messages.insert(0, self.system_message)

        if role == "user":
            self.memory.chat_memory.add_message(HumanMessage(content=content))
        elif role == "assistant":
            self.memory.chat_memory.add_message(AIMessage(content=content))
        else:
            raise ValueError("Invalid role. Must be 'user' or 'assistant'.")

    def _convert_langchain_messages(self, messages: List[BaseMessage]) -> List[dict]:
        converted = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            else:
                continue
            converted.append({"role": role, "content": msg.content})
        return converted

    def _count_tokens(self, messages: List[dict]) -> int:
        # Very naive token estimation (1 word = 1 token)
        return sum(len(msg["content"].split()) for msg in messages)

    def _trim_messages_to_fit_token_limit(
        self, messages: List[BaseMessage]
    ) -> List[BaseMessage]:
        trimmed = messages.copy()
        while (
            self._count_tokens(self._convert_langchain_messages(trimmed))
            > self.max_token_limit
        ):
            if len(trimmed) > 1:
                trimmed.pop(1)  # Keep system message at index 0
            else:
                break
        return trimmed

    def get_history(self) -> List[BaseMessage]:
        return self._convert_langchain_messages(self.memory.chat_memory.messages)

    def get_trimmed_history(self) -> List[dict]:
        messages = self.memory.chat_memory.messages
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [self.system_message] + messages
        trimmed = self._trim_messages_to_fit_token_limit(messages)
        return self._convert_langchain_messages(trimmed)

    async def generate_response(self, user_input: str) -> AsyncIterator[str]:
        self.add_message("user", user_input)
        messages_to_send = self.get_trimmed_history()
        response = ""

        async for chunk in self.ollama_llm.astream(messages_to_send):
            response += chunk
            yield chunk

        self.add_message("assistant", response)

    def clear(self) -> None:
        self.memory.clear()
