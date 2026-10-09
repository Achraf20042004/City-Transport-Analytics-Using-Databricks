import sqlite3, shutil

CITIES = ["chandigarh", "coimbatore", "indore", "jaipur", "kochi",
          "lucknow", "mysore", "surat", "vadodara"]   # Visakhapatnam non exportée

local_path = "/tmp/good_gold.db"
conn = sqlite3.connect(local_path)

frames = []
for city in CITIES:
    pdf = spark.table(f"transportation.gold.fait_{city}").toPandas()     # Spark → pandas
    pdf.to_sql(f"fait_{city}", conn, if_exists="replace", index=False)   # pandas → SQLite
    frames.append(pdf)

import pandas as pd
pd.concat(frames).to_sql("trips_summary", conn, if_exists="replace", index=False)
conn.close()

# copie vers un volume pour pouvoir le télécharger
shutil.copy(local_path, "/Volumes/transportation/gold/exports/good_gold.db")