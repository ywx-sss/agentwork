from __future__ import annotations

from typing import Dict, List

from src.llm_client import LLMClient

TOPIC_LABELS = {
    "stack_queue": "栈与队列",
    "linked_list": "链表",
    "tree": "树与二叉树",
    "graph": "图",
    "sorting": "排序",
    "recursion_search": "递归与查找",
}


def build_study_plan(weak_topics: List[str], goal: str, days: int, llm: LLMClient) -> Dict:
    labels = [TOPIC_LABELS.get(item, item) for item in weak_topics] or ["栈与队列", "树与二叉树"]
    messages = [
        {
            "role": "system",
            "content": "你是学习规划助手，只输出 JSON。",
        },
        {
            "role": "user",
            "content": (
                "请生成可执行学习计划，输出 JSON："
                '{"goal":"...","advice":["..."],"schedule":[{"day":"第1天","focus":"...","tasks":["..."]}]}\n'
                f"薄弱知识点：{labels}\n目标：{goal or '打牢数据结构基础'}\n周期天数：{days}"
            ),
        },
    ]
    try:
        result = llm.chat_json(messages, temperature=0.2)
        return {
            "goal": str(result.get("goal", goal or "打牢数据结构基础")),
            "advice": [str(x) for x in result.get("advice", [])],
            "schedule": result.get("schedule", []),
        }
    except Exception:
        return {
            "goal": goal or "打牢数据结构基础",
            "advice": ["学习计划生成失败，请检查 model.env 后重试。"],
            "schedule": [],
        }
