# coding: utf-8
import sys
import lxml.html
import tablib
import requests

try:
    url = sys.argv[1]
except:
    url = "http://www.cstv.com/printable/schools/army/sports/m-soccer/sched/army-m-soccer-sched.html?frame=bottom"


def process_page(url):

    content = requests.get(url).content
    root = lxml.html.fromstring(content)

    html_tables = root.xpath('//table[@id="schedtable"]')

    table = extract_table(html_tables[0])

    return table

def extract_table(table):
    rows = []
    for tr in table.xpath('tr'):
        row = []
        for td in tr:
            row.append(td.text_content().encode('utf8'))
        rows.append(row)
    return rows

def create_dataset(table_data):

    headers = table_data[0]
    table_data = table_data[1:]

    ds = tablib.Dataset(headers=headers)

    for row in table_data:
        if len(row) != len(headers):
            continue
        data = row[:]
        ds.append(data)
    return ds


def _export(ds, type):
    """
    type must be one of:
        'csv','xls','xlsx','json','yaml','html'
    """
    try:
        return ds.__getattribute__(type)
    except Exception, e:
        sys.stderr.write(e)
        return str(e)


def save_data(ds):

    for type in ('xls','csv','xlsx','json','html','yaml'):
        filename = 'out/ds.%s' % type
        with open(filename, 'w') as ofile:
            ofile.write(_export(ds, type))


if __name__ == '__main__':
    ret = process_page(url)
    ds = create_dataset(ret)
    save_data(ds)

