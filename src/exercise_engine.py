from __future__ import annotations

import json
from typing import Callable, Dict, List

from src.knowledge_base import CourseKnowledgeBase
from src.llm_client import LLMClient


ALLOWED_TYPES = ["选择题", "填空题", "判断题", "简答题", "编程题"]


def _normalize_question(item: Dict, topic: str) -> Dict:
    item = dict(item or {})
    q_type = str(item.get("type", "简答题")).strip()
    if q_type not in ALLOWED_TYPES:
        q_type = "简答题"
    item["type"] = q_type
    item.setdefault("question", f"请说明 {topic} 的一个核心知识点，并举例说明。")
    item.setdefault("options", [])
    item.setdefault("reference_answer", "")
    item.setdefault("hint", "从定义、原理和应用场景作答。")
    item.setdefault("analysis", "请回到知识库复盘定义、原理和典型例题。")
    if q_type == "选择题":
        options = item.get("options") or []
        if len(options) < 4:
            options = ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"]
        item["options"] = options[:4]
    else:
        item["options"] = []
    return item


def _build_messages(topic: str, context: str, q_type: str, count: int) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "你是数据结构课程命题专家。严格基于材料命题，只输出 JSON，不要额外解释。",
        },
        {
            "role": "user",
            "content": (
                f"请围绕主题 {topic}，基于材料生成 {count} 道{q_type}，避免重复。\n"
                "材料如下：\n"
                f"{context}\n\n"
                '仅输出 JSON，格式：{"questions":[{"type":"选择题","question":"...","options":["A...","B...","C...","D..."],'
                '"reference_answer":"...","hint":"...","analysis":"..."}]}。\n'
                "规则：题目表述清晰、答案唯一、解析准确；非选择题 options 必须为空数组。"
            ),
        },
    ]


def _build_messages_with_profile(
    topic: str,
    context: str,
    q_type: str,
    count: int,
    student_profile: Dict | None,
    generation_options: Dict | None,
) -> List[Dict[str, str]]:
    profile_text = json.dumps(student_profile or {}, ensure_ascii=False)
    options_text = json.dumps(generation_options or {}, ensure_ascii=False)
    return [
        {
            "role": "system",
            "content": "你是数据结构课程命题专家。严格基于材料命题，只输出 JSON，不要额外解释。",
        },
        {
            "role": "user",
            "content": (
                f"请围绕主题 {topic}，基于材料生成 {count} 道{q_type}，避免重复。\n"
                f"学生画像：{profile_text}\n"
                f"出题选项：{options_text}\n"
                "请根据画像自适应控制难度和问法，并优先覆盖学生薄弱点。\n"
                "材料如下：\n"
                f"{context}\n\n"
                '仅输出 JSON，格式：{"questions":[{"type":"选择题","question":"...","options":["A...","B...","C...","D..."],'
                '"reference_answer":"...","hint":"...","analysis":"..."}]}。\n'
                "规则：题目表述清晰、答案唯一、解析准确；非选择题 options 必须为空数组。"
            ),
        },
    ]


def generate_exercises(
    topic: str,
    kb: CourseKnowledgeBase,
    llm: LLMClient,
    count: int = 10,
    student_profile: Dict | None = None,
    generation_options: Dict | None = None,
    progress_callback: Callable[[int, int, str], None] | None = None,
) -> List[Dict]:
    def _report(step: int, total: int, text: str) -> None:
        if progress_callback:
            progress_callback(step, total, text)

    total_steps = 1 + len(ALLOWED_TYPES) + len(ALLOWED_TYPES) + 1
    step = 0

    step += 1
    _report(step, total_steps, "检索网页知识库...")
    chunks = kb.retrieve(topic, top_k=4)
    context = "\n\n".join([f"[{c.source}-{c.section}] {c.text}" for c in chunks])

    distribution = {
        "选择题": 3,
        "填空题": 2,
        "判断题": 2,
        "简答题": 2,
        "编程题": 1,
    }
    if count != 10:
        distribution = {k: max(1, round(v * count / 10)) for k, v in distribution.items()}

    generated: List[Dict] = []
    for q_type, n in distribution.items():
        step += 1
        _report(step, total_steps, f"正在生成{q_type}...")
        messages = _build_messages_with_profile(
            topic,
            context,
            q_type,
            n,
            student_profile=student_profile,
            generation_options=generation_options,
        )
        payload = llm.chat_json(messages, temperature=0.2, timeout_sec=45)
        items = payload.get("questions", [])
        for item in items[:n]:
            generated.append(_normalize_question(item, topic))

    # 二次校验与补齐：不足数量时再次请求“缺失题型”
    type_count: Dict[str, int] = {t: 0 for t in ALLOWED_TYPES}
    for q in generated:
        type_count[q["type"]] += 1

    for t, need in distribution.items():
        step += 1
        _report(step, total_steps, f"校验并补齐{t}...")
        missing = max(0, need - type_count.get(t, 0))
        if missing <= 0:
            continue
        messages = _build_messages_with_profile(
            topic,
            context,
            t,
            missing,
            student_profile=student_profile,
            generation_options=generation_options,
        )
        payload = llm.chat_json(messages, temperature=0.15, timeout_sec=45)
        items = payload.get("questions", [])
        for item in items[:missing]:
            generated.append(_normalize_question(item, topic))

    final_questions = generated[:count]
    if len(final_questions) < count:
        raise RuntimeError("题目生成数量不足，请重试。")
    step += 1
    _report(step, total_steps, "题目生成完成")
    return final_questions


def evaluate_answer(exercise: Dict, student_answer: str, llm: LLMClient) -> Dict:
    messages = [
        {
            "role": "system",
            "content": "你是教学评价助手。只输出 JSON。",
        },
        {
            "role": "user",
            "content": (
                "请根据题目与学生答案进行判定。输出 JSON："
                '{"correct":"...","score":"...","feedback":"...","analysis":"...","improvement":"..."}。\n'
                f"题目：{json.dumps(exercise, ensure_ascii=False)}\n"
                f"学生答案：{student_answer}"
            ),
        },
    ]
    try:
        result = llm.chat_json(messages, temperature=0.1)
        correct_val = result.get("correct", False)
        if isinstance(correct_val, str):
            correct_val = correct_val.lower() == "true"
        return {
            "correct": bool(correct_val),
            "score": int(result.get("score", 0)),
            "feedback": str(result.get("feedback", "请根据解析继续改进。")),
            "analysis": str(result.get("analysis", "暂无解析。")),
            "improvement": str(result.get("improvement", "建议回顾定义与原理后重做。")),
        }
    except Exception:
        return {
            "correct": False,
            "score": 0,
            "feedback": "大模型判题失败，请检查 API 配置。",
            "analysis": "暂无解析。",
            "improvement": "请检查 model.env 并重新提交答案。",
        }
