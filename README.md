# Pandoc table filter for 2-column mode

## Version 0.1

This is a pandoc filter (so, invoke with `pandoc -F /path/to/table_filter.py`). Instead of the pandoc default table environment which uses longtable, it will create a regular {table*} which is compatible with 2-column layouts.

Requires python and the `pandocfilters` package, (`pip install pandocfilters`).

## TODOs

I intend to extend this to handle auto-detecting one and two-column tables, using the label, and a few more advanced features. 

