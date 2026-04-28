import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from agent_logic import app as agent_app  # 确保这里用 as agent_app 防止命名冲突

# 1. 加载环境变量
load_dotenv()

# 2. 页面基础配置 (必须是 Streamlit 的第一条指令)
st.set_page_config(
    page_title="Auto-SecPatch Agent", 
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Auto-SecPatch: 智能代码漏洞自愈 Agent")
st.markdown("---")

# 3. 侧边栏配置
with st.sidebar:
    st.header("⚙️ 控制面板")
    st.info("Agent 会自动识别 SQL 注入等漏洞并使用参数化查询修复。")
    if st.button("🧹 清除运行缓存"):
        st.cache_data.clear()
        st.rerun()

# 4. 默认代码示例
default_code = """import sqlite3

def get_user(username):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # ❌ 危险：直接使用 f-string 拼接 SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()"""

# 5. 主界面布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 待审计代码")
    code_content = st.text_area(
        "在这里输入或粘贴 Python 代码：", 
        value=default_code, 
        height=450
    )

with col2:
    st.subheader("🤖 Agent 修复过程")
    
    if st.button("🚀 开始自动审计与修复", use_container_width=True):
        if not code_content.strip():
            st.error("请输入一段代码后再试。")
        else:
            initial_input = {
                "code": code_content,
                "error": "Security Audit: Potential Vulnerability Detection.",
                "iterations": 0,
                "is_fixed": False
            }

            with st.spinner("Agent 正在思考并验证中..."):
                try:
                    # 【核心修复点】
                    # 在 Python 3.13 + Railway 环境下，必须为同步调用创建独立的事件循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        # 使用刚才导入的 agent_app
                        final_result = agent_app.invoke(initial_input)
                    finally:
                        loop.close()
                    
                    # 6. 显示结果
                    if final_result.get("is_fixed"):
                        st.success(f"✅ 修复成功！尝试次数: {final_result.get('iterations')}")
                    else:
                        st.warning("⚠️ Agent 尝试了修复但未通过验证。")

                    st.subheader("✨ 修复后的代码")
                    st.code(final_result.get("code"), language="python")
                    
                    st.download_button(
                        label="📥 下载修复后的代码",
                        data=final_result.get("code"),
                        file_name="fixed_code.py",
                        mime="text/x-python"
                    )
                except Exception as e:
                    st.error(f"❌ 运行出错: {str(e)}")
                    st.info("提示：请检查 Railway 变量中是否配置了 OPENAI_API_KEY。")
