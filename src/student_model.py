from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from src.llm_client import LLMClient


TOPIC_KEYWORDS = {
    "stack_queue": ["栈", "队列", "递归", "括号匹配", "bfs"],
    "linked_list": ["链表", "结点", "指针", "头插法"],
    "tree": ["树", "二叉树", "遍历", "二叉搜索树"],
    "graph": ["图", "dfs", "bfs", "最短路径", "邻接表"],
    "sorting": ["排序", "快速排序", "归并排序", "稳定性", "复杂度"],
    "recursion_search": ["递归", "查找", "二分查找", "折半查找", "哈希"],
}

TOPIC_LABELS = {
    "stack_queue": "栈与队列",
    "linked_list": "链表",
    "tree": "树与二叉树",
    "graph": "图",
    "sorting": "排序",
    "recursion_search": "递归与查找",
}


class StudentModel:
    def __init__(self, data_file: str, llm: LLMClient) -> None:
        self.data_file = Path(data_file)
        self.llm = llm
        self.data = self._load()

    def _load(self) -> Dict:
        if self.data_file.exists():
            return json.loads(self.data_file.read_text(encoding="utf-8"))
        return {
            "profile": {"name": "", "level": "", "goal": ""},
            "history": [],
            "wrong_topics": [],
            "exercise_results": [],
        }

    def save(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def infer_topics(self, text: str) -> List[str]:
        prompt = (
            "请识别学生问题涉及的主题，返回 JSON："
            '{"topics":["stack_queue","tree"]}。'
            "topics 只能从以下列表选："
            f"{list(TOPIC_KEYWORDS.keys())}。最多返回 3 个。"
            f"学生文本：{text}"
        )
        try:
            result = self.llm.chat_json(
                [
                    {"role": "system", "content": "你是课程主题分类器，只输出 JSON。"},
                    {"role": "user", "content": prompt},
                ]
            )
            topics = result.get("topics", [])
            return [item for item in topics if item in TOPIC_KEYWORDS][:3]
        except Exception:
            return []

    def record_question(self, question: str) -> List[str]:
        topics = self.infer_topics(question)
        self.data["history"].append(
            {
                "type": "question",
                "content": question,
                "topics": topics,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        self.save()
        return topics

    def record_exercise_result(self, topic: str, correct: bool, student_answer: str) -> None:
        result = {
            "topic": topic,
            "correct": correct,
            "answer": student_answer,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.data["exercise_results"].append(result)
        self.data["history"].append(
            {
                "type": "exercise",
                "content": f"{TOPIC_LABELS.get(topic, topic)}练习：{'正确' if correct else '需改进'}",
                "topics": [topic],
                "time": result["time"],
            }
        )
        if not correct:
            self.data["wrong_topics"].append(topic)
        self.save()

    def recent_history(self, limit: int = 8) -> List[Dict]:
        return list(reversed(self.data["history"][-limit:]))

    @staticmethod
    def _clean_text(value: str) -> str:
        text = str(value or "").strip()
        if not text:
            return text
        # 常见乱码修复：UTF-8 被当作 Latin-1 解码
        if any(mark in text for mark in ["Ã", "â", "€", "™"]):
            try:
                text = text.encode("latin-1", errors="ignore").decode("utf-8", errors="ignore")
            except Exception:
                pass
        # 去掉不可见控制字符和替换字符
        text = "".join(ch for ch in text if ch >= " " or ch in "\n\t")
        text = text.replace("\ufffd", "")
        return text.strip()

    @classmethod
    def _ensure_text_list(cls, value) -> List[str]:
        if isinstance(value, str):
            cleaned = cls._clean_text(value)
            return [cleaned] if cleaned else []
        if isinstance(value, list):
            items = [cls._clean_text(x) for x in value]
            return [x for x in items if x]
        return []

    def build_dynamic_profile(self) -> Dict[str, str]:
        history = self.data.get("history", [])
        results = self.data.get("exercise_results", [])
        if not history and not results:
            return {
                "stage": "初始画像为空",
                "description": "尚未收集到学习行为数据，提交问题或完成练习后将自动生成画像。",
                "focus": "暂无",
            }

        payload = json.dumps(
            {"history": history[-12:], "exercise_results": results[-12:]},
            ensure_ascii=False,
        )
        try:
            result = self.llm.chat_json(
                [
                    {
                        "role": "system",
                        "content": "你是学习画像助手。只输出 JSON。",
                    },
                    {
                        "role": "user",
                        "content": (
                            "根据学习记录生成画像，返回 JSON："
                            '{"stage":"基础一般","description":"...","focus":"栈与队列"}。'
                            f"数据：{payload}"
                        ),
                    },
                ],
                temperature=0.1,
            )
            return {
                "stage": self._clean_text(result.get("stage", "探索阶段")),
                "description": self._clean_text(result.get("description", "建议继续提问和练习完善画像。")),
                "focus": self._clean_text(result.get("focus", "暂无")),
            }
        except Exception:
            return {
                "stage": "画像生成失败",
                "description": "大模型调用失败，请检查 model.env 配置。",
                "focus": "暂无",
            }

    def diagnose(self) -> Dict[str, List[str]]:
        if not self.data["history"] and not self.data["exercise_results"]:
            return {
                "weak_topics": [],
                "strong_topics": [],
                "summary": ["暂无学习数据，请先提问或完成练习后再进行诊断。"],
            }
        payload = json.dumps(
            {
                "history": self.data["history"][-20:],
                "wrong_topics": self.data["wrong_topics"][-20:],
                "exercise_results": self.data["exercise_results"][-20:],
                "candidate_topics": list(TOPIC_KEYWORDS.keys()),
            },
            ensure_ascii=False,
        )
        try:
            result = self.llm.chat_json(
                [
                    {
                        "role": "system",
                        "content": "你是学情诊断助手，只输出 JSON。",
                    },
                    {
                        "role": "user",
                        "content": (
                            "请识别薄弱点和相对稳定点，输出 JSON："
                            '{"weak_topics":["stack_queue"],"strong_topics":["linked_list"],"summary":["..."]}。'
                            "weak_topics/strong_topics 的值必须来自 candidate_topics。"
                            f"学习数据：{payload}"
                        ),
                    },
                ],
                temperature=0.1,
            )
            weak = [x for x in result.get("weak_topics", []) if x in TOPIC_KEYWORDS][:3]
            strong = [x for x in result.get("strong_topics", []) if x in TOPIC_KEYWORDS][:3]
            summary = self._ensure_text_list(result.get("summary", []))[:4]
            return {
                "weak_topics": weak,
                "strong_topics": strong,
                "summary": [x for x in summary if x] or ["建议补充练习数据以提高诊断可信度。"],
            }
        except Exception:
            return {
                "weak_topics": [],
                "strong_topics": [],
                "summary": ["学情诊断失败：大模型调用失败，请检查 model.env 配置。"],
            }
