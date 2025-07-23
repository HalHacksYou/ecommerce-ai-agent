import pandas as pd, sqlite3, pathlib

DB = "ecommerce.db"
data_dir = pathlib.Path(__file__).parent / "data"

def main():
    conn = sqlite3.connect(DB)
    pd.read_excel(data_dir/"Product-Level-Ad-Sales-and-Metrics-mapped.xlsx") \
      .to_sql("ad_sales_metrics",   conn, if_exists="replace", index=False)
    pd.read_excel(data_dir/"Product-Level-Total-Sales-and-Metrics-mapped.xlsx") \
      .to_sql("total_sales_metrics",conn, if_exists="replace", index=False)
    pd.read_excel(data_dir/"Product-Level-Eligibility-Table-mapped.xlsx") \
      .to_sql("product_eligibility",conn, if_exists="replace", index=False)

    conn.executescript("""
        CREATE INDEX IF NOT EXISTS idx_ad_item_date     ON ad_sales_metrics(item_id,date);
        CREATE INDEX IF NOT EXISTS idx_sales_item_date  ON total_sales_metrics(item_id,date);
        CREATE INDEX IF NOT EXISTS idx_elig_item        ON product_eligibility(item_id);
    """)
    conn.close()
    print("✅ SQLite database built:", DB)

if __name__ == "__main__":
    main()
