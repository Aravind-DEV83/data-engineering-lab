## Why data format decisions define cost, performance, and scalability

We wrote the same 1M rows dataset in CSV, Parquert & Avro

Results:
- CSV was the largest due to text storage
- Avro reduced the size using binary encoding
- Parquet was the smallest due to columnar compression.


### CSV -- Plain text, Row-Based storage

No compression or encoding, No Schema or data types.
Each record is stored row by row delimitted by new line and values are stored as plain text characters.

```
1,John,john@email.com,IN,50000,2025-01-01
2,Alice,alice@email.com,IN,60000,2025-01-01
```

**Pros:** Simple, human-readable, universally compatible
**Cons:** Large file size, no schema enforcement, slower queries
**Best for:** Data exchange, simple datasets, human readable

### Avro -- Binary, Row-Based storage

Avro stores data in binary format and enforces a schema, but it still stores data row by row.
Each row is encoded in binary, rows are compressed into blocks and compressed together
```
[Schema metadata] + [Binary encoded row 1] + [Binary encoded row 2] + ...
```

**Pros:** Compact, schema evolution support, fast serialization
**Cons:** Not human-readable, requires schema knowledge
**Best for:** Streaming Data, event pipelines, write-heavy systems

### Parquet -- Binary, Columnar storage

Data organized by column, not row. Each column is compressed separately within a row group, enabling selective reads.
Uses dictionary & run length encoding, Schema is embedded in file metadata.


```
[Column 1: IDs] [Column 2: Names] [Column 3: Emails] [Column 4: Countries] [Column 5: Salaries] [Column 6: Dates]
```

**Pros:** Smallest file size, excellent for analytical queries, efficient compression
**Cons:** Slower writes, overkill for small datasets
**Best for:** Data warehouses, analytics, OLAP workloads, big data processing
