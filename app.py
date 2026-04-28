import streamlit as st
from dotenv import load_dotenv
from agent_logic import app as agent_app
st.markdown("""
<style>

/* 🚀 干掉顶部白色条 */
header {display: none;}

/* 页面整体背景 */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* 上边距优化 */
.block-container {
    padding-top: 1rem;
}

/* 卡片 */
.card {
    background: rgba(30, 41, 59, 0.7);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.2);
}

</style>
""", unsafe_allow_html=True)

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="Auto-SecPatch Agent",
    page_icon="🛡️",
    layout="wide"
)

# ===== 🌟 全局UI美化（核心）=====
st.markdown("""
<style>
/* 整体背景 */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
}

/* 主容器 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* 卡片效果 */
.card {
    background: rgba(30, 41, 59, 0.7);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* 标题 */
.title {
    font-size: 32px;
    font-weight: 700;
}

/* 副标题 */
.subtitle {
    color: #94a3b8;
    margin-bottom: 10px;
}

/* 按钮 */
.stButton>button {
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

/* 输入框 */
textarea {
    border-radius: 12px !important;
    background-color: #020617 !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
}

/* code块 */
pre {
    border-radius: 12px !important;
}

/* 成功提示 */
.stSuccess {
    border-radius: 12px;
}

/* warning */
.stWarning {
    border-radius: 12px;
}

/* error */
.stError {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ===== 标题 =====
st.markdown("""
<div class="title">🛡️ Auto-SecPatch</div>
<div class="subtitle">智能代码漏洞自愈 Agent</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== 默认代码 =====
default_code = """import sqlite3
def get_user(username):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()"""

# ===== 左右布局 =====
col1, col2 = st.columns([1, 1], gap="large")

# ===== 左侧 =====
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📄 输入代码")

    code_content = st.text_area(
        " ",
        value=default_code,
        height=520,
        label_visibility="collapsed"
    )

    run_button = st.button("🚀 开始修复", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ===== 右侧 =====
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 🤖 修复结果")

    if run_button:
        if not code_content.strip():
            st.error("请输入代码")
        else:
            initial_input = {
                "code": code_content,
                "error": "",
                "iterations": 0,
                "is_fixed": False,
                "max_iters": 3
            }

            with st.spinner("Agent 正在思考中..."):
                try:
                    result = agent_app.invoke(initial_input)

                    if result.get("is_fixed"):
                        st.success(f"✅ 修复成功（{result.get('iterations')} 次尝试）")
                    else:
                        st.warning("⚠️ 未完全修复")

                    st.markdown("#### ✨ 修复后的代码")
                    st.code(result.get("code"), language="python")

                except Exception as e:
                    st.error(f"❌ 出错: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)
