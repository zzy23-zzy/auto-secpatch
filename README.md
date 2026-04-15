# 🛡️ Auto-SecPatch: 智能代码漏洞自愈 Agent

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://你的应用链接.streamlit.app) 
*(注：等上线后把上面的链接换掉)*

### 🌟 项目愿景
在“AI 驱动生产力”的时代，大模型生成的代码往往存在“能运行但不安全”的风险。**Auto-SecPatch** 是一款基于 LangGraph 状态机开发的自动化安全补丁工具，它模拟资深安全专家的思维逻辑，实现从漏洞发现到自动修复、再到运行验证的完整闭环。

---

### 🚀 核心特性
- **🧠 闭环智能体架构**: 不同于简单的单次提示（Prompt），本项目使用 **LangGraph** 构建了“审计-修复-验证-重构”的状态机逻辑，确保修复后的代码真实可用。
- **🔍 深度安全审计**: 
  - **SQL 注入消除**: 自动识别拼接 SQL 语句并重构为参数化查询。
  - **密钥脱敏**: 自动识别代码中硬编码的 API Key 或密码，并迁移至环境变量 `os.getenv`。
- **🧪 动态环境执行验证**: 集成基于 `subprocess` 的执行器，Agent 会在虚拟隔离环境中运行修复后的代码，只有通过语法和逻辑测试的补丁才会被交付。
- **📊 交互式 UI**: 基于 **Streamlit** 开发，支持实时粘贴代码审计、修复过程可视化展示及补丁一键下载。

---

### 🛠️ 技术栈
- **核心大脑**: DeepSeek-V3 / Gemini 1.5 Pro
- **逻辑编排**: LangGraph (State Machine)
- **Web 框架**: Streamlit
- **环境变量管理**: Python-dotenv

---

### 📦 快速开始

#### 1. 克隆本项目
```bash
git clone [https://github.com/你的用户名/Auto-SecPatch-Agent.git](https://github.com/你的用户名/Auto-SecPatch-Agent.git)
cd Auto-SecPatch-Agent