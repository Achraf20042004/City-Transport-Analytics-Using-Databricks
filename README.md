# City Transport Assistant

Small Streamlit app on top of city trip data. The heavy lifting (NiFi → MinIO → Databricks bronze/silver/gold) sits outside this folder. What you have here is the local serving layer: login, roles, and a text-to-SQL chatbot scoped per city.

## What this repo is

| Piece | Where it runs |
| --- | --- |
| NiFi + MinIO (ngrok) | your machines / lab setup |
| Autoloader, bronze, silver, gold notebooks | Databricks workspace only |
| Streamlit UI + LangChain agent | this folder |

Gold Unity Catalog tables are loaded into a local SQLite file (`good_gold.db`) with a Databricks notebook script (pandas + `to_sql`), then the Streamlit app queries that file. On free tier you still copy `good_gold.db` from DBFS into this project folder after the notebook runs : the export itself is the script, not a hand-built database.

The app expects one SQLite table per city (`fait_chandigarh`, `fait_coimbatore`, …), matching `CITY_TABLES` in `agent.py`.

## Cities

Chandigarh, Coimbatore, Indore, Jaipur, Kochi, Lucknow, Mysore, Surat, Vadodara.

Source tables in Databricks look like `transportation.gold.fait_<city>`.

## Roles

Stored in `auth.db` (created by `set_up_auth.py`):

- **manager** : creates `city_responsible` accounts and assigns a city
- **city_responsible** : chat only against their own city’s table

Passwords are SHA-256 hashed. Don’t commit `auth.db`.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# mac/linux
# source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set your OpenRouter key:

```
OPENROUTER_API_KEY=...
```

Init auth (once):

```bash
python set_up_auth.py
```

Get `good_gold.db` into the project root (same folder as `app.py`):

1. Run the Databricks notebook that reads the gold tables and writes them into SQLite.
2. Copy / download the resulting `good_gold.db` from DBFS into this folder.

That step lives in the Databricks workspace, not in this repo.

Run:

```bash
streamlit run app.py
```

## How the agent works (short)

1. User asks a question in natural language.
2. `agent.py` injects only that city’s table schema.
3. Model returns a SELECT.
4. We reject anything that isn’t SELECT or that touches another table.
5. Result is turned into a short answer (SQL is not shown to the user).

Model goes through OpenRouter (`langchain-openai`).

## Files

- `app.py` : login UI, manager panel, city chatbot
- `agent.py` : schema lookup, SQL generation, execution, answer
- `set_up_auth.py` : creates `auth.db` + first manager user
- `docker-compose.example.yml` : sample NiFi + MinIO stack (copy to `docker-compose.yml` and set your own passwords)
- `.env` : local secrets (never push this)

## Notes

- `auth.db` and `good_gold.db` are local paths, hardcoded to the project root.
- Medallion notebooks + the gold→SQLite export notebook stay in Databricks; this repo is only the serving app.
- New machine: venv + `.env` + `set_up_auth.py` + a fresh `good_gold.db` from the export notebook.
