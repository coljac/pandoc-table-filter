#!env python

# For two-column documents.
# Probably needs work.
# Original inspiration:
# https://groups.google.com/forum/#!msg/pandoc-discuss/RUC-tuu_qf0/h-H3RRVt1coJ

import json
import pandocfilters as pf

# def logging(s, label="", mode="a"):
    # s = str(s)
    # with open("log", mode) as ff:
        # ff.write(">> " + label + " <<   " + s + "\n\n")

# def save_obj(s):
    # with open("obj.json", "w") as f:
        # f.write(json.dumps(s))

def latex(s):
    return pf.RawBlock('latex', s)


def inlatex(s):
    return pf.RawInline('latex', s)


def tbl_caption(root):
    result = []
    caption = root['c'][1][0]['c']
    res = pf.Para([inlatex(r'\caption{')] + caption + [inlatex('}')])
    return res


def tbl_alignment(root): # list of lists of dicts
    aligns = {
        "AlignDefault": 'l',
        "AlignLeft": 'l',
        "AlignCenter": 'c',
        "AlignRight": 'r',
    }
    align_string = ""
    for col in root:
        align_string += aligns[col[0]['t']]

    res = r'\begin{tabular}{@{}' + align_string  + r'@{}}'
    return latex(res)


def tbl_headers(s):
    root = s
    if root['t'] != "TableHead":
        return

    headers = []

    item = root['c'][1][0]
    if item['t'] != "Row":
        return
    for bit in item['c'][1]:
        if bit['t'] == "Cell":
            for cell_chunk in bit['c']:
                if type(cell_chunk) == list:
                    if type(cell_chunk[0]) == dict:
                        leaf = cell_chunk[0]['c'][0]
                        if leaf['t'] == "Str":
                            headers.append(leaf['c'])
                            # headers.append(leaf)


    result = []
    for cn, val in enumerate(headers):
        result.append(inlatex(val + (" & " if cn < len(headers)-1 else "")))

    result.append(inlatex(r" \\\midrule"))
    res = pf.Para(result)
    return res


def tbl_contents(s):
    result = []

    root = s[0]
    if root['t'] != "TableBody":
        return

    results = []

    for row in root['c'][3]:
        row_cells = []
        if row['t'] != "Row":
            continue
        for cell in row['c'][1]:
            if type(cell) != dict or cell['t'] != "Cell":
                continue
            content = cell['c'][4][0]['c'][0]
            if type(content) != dict or content['t'] != "Str":
                continue
            row_cells.append(content['c'])

        results.append(row_cells)
    res = []
    for row_cells in results:
        for cn, val in enumerate(row_cells):
            res.append(inlatex(val + (" & " if cn < len(row_cells) -1 else "")))
        res.append(inlatex(" \\\\ \n"))
    res.append(inlatex(r' \bottomrule'))
    res = pf.Para(res)
    return res


def do_filter(key, value, fmt, meta):
    if key == "Table":
        table = "table"
        if "_2col" in str(value[1]):
            table = "table*"

        return [
           latex(r'\begin{' + table + '}' '\n' r'\centering'),
           tbl_caption(value[1]),
           tbl_alignment(value[2]),
           latex('\n' r'\toprule' '\n'),
           tbl_headers(value[3]),
           tbl_contents(value[4]),
           latex(r"\end{tabular}"),
           latex("\\end{" + table + "}")
        ]


if __name__ == "__main__":
    pf.toJSONFilter(do_filter)

