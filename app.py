import streamlit as st
from dotenv import load_dotenv
from agent_logic import app as agent_app

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="Auto-SecPatch Agent",
    page_icon="🛡️",
    layout="wide"
)

# ===== 顶部标题 =====
st.markdown("""
# 🛡️ Auto-SecPatch
### 智能代码漏洞自愈 Agent
""")
st.markdown("---")

# ===== 默认漏洞代码 =====
default_code = """import sqlite3
def get_user(username):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()"""

# ===== 左右分栏布局 =====
col1, col2 = st.columns([1, 1], gap="large")

# ===== 左侧：代码输入 =====
with col1:
    st.markdown("### 📄 输入代码")
    
    code_content = st.text_area(
        " ",
        value=default_code,
        height=500,
        label_visibility="collapsed"
    )

    run_button = st.button("🚀 开始修复", use_container_width=True)

# ===== 右侧：修复结果 =====
with col2:
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
