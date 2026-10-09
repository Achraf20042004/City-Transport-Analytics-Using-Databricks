from pyspark import pipelines as dp
from pyspark.sql.functions import col, current_timestamp
from pyspark.sql.functions import md5, concat_ws, sha2

SOURCE_PATH= "/Volumes/transportation/bronze/datasource/1. data/city/"



@dp.materialized_view(
    name="ville_bronze",
    comment="City Raw Data Processing",
    table_properties={
        "quality": "bronze",
        "layer": "bronze",
        "source_format": "csv",
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true"
    }
)


def ville_bronze():
    df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").option("mode", "PERMISSIVE").option("mergeSchema", "true").option("columnNameOfCorruptRecord","_corrupt_record").load(SOURCE_PATH)

    df = df.withColumn("file_name", col("_metadata.file_path")).withColumn("ingest_datetime", current_timestamp())
    
    return df