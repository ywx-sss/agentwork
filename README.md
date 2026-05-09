# 数据结构智能学伴

上传代码

用浏览器就能用的《数据结构》学习助手：提问、练题、看薄弱点、生成学习计划，学习过程会保存在本机。

## 你能做什么

- **知识问答**：用自然语言问课程相关概念，结合在线资料做检索与回答  
- **学情诊断**：根据你的提问与练习记录，总结当前水平与薄弱方向  
- **练习与反馈**：按知识点出题，并对你的作答给出改进建议  
- **学习规划**：生成阶段性学习安排，便于按计划推进  
- **学习档案**：姓名、目标与历史问答/练习记录在本地留存，下次打开接着学  

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置大模型（必填）

本工具通过 **OpenAI 兼容接口** 调用大模型（例如阿里云 DashScope、其他中转或自建服务均可）。

1. 复制 `.env.example` 为 `.env` 或 `model.env`（任选其一或两个都建，程序都会读）  
2. 按文件内说明填写：可用 `OPENAI_*` 变量，或用 `BASE_URL` + `API_KEY`（国内接口常见）  
3. 可选：设置 `OPENAI_MODEL`；不设置时默认 `qwen-plus`  

含密钥的文件只放在本机，不要提交或外传。

### 3. 启动

```bash
streamlit run app.py
```

浏览器会自动打开应用页面；若未打开，请查看终端里提示的本地地址。

## 数据与隐私

- 学习记录写入 `data/student_profile.json`（首次运行后自动生成）  
- 可参考 `data/student_profile.example.json` 了解文件结构  
- API 密钥与学习档案请只保留在本地  

## 项目结构（供查阅）

| 路径 | 说明 |
|------|------|
| `app.py` | 网页界面与主要流程 |
| `src/llm_client.py` | 大模型调用 |
| `src/knowledge_base.py` | 在线资料检索与缓存 |
| `src/qa_engine.py` | 问答 |
| `src/student_model.py` | 学习档案与学情诊断 |
| `src/exercise_engine.py` | 练习生成与评价 |
| `src/planner.py` | 学习计划 |
| `course_materials/` | 课程相关 Markdown 资料 |
