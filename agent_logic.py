from typing import TypedDict
from langgraph.graph import StateGraph, END
import os
from langchain_openai import ChatOpenAI
from executor import run_python_code

class AgentState(TypedDict):
    code: str
    error: str
    iterations: int
    is_fixed: bool
    max_iters: int

def repair_node(state: AgentState):
    api_key = os.getenv("OPENAI_API_KEY")
    
    llm = ChatOpenAI(
        model='deepseek-chat', 
        openai_api_key=api_key, 
        openai_api_base='https://api.deepseek.com',
        temperature=0.2,
        streaming=False
    )
    
    prompt = f"""
你是一个专业的 Python 调试工程师。

任务：
1. 修复代码中的报错
2. 保持原有功能不变
3. 不要随意删除或重写功能
4. 只在必要处修改
5. 返回完整代码，不要解释，不要Markdown
6.修复代码时，必须保持和输入代码相同的编程语言，不能自动切换成其他语言。
【原始代码】
{state['code']}

【报错信息】
{state['error']}
"""
    
    response = llm.invoke(prompt)
    clean_code = response.content.replace("```python", "").replace("```", "").strip()

    # 防止AI返回垃圾
    if len(clean_code) < len(state["code"]) * 0.5:
        clean_code = state["code"]
    
    return {
        "code": clean_code,
        "iterations": state.get("iterations", 0) + 1,
        "is_fixed": False
    }

def verify_node(state: AgentState):
    success, result = run_python_code(state["code"])
    return {
        **state,
        "error": "" if success else result,
        "is_fixed": success
    }

def should_continue(state: AgentState):
    if state["is_fixed"] or state["iterations"] >= state.get("max_iters", 3):
        return "end"
    return "continue"

workflow = StateGraph(AgentState)
workflow.add_node("repair", repair_node)
workflow.add_node("verify", verify_node)

workflow.set_entry_point("repair")

workflow.add_edge("repair", "verify")

workflow.add_conditional_edges(
    "verify",
    should_continue,
    {
        "continue": "repair",
        "end": END
    }
)

app = workflow.compile()
