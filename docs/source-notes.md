# Source Notes

## TLC Source

Primary source: NYC TLC Trip Record Data.

The project currently targets:

- Yellow Taxi monthly parquet files
- Green Taxi monthly parquet files

## Why These Sources

- official public source
- monthly partitioning aligns with batch ELT
- parquet format is suitable for lakehouse workflows

## Known Modeling Notes

- Yellow and Green use similar but not identical datetime column names
- schema evolution is expected over time
- keep current scope limited to the two monthly trip parquet sources
