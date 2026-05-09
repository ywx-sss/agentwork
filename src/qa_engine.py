from __future__ import annotations

from typing import Dict, List

from src.knowledge_base import Chunk, CourseKnowledgeBase
from src.llm_client import LLMClient

class QAEngine:
    def __init__(self, kb: CourseKnowledgeBase, llm: LLMClient) -> None:
        self.kb = kb
        self.llm = llm

    def answer(self, question: str, use_web: bool = True) -> Dict:
        """回答问题
        
        Args:
            question: 学生问题
            use_web: 是否启用实时网页检索（默认 True）
        
        Returns:
            包含答案和来源的字典
        """
        # 首先从本地和缓存检索
        chunks = self.kb.retrieve(question, use_web=use_web)
        
        # 如果启用了网页检索，同时从实时网页获取内容
        web_chunks = []
        if use_web:
            web_chunks = self.kb.retrieve_from_web(question)
        
        # 合并结果（网页内容优先，因为它是最新的）
        all_chunks = web_chunks + chunks
        
        if not all_chunks:
            return {
                "answer": "未在课程资料中检索到高度相关内容，建议换一种问法或补充关键词。",
                "sources": [],
            }

        llm_answer = self._ask_llm(question, all_chunks)
        return {
            "answer": llm_answer,
            "sources": [f"{chunk.source} / {chunk.section}" for chunk in all_chunks],
        }

    def _ask_llm(self, question: str, chunks: List[Chunk]) -> str:
        context = "\n\n".join(
            [f"[{chunk.source}-{chunk.section}]\n{chunk.text}" for chunk in chunks]
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "你是数据结构课程助教。必须严格依据给定材料回答，"
                    "不允许编造教材中不存在的事实。输出结构固定为："
                    "定义、原理、示例、易错点、延伸练习建议。"
                ),
            },
            {
                "role": "user",
                "content": f"课程资料：\n{context}\n\n学生问题：{question}",
            },
        ]
        try:
            return self.llm.chat(messages, temperature=0.2)
        except Exception:
            return "当前大模型调用失败，请检查 model.env 中的 API 配置后重试。"
