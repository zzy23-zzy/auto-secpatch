from typing import TypedDict
from langgraph.graph import StateGraph, END
import os
from langchain_openai import ChatOpenAI
from executor import run_python_code

# 1. 定义状态结构
class AgentState(TypedDict):
    code: str
    error: str
    iterations: int
    is_fixed: bool

# 2. 定义修复节点
# 找到 repair_node 函数里的 llm 定义
def repair_node(state: AgentState):
    api_key = os.getenv("OPENAI_API_KEY")
    
    # 强制使用同步客户端，并关闭所有可能引起异步冲突的特性
    llm = ChatOpenAI(
    model='deepseek-chat', 
    openai_api_key=api_key, 
    openai_api_base='https://api.deepseek.com',
    temperature=0.1, # 降低随机性
    max_tokens=2000
)
    current_iter = state.get("iterations", 0)
    prompt = f"..." # 这里保持你原来的 prompt 不变
    
    # 3. 这里也是核心修改：用简单的 try-except 包裹
    try:
        response = llm.invoke(prompt)
    except Exception as e:
        # 如果 invoke 还是不行，尝试用 predict（这是老版本但更稳的方法）
        response = llm.generate([prompt]).generations[0][0]
        
    clean_code = response.content.replace("```python", "").replace("```", "").strip()
    
    return {
        "code": clean_code, 
        "iterations": current_iter + 1,
        "is_fixed": False
    }
    
    current_iter = state.get("iterations", 0)
    print(f"\n🚀 [Agent 思考中] 正在进行第 {current_iter + 1} 次修复尝试...")
    
    prompt = f"""
    你现在是一名【高级网络空间安全专家】。
    用户提供的 Python 代码存在严重的【安全漏洞】（特别是 SQL 注入风险）。
    
    你的任务：
    1. 识别代码中通过字符串拼接构造 SQL 语句的危险行为。
    2. 使用【参数化查询（Parameterized Queries）】重写数据库操作部分。
    3. 修复任何可能导致运行失败的逻辑错误。
    4. 只返回修复后的完整代码，严禁包含解释文字和 Markdown 标签（如 ```python）。
请只输出修复后的 Python 代码，不要包含任何解释、不要包含 Markdown 的 ```python 标记
    【待修复的危险代码】：
    {state['code']}
    
    【安全反馈信息】：
    {state['error']}
    """
    
    response = llm.invoke(prompt)
    # 彻底清洗掉可能干扰运行的 Markdown 格式
    clean_code = response.content.replace("```python", "").replace("```", "").strip()
    
    # 返回更新后的状态：次数+1
    return {
        "code": clean_code, 
        "iterations": current_iter + 1,
        "is_fixed": False # 默认未修复，交给 verify 节点去判断
    }

# 3. 定义验证节点
def verify_node(state: AgentState):
    print("🔍 [Agent 验证中] 正在运行测试...")
    # 调用你的 executor.py
    success, result = run_python_code(state["code"])
    
    if success:
        print("✅ 验证通过！代码运行正常。")
        return {**state, "error": "", "is_fixed": True}
    else:
        print(f"❌ 验证失败，报错：{result}")
        return {**state, "error": result, "is_fixed": False}

# 4. 定义条件判断（控制循环开关）
def should_continue(state: AgentState):
    # 核心：增加强制停止机制
    if state["is_fixed"]:
        return "end"
    if state["iterations"] >= 3:
        print("⚠️ 已达到最大尝试次数（3次），停止修复。")
        return "end"
    return "continue"

# 5. 构建工作流图
workflow = StateGraph(AgentState)

workflow.add_node("repair_code", repair_node)
workflow.add_node("verify_code", verify_node)

workflow.set_entry_point("repair_code")

# 连线
workflow.add_edge("repair_code", "verify_code")

# 使用条件边
workflow.add_conditional_edges(
    "verify_code",
    should_continue,
    {
        "continue": "repair_code",
        "end": END
    }
)

# 6. 编译
app = workflow.compile()
