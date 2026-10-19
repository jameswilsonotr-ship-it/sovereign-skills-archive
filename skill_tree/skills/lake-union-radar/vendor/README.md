# vendor
wheels/ + site-packages/ : duckdb 1.5.5, ijson, orjson, geographiclib, haversine
src/ : haversine + ijson git clones
pip download 502s on internal proxy. urllib to pypi.org worked.
scripts call vendor.bootstrap.load().
