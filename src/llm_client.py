from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import requests


class LLMClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "").rstrip("/")
        self.model = os.getenv("OPENAI_MODEL", "qwen-plus")

    def is_ready(self) -> bool:
        return bool(self.api_key and self.base_url and self.model)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        timeout_sec: int = 30,
    ) -> str:
        if not self.is_ready():
            raise RuntimeError("LLM API not configured. Please check .env or model.env.")
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            },
            timeout=timeout_sec,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.1,
        timeout_sec: int = 30,
    ) -> Dict[str, Any]:
        raw = self.chat(messages=messages, temperature=temperature, timeout_sec=timeout_sec)
        return self._extract_json(raw)

    @staticmethod
    def _extract_json(raw: str) -> Dict[str, Any]:
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model output is not valid JSON.")
        return json.loads(raw[start : end + 1])
