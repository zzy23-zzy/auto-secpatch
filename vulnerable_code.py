import sqlite3

def get_user(username):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # ❌ 这里的代码极度危险！直接用 f-string 拼接用户输入
    query = f"SELECT * FROM users WHERE username = '{username}'"
    print(f"正在执行查询: {query}")
    cursor.execute(query)
    return cursor.fetchone()

# 模拟恶意攻击者输入
print(get_user("' OR '1'='1"))