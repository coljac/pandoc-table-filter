# Pandoc table filter for 2-column mode

## Version 0.1

This is a pandoc filter (so, invoke with `pandoc -F /path/to/table_filter.py`). Instead of the pandoc default table environment which uses longtable, it will create a regular `{table}` which is compatible with 2-column layouts. If you want the table to **span two columns**, name the table `xxx_2col`, for instance `Table: Here's my caption. {#tbl:nicetable_2col}`. In that case, the tex will end up with a `{table*}` environment.

Requires python and the `pandocfilters` package, (`pip install pandocfilters`).





