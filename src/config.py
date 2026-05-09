from __future__ import annotations

import os
from pathlib import Path


def load_env_file(env_path: str) -> None:
    path = Path(env_path)
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        content = line.strip()
        if not content or content.startswith("#") or "=" not in content:
            continue
        key, value = content.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def normalize_model_env() -> None:
    """
    兼容 model.env 常见命名：
    - API_KEY -> OPENAI_API_KEY
    - BASE_URL -> OPENAI_BASE_URL
    并提供默认模型名称，避免未设置 OPENAI_MODEL 时无法调用。
    """
    if not os.getenv("OPENAI_API_KEY") and os.getenv("API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.environ["API_KEY"]
    if not os.getenv("OPENAI_BASE_URL") and os.getenv("BASE_URL"):
        os.environ["OPENAI_BASE_URL"] = os.environ["BASE_URL"]
    if not os.getenv("OPENAI_MODEL"):
        os.environ["OPENAI_MODEL"] = "qwen-plus"
