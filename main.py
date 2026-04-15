import os
from dotenv import load_dotenv
from agent_logic import app

load_dotenv()

def run_auto_patch(target_file):
    # 1. 自动读取目标文件内容
    if not os.path.exists(target_file):
        print(f"❌ 找不到文件: {target_file}")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    print(f"📂 已读取文件: {target_file}，准备进行安全审计...")

    # 2. 构造 Agent 初始输入
    initial_input = {
        "code": source_code,
        "error": "Security Audit: Please scan for SQL injection or logic bugs.",
        "iterations": 0,
        "is_fixed": False
    }

    print("--- 🤖 Auto-SecPatch Agent 启动扫描 ---")
    
    # 3. 运行 Agent
    final_result = app.invoke(initial_input)

    # 4. 将修复后的代码保存到新文件，防止覆盖源码
    output_file = f"fixed_{target_file}"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_result['code'])

    print("\n" + "="*40)
    print(f"✅ 审计与修复完成！")
    print(f"💾 修复后的代码已保存至: {output_file}")
    print(f"📊 修复尝试次数: {final_result['iterations']}")
    print("="*40)

if __name__ == "__main__":
    # 指定你要扫描的文件名
    run_auto_patch("vulnerable_code.py")