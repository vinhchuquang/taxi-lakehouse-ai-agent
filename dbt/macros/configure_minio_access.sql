{% macro configure_minio_access() %}
    {% set endpoint = env_var('DUCKDB_S3_ENDPOINT', 'minio:9000') %}
    {% set access_key = env_var('MINIO_ROOT_USER', 'minioadmin') %}
    {% set secret_key = env_var('MINIO_ROOT_PASSWORD', 'minioadmin123') %}
    {% set region = env_var('DUCKDB_S3_REGION', 'us-east-1') %}
    {% set url_style = env_var('DUCKDB_S3_URL_STYLE', 'path') %}
    {% set use_ssl = env_var('DUCKDB_S3_USE_SSL', 'false') %}

    install httpfs;
    load httpfs;

    create or replace secret minio_bronze (
        type s3,
        key_id '{{ access_key }}',
        secret '{{ secret_key }}',
        region '{{ region }}',
        endpoint '{{ endpoint }}',
        url_style '{{ url_style }}',
        use_ssl {{ use_ssl }}
    );
{% endmacro %}
