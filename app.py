import asyncio
import streamlit as st
import os
from dotenv import load_dotenv
from agent_logic import app  # 确保你的 agent_logic.py 在同级目录

# 加载环境变量
load_dotenv()

# 页面基础配置
st.set_page_config(
    page_title="Auto-SecPatch Agent", 
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Auto-SecPatch: 智能代码漏洞自愈 Agent")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 控制面板")
    max_iters = st.slider("最大修复尝试次数", 1, 5, 3)
    st.info("Agent 会在修复后自动运行测试，若失败将继续尝试，直到达到最大次数。")
    
    if st.button("🧹 清除运行缓存"):
        st.cache_data.clear()
        st.rerun()

# 默认展示的 SQL 注入示例代码
default_code = """import sqlite3

def get_user(username):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # ❌ 危险：直接使用 f-string 拼接 SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

print(get_user("' OR '1'='1"))"""

# 主界面布局：左侧输入/原始代码，右侧结果
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 待审计代码")
    # 使用 text_area 让用户可以直接在 UI 里替换代码
    code_content = st.text_area(
        "在这里输入或粘贴你想修复的 Python 代码：", 
        value=default_code, 
        height=450
    )

with col2:
    st.subheader("🤖 Agent 修复过程")
    
    # 只有点击按钮才开始运行
    if st.button("🚀 开始自动审计与修复", use_container_width=True):
        if not code_content.strip():
            st.error("请输入一段代码后再试。")
        else:
            # 构造 LangGraph 初始状态
            initial_input = {
                "code": code_content,
                "error": "Security Audit: Potential Vulnerability Detection.",
                "iterations": 0,
                "is_fixed": False
            }

            with st.spinner("Agent 正在思考并验证中..."):
                # 调用 LangGraph 编译后的 app
                //# 修改后的代码：强制在异步环境里运行这个任务
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
final_result = app.invoke(initial_input)
                
            # 显示修复状态
            if final_result["is_fixed"]:
                st.success(f"✅ 修复成功！历时 {final_result['iterations']} 次尝试。")
            else:
                st.warning("⚠️ Agent 尝试了修复但未通过验证，请检查代码逻辑。")

            st.subheader("✨ 修复后的代码")
            st.code(final_result["code"], language="python")
            
            # 提供下载按钮，方便别人使用
            st.download_button(
                label="📥 下载修复后的代码",
                data=final_result["code"],
                file_name="fixed_code.py",
                mime="text/x-python"
            )
