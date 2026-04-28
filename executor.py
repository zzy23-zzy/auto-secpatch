import sys
import io
import traceback

def run_python_code(code: str):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        exec(code, globals())
        output = sys.stdout.getvalue()
        return True, output

    except Exception:
        error_msg = traceback.format_exc()
        return False, error_msg

    finally:
        sys.stdout = old_stdout
