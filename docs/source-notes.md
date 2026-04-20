# Source Notes

## TLC Source

Primary source: NYC TLC Trip Record Data.

The project currently targets:

- Yellow Taxi monthly parquet files
- Green Taxi monthly parquet files
- Taxi Zone Lookup CSV as a dimension/lookup source

## Why These Sources

- official public source
- monthly partitioning aligns with batch ELT
- parquet format is suitable for lakehouse workflows
- Taxi Zone Lookup enriches location IDs with zone and borough names

## Known Modeling Notes

- Yellow and Green use similar but not identical datetime column names
- schema evolution is expected over time
- Taxi Zone Lookup is reference data, not a trip fact source
