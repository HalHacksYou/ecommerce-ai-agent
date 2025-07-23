from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3, datetime, json, pathlib
from pydantic import BaseModel
from text_to_sql_converter import nl_to_sql

DB = pathlib.Path(__file__).with_name("ecommerce.db")
app = FastAPI(title="E-commerce AI Agent")

class QueryRequest(BaseModel):
    question:str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>E-commerce AI Agent</h1><p>POST /ask with JSON {'question': ...}</p>"

@app.post("/ask")
def ask(req:QueryRequest):
    sql = nl_to_sql(req.question)
    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql).fetchall()
        return {"sql":sql, "results":[dict(r) for r in rows]}
    except sqlite3.Error as e:
        raise HTTPException(400, f"SQL error: {e}")

# Quick-demo endpoints
@app.get("/demo/total-sales")
def demo_total_sales():
    q = "SELECT ROUND(SUM(total_sales),2) AS total_sales FROM total_sales_metrics WHERE total_sales>0;"
    return ask(QueryRequest(question="What is my total sales?"))
