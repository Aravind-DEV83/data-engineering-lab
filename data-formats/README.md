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
