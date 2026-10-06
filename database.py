import sqlite3
from datetime import datetime

def get_db_conn():
    return sqlite3.connect("calc.db")

def add_record(expr:str,result:str):
    conn = get_db_conn()
    cur = conn.cursor()
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO history(expression,result,create_time) VALUES (?,?,?)",(expr,result,t))
    conn.commit()
    conn.close()

def get_all_history():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,expression,result FROM history ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return data

def delete_record(rid:int):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM history WHERE id=?",(rid,))
    conn.commit()
    conn.close()
