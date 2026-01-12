## Why data format decisions define cost, performance, and scalability

We wrote the same 1M rows dataset in CSV, Parquert & Avro

Results:
- CSV was the largest due to text storage -- 649Mib
- Avro reduced the size using binary encoding -- 462Mib
- Parquet was the smallest due to columnar compression -- 420Mib

### CSV -- Plain text, Row-Based storage

No compression or encoding, No Schema or data types.
Each record is stored row by row delimitted by new line and values are stored as plain text characters.

```
1,John,john@email.com,IN,50000,2025-01-01
2,Alice,alice@email.com,IN,60000,2025-01-01
```

**Pros:** Simple, human-readable, universally compatible\
**Cons:** Large file size, no schema enforcement, slower queries\
**Best for:** Data exchange, simple datasets, human readable

### Avro -- Binary, Row-Based storage

Avro is a row based stored data format and a data serialization framework. It uses JSON to define schema and serializes data in binary format. 
Rows are organized into blocks, with each block containing multiple rows for better compression.

```
[Schema metadata]
{
    "type": "record",
    "name": "UserActivity",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "activity", "type": "string"},
        {"name": "timestamp", "type": "long"}
    ]
}
 + 
[Sync Marker]

[Binary encoded row 1] + 
[Binary encoded row 2] + ...

[Sync Marker]
```

Sync Marker: A randomnly generated 16-byte marker to separate the data blocks. This allows files to be split efficiently when processed by distributed systems for processing.

**Pros:** Compact, schema evolution support, fast serialization\
**Cons:** Not human-readable, requires schema knowledge\
**Best for:** Streaming Data, event pipelines, write-heavy systems

### Parquet -- Binary, Columnar storage

Parquet is columnar based storage desgined for efficient data processing & analytics. 

Each parquet file starts with 4-byte magic number `PAR 1`. This file is divided into row groups, inside each row group, data for each column is stored separately in column chunks, allowing for fast access to specific columns.
Each column chunk contains pages, these pages actually holds the data.

```
[PAR 1].        # Magic Number
[Row Group 1]
    [Column chunk: IDs] 
        [Data Page 1]
        [Data Page 2]
    [Column chunk: Names]
        [Date Page 1]
        [Data Page 2]

[Footer]
{
    "schema": [...],
    "rowGroupOffsets" : [...],
    "numRows": 1000,
    "createdBy": ""
}

```

**Pros:** Smallest file size, excellent for analytical queries, efficient compression\
**Cons:** Slower writes, overkill for small datasets\
**Best for:** Data warehouses, analytics, OLAP workloads, big data processing




### Columar Pruning (Parquet)

When querying only a subset of columns:
- CSV and Avro read the entire dataset
- Parquet reads only the required columns

Spark Physical Plan showed for Parquet:
    ReadSchema: struct<id:bigint>


This is possible because Parquet stores data column-wise, allowing query engines to physically skip unused columns and reduce IO.

##### Observation

Parquet and Avro looks similar in the query plan, but works differently at the storage level. The ReadSchema looks identical for both query plans as you saw in the notebook, but they mean different things internally.

1. Avro supports column projection but not column pruning.
2. Avro still reads and decodes full rows from disk. Unused columns are discarded only after decoding.

Note: 
    `ReadSchema tells you which columns spark will materialized into spark rows. It won't tell you how many bytes it read from disk. So Avro still reads full rows, decode the fields, only return the "id" to Spark.`

Conclusion: 
    `Parquet physically skips unused columns at disk level, which significantly reduces IO and improves performance.`


### Schema Evolution: Parquet and Avro

#### Avro
Avro natively supports schema evolution by embedding the schema with each file. When a producer adds a new column, older records that lack the field are automatically populated with default or null values at read time. No special configuration is required.



#### Parquet
Parquet does not support schema evolution natively. Schema evolution is handled by the query engine (Spark) by merging schemas across multiple files at read time. Additive schema changes work only when schema merging is enabled.