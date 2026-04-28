import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from agent_logic import app as agent_app

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="Auto-SecPatch Agent", layout="wide")
st.title("🛡️ Auto-SecPatch: 智能代码漏洞自愈 Agent")

# 默认代码
default_code = """import sqlite3
def get_user(username):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()"""

code_content = st.text_area("输入 Python 代码：", value=default_code, height=400)

if st.button("🚀 开始自动审计与修复", use_container_width=True):
    if not code_content.strip():
        st.error("请输入代码")
    else:
        initial_input = {
            "code": code_content,
            "error": "Security Audit",
            "iterations": 0,
            "is_fixed": False
        }

        with st.spinner("Agent 正在修复中..."):
            try:
                # 【核心修复点】手动创建并设置事件循环，彻底解决 RuntimeError
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # 在这个循环里运行你的 Agent
                final_result = agent_app.invoke(initial_input)
                
                # 运行完关闭循环
                loop.close()

                if final_result.get("is_fixed"):
                    st.success(f"✅ 修复成功！尝试次数: {final_result.get('iterations')}")
                else:
                    st.warning("⚠️ 未能完全修复，请检查逻辑。")
                
                st.subheader("✨ 修复后的代码")
                st.code(final_result.get("code"), language="python")
            except Exception as e:
                st.error(f"❌ 运行出错: {str(e)}")
