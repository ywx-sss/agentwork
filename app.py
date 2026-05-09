from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import load_env_file, normalize_model_env
from src.exercise_engine import evaluate_answer, generate_exercises
from src.knowledge_base import CourseKnowledgeBase
from src.llm_client import LLMClient
from src.planner import build_study_plan
from src.qa_engine import QAEngine
from src.student_model import StudentModel, TOPIC_LABELS


BASE_DIR = Path(__file__).parent
load_env_file(str(BASE_DIR / ".env"))
load_env_file(str(BASE_DIR / "model.env"))
normalize_model_env()
llm = LLMClient()
kb = CourseKnowledgeBase(str(BASE_DIR / "data" / "web_cache"))
# 启动时自动清理无效缓存
cleaned = kb.clean_invalid_cache()
if cleaned > 0:
    print(f"已清理 {cleaned} 个无效页面缓存")
student_model = StudentModel(str(BASE_DIR / "data" / "student_profile.json"), llm=llm)
qa_engine = QAEngine(kb, llm=llm)


def run_with_progress(title: str, steps: list[str], fn):
    st.markdown(f"**{title}**")
    status = st.empty()
    bar = st.progress(0)
    total = max(1, len(steps))
    for i, text in enumerate(steps, start=1):
        status.info(text)
        bar.progress(min(i - 1, total) / total)
    result = fn(status, bar, total)
    bar.progress(1.0)
    status.success("完成")
    return result


st.set_page_config(page_title="数据结构智能学伴系统", page_icon="📘", layout="wide")
st.title("数据结构智能学伴系统")
st.caption("集成知识问答、学情诊断、个性化练习、学习规划与学习记录的课程智能体原型")
if not llm.is_ready():
    st.error("未检测到可用大模型配置，请在 .env 或 model.env 中设置 API 与地址（见 .env.example）。")

with st.sidebar:
    st.header("学生画像")
    name = st.text_input("姓名", value=student_model.data["profile"].get("name", ""))
    dynamic_profile = student_model.build_dynamic_profile()
    st.markdown("**动态画像**")
    st.write(f"- 当前阶段：{dynamic_profile['stage']}")
    st.write(f"- 关注主题：{dynamic_profile['focus']}")
    st.write(f"- 画像说明：{dynamic_profile['description']}")
    goal = st.text_input(
        "学习目标（可选手动补充）",
        value=student_model.data["profile"].get("goal", ""),
    )
    student_model.data["profile"].update({"name": name, "level": dynamic_profile["stage"], "goal": goal})
    student_model.save()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["智能问答", "学情诊断", "个性化练习", "学习规划", "学习记录"]
)

with tab1:
    st.subheader("课程知识问答")
    
    # 添加实时网页检索选项
    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_area(
            "请输入你的问题",
            placeholder="例如：为什么说递归和栈有密切关系？",
            height=120,
        )
    with col2:
        use_web_search = st.checkbox(
            "实时网页检索",
            value=True,
            help="启用后会从菜鸟教程等网站实时获取最新内容"
        )
    
    if st.button("提交问题"):
        if question.strip():
            def _run_qa(status, bar, total):
                status.info("记录问题与主题识别中...")
                bar.progress(1 / total)
                topics_local = student_model.record_question(question)
                
                if use_web_search:
                    status.info("实时检索网页并调用大模型回答中...")
                else:
                    status.info("检索本地知识并调用大模型回答中...")
                bar.progress(2 / total)
                
                result_local = qa_engine.answer(question, use_web=use_web_search)
                return topics_local, result_local

            topics, result = run_with_progress(
                "问答处理中",
                ["初始化", "记录学习行为", "生成回答"],
                _run_qa,
            )
            st.markdown(result["answer"])
            st.markdown("**检索来源**")
            for source in result["sources"]:
                # 标记来源类型
                if source.startswith("http"):
                    st.write(f"- 🌐 {source}")
                elif source.startswith("local"):
                    st.write(f"- 📚 {source}")
                else:
                    st.write(f"- {source}")
            if topics:
                st.info("识别到的问题主题：" + "、".join(TOPIC_LABELS.get(item, item) for item in topics))
        else:
            st.warning("请先输入问题。")

with tab2:
    st.subheader("学习诊断结果")
    diagnosis = run_with_progress(
        "诊断处理中",
        ["读取学习记录", "调用大模型分析", "整理结果"],
        lambda status, bar, total: student_model.diagnose(),
    )
    
    # 构建雷达图数据：为所有知识点计算掌握程度得分
    all_topics = list(TOPIC_LABELS.keys())
    weak_set = set(diagnosis["weak_topics"])
    strong_set = set(diagnosis["strong_topics"])
    
    # 计算每个主题的得分（薄弱点=30 分，稳定点=80 分，未涉及=50 分）
    scores = []
    for topic in all_topics:
        if topic in weak_set:
            scores.append(30)
        elif topic in strong_set:
            scores.append(80)
        else:
            scores.append(50)
    
    radar_df = pd.DataFrame({
        "知识点": [TOPIC_LABELS.get(t, t) for t in all_topics],
        "掌握程度": scores
    })
    radar_df = radar_df.set_index("知识点")
    
    if not radar_df.empty:
        st.subheader("知识点掌握图")
        st.line_chart(radar_df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**薄弱知识点**")
        if diagnosis["weak_topics"]:
            for item in diagnosis["weak_topics"]:
                st.write(f"- {TOPIC_LABELS.get(item, item)}")
        else:
            st.write("- 暂无")
    with col2:
        st.markdown("**相对稳定知识点**")
        if diagnosis["strong_topics"]:
            for item in diagnosis["strong_topics"]:
                st.write(f"- {TOPIC_LABELS.get(item, item)}")
        else:
            st.write("- 暂无")
    st.markdown("**诊断结论**")
    summary_lines = diagnosis.get("summary", [])
    if isinstance(summary_lines, str):
        summary_lines = [summary_lines]
    for line in summary_lines:
        st.write(f"- {line}")

with tab3:
    st.subheader("围绕薄弱点生成练习")
    diagnosis = student_model.diagnose()
    default_topic = diagnosis["weak_topics"][0] if diagnosis["weak_topics"] else "stack_queue"
    topic_options = kb.all_topics()
    exercise_topic = st.selectbox(
        "选择练习主题",
        topic_options,
        index=topic_options.index(default_topic),
        format_func=lambda item: TOPIC_LABELS.get(item, item),
    )
    generation_strategy = st.selectbox(
        "出题策略",
        ["根据学生画像自适应", "仅按知识点"],
        index=0,
    )
    default_level = "中等"
    if "薄弱" in dynamic_profile.get("stage", ""):
        default_level = "基础"
    elif "较好" in dynamic_profile.get("stage", ""):
        default_level = "进阶"
    difficulty = st.selectbox(
        "题目难度",
        ["基础", "中等", "进阶"],
        index=["基础", "中等", "进阶"].index(default_level),
    )
    focus_mode = st.selectbox(
        "题目侧重",
        ["薄弱点强化", "综合训练", "考前冲刺"],
        index=0,
    )
    if st.button("生成10道练习题"):
        holder = st.empty()
        with holder.container():
            status = st.empty()
            bar = st.progress(0)

            def _progress(step: int, total: int, text: str) -> None:
                status.info(text)
                bar.progress(min(1.0, step / max(1, total)))

            st.session_state["exercise_set"] = generate_exercises(
                exercise_topic,
                kb=kb,
                llm=llm,
                count=10,
                student_profile={
                    "dynamic_profile": dynamic_profile,
                    "diagnosis": diagnosis,
                    "goal": goal,
                }
                if generation_strategy == "根据学生画像自适应"
                else {},
                generation_options={
                    "strategy": generation_strategy,
                    "difficulty": difficulty,
                    "focus_mode": focus_mode,
                },
                progress_callback=_progress,
            )
            status.success("10道题生成完成")
        st.session_state["exercise_topic"] = exercise_topic
        st.session_state["exercise_results"] = {}

    exercise_set = st.session_state.get("exercise_set", [])
    if exercise_set:
        st.markdown(f"已生成 **{len(exercise_set)}** 道题（混合题型）")
        for idx, exercise in enumerate(exercise_set, start=1):
            st.markdown(f"---\n### 第 {idx} 题（{exercise['type']}）")
            st.markdown(exercise["question"])
            if exercise.get("options"):
                for option in exercise["options"]:
                    st.write(option)
            st.info("提示：" + exercise["hint"])
            answer_key = f"answer_box_{idx}"
            answer = st.text_area("请输入你的答案", key=answer_key)
            submit_key = f"submit_one_{idx}"
            if st.button(f"提交第{idx}题", key=submit_key):
                result = run_with_progress(
                    f"第{idx}题判题中",
                    ["提交答案", "调用大模型判题", "生成反馈"],
                    lambda status, bar, total: evaluate_answer(exercise, answer or "", llm=llm),
                )
                st.session_state["exercise_results"][idx] = result
                student_model.record_exercise_result(
                    st.session_state.get("exercise_topic", exercise_topic),
                    result["correct"],
                    answer or "",
                )

            current = st.session_state.get("exercise_results", {}).get(idx)
            if current:
                st.success("判定结果：" + ("正确" if current["correct"] else "需改进"))
                st.write(f"得分：{current['score']}")
                st.write(current["feedback"])
                st.write("解析：" + current["analysis"])
                st.write("改进建议：" + current["improvement"])

        if st.session_state.get("exercise_results"):
            scores = [item["score"] for item in st.session_state["exercise_results"].values()]
            avg_score = sum(scores) / len(scores)
            st.markdown("---")
            st.subheader("本次练习统计")
            st.write(f"- 已提交题数：{len(scores)}/{len(exercise_set)}")
            st.write(f"- 平均得分：{avg_score:.1f}")

with tab4:
    st.subheader("个性化学习计划")
    days = st.slider("计划周期（天）", min_value=3, max_value=14, value=7)
    diagnosis = run_with_progress(
        "规划前诊断中",
        ["读取历史", "识别薄弱点", "准备规划输入"],
        lambda status, bar, total: student_model.diagnose(),
    )
    plan = run_with_progress(
        "学习计划生成中",
        ["分析目标与周期", "调用大模型生成计划", "整理输出"],
        lambda status, bar, total: build_study_plan(diagnosis["weak_topics"], goal, days, llm=llm),
    )
    st.markdown(f"**目标：** {plan['goal']}")
    st.markdown("**阶段建议**")
    for advice in plan["advice"]:
        st.write(f"- {advice}")
    st.markdown("**每日安排**")
    for item in plan["schedule"]:
        st.markdown(f"**{item['day']}：{item['focus']}**")
        for task in item["tasks"]:
            st.write(f"- {task}")

with tab5:
    st.subheader("学习过程记录")
    history = student_model.recent_history()
    if not history:
        st.write("当前还没有学习记录，请先进行提问或练习。")
    for item in history:
        st.write(f"- [{item['time']}] {item['content']}")
