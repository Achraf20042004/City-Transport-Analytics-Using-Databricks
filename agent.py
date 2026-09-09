from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv(".env")

llm = ChatOpenAI(
    model="nvidia/nemotron-3.5-lightning:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

CITY_TABLES = {
    "Chandigarh": "fait_chandigarh",
    "Coimbatore": "fait_coimbatore",
    "Indore": "fait_indore",
    "Jaipur": "fait_jaipur",
    "Kochi": "fait_kochi",
    "Lucknow": "fait_lucknow",
    "Mysore": "fait_mysore",
    "Surat": "fait_surat",
    "Vadodara": "fait_vadodara"
}

def get_city_schema(table_name):
    conn = sqlite3.connect("good_gold.db")
    cursor = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )
    result = cursor.fetchone()
    conn.close()
    if result is None:
        raise ValueError(f"Table '{table_name}' does not exist")
    return result[0]

def generate_sql(question, city):
    table_name = CITY_TABLES[city]
    schema = get_city_schema(table_name)

    prompt = f"""
You are a SQL assistant for a city manager.

The manager is responsible ONLY for the city: {city}.

The ONLY table you can use is:

{schema}

Rules:
- Use ONLY the table shown above.
- The table contains data ONLY for {city}.
- NEVER filter for another city.
- If the question asks about another city, do not generate SQL and says "you have not the right to use this tables ".
- Never invent tables or columns.
- Use SQLite-compatible SQL.
- Only generate SELECT queries.
- Return ONLY the SQL query juste for this function not also for user.
- Do not use markdown.
- Do not explain anything.

Question:
{question}
"""
    response = llm.invoke(prompt)
    sql = response.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def execute_sql(sql, allowed_table):
    sql_clean = sql.strip().lower()
    if not sql_clean.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    if allowed_table.lower() not in sql_clean:
        raise ValueError(f"Unauthorized table access. Allowed table: {allowed_table}")

    conn = sqlite3.connect("good_gold.db")
    try:
        cursor = conn.execute(sql)
        result = cursor.fetchall()
    finally:
        conn.close()
    return result

def generate_answer(question, sql, result):
    prompt = f"""
You are a city data assistant.

Question:
{question}

SQL query:
{sql}

Database result:
{result}

Give ONLY the final answer to the user (the result explained simply and concisely)
Do not show your reasoning.
Do not show the SQL(very important).
Do not show analysis or steps.
Do not use phrases like "thinking process".
"""
    response = llm.invoke(prompt)
    return response.content.strip()

def ask_city(question, city):
    table_name = CITY_TABLES[city]
    for other_city in CITY_TABLES:
        if other_city.lower() in question.lower() and other_city.lower() != city.lower():
            return f"You can only access data for {city}."
    sql = generate_sql(question, city)
    result = execute_sql(sql, table_name)
    answer = generate_answer(question, sql, result)
    return answer