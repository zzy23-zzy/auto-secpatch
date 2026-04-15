import sys
import io

def run_python_code(code: str):
    """尝试运行一段代码并抓取报错"""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(code, {})
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return True, output
    except Exception as e:
        sys.stdout = old_stdout
        return False, str(e)