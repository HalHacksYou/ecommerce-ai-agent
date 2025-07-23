import requests, json, textwrap

SCHEMA_PROMPT = """
Database schema:
1. ad_sales_metrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
2. total_sales_metrics(date, item_id, total_sales, total_units_ordered)
3. product_eligibility(eligibility_datetime_utc, item_id, eligibility, message)
Metrics:
 ROAS = ad_sales / NULLIF(ad_spend,0)
 CPC  = ad_spend / NULLIF(clicks,0)
 CTR  = clicks * 100.0 / NULLIF(impressions,0)
""".strip()

def nl_to_sql(question:str)->str:
    prompt = textwrap.dedent(f"""
        You are a senior data engineer. Convert the following
        user question to a valid SQLite SQL query.
        {SCHEMA_PROMPT}

        Question: \"{question}\"
        SQL:
    """)
    r = requests.post("http://localhost:11434/api/generate",
                      json={"model":"sqlcoder:7b",
                            "prompt":prompt,
                            "stream":False,
                            "options":{"temperature":0.1}})
    r.raise_for_status()
    raw = r.json()["response"].strip()
    # In most cases model returns only the query. If extra text appears, extract first SELECT.
    for line in raw.splitlines():
        if line.lower().startswith("select"):
            return line.rstrip(";") + ";"
    return raw
