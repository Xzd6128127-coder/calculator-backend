from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import math
import uvicorn

app = FastAPI(title="Calculator Backend")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体模型
class CalcRequest(BaseModel):
    expression: str

# 初始化数据库
def init_db():
    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# POST接口，接收JSON body，修复浮点数精度
@app.post("/calculate")
def calculate(req: CalcRequest):
    try:
        expression = req.expression
        result = eval(expression, {"__builtins__": None}, vars(math))
        
        # 浮点数处理：去除尾部多余0，解决0.1+0.2精度bug
        if isinstance(result, float):
            # 最多保留10位小数
            result = round(result,10)
            # 如果是整数形式的浮点数，转成int，例如5.0 →5
            if result.is_integer():
                result = int(result)

        result_str = str(result)
        conn = sqlite3.connect("calculator.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result_str))
        conn.commit()
        conn.close()
        return {"result": result_str}
    except Exception:
        return {"result": "Error"}

# 获取历史
@app.get("/history")
def get_history():
    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()
    cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    res_list = []
    for exp, val in records:
        res_list.append({"expression": exp, "result": val})
    return res_list

# 删除全部历史
@app.delete("/history/delete")
def delete_history():
    conn = sqlite3.connect("calculator.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    return {"msg": "All history cleared"}

# ========== 启动服务 ==========
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
