#!/usr/bin/env python3
"""Read authoritative Markdown; validate unique identities and synchronize exports."""
import csv, io, json, re, sys, unicodedata
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
ROOT = Path(__file__).resolve().parents[1]
def normalized(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s).casefold() if c.isalnum())
def read_markdown():
    records=[]
    for block in (ROOT/'UNIVERSITIES.md').read_text().split('\n### ')[1:]:
        record={}
        for line in block.splitlines():
            if line.startswith('| ') and not line.startswith(('| Field ', '| ---')):
                key, value = line.strip('| ').split(' | ', 1)
                record[key]=value
        records.append(record)
    assert records, 'No records'
    identities={}
    for record in records:
        assert set(record)==set(records[0]), 'Schema mismatch'
        assert all(record.values()), 'Use Unknown for missing data'
        assert record['csc_type_b_status'] in {'CONFIRMED_2027_2028','PREVIOUS_YEAR_EVIDENCE','UNVERIFIED'}
        names=[record['university_name'],record['chinese_name']]+record['aliases'].split(';')
        for value in names:
            if value.strip()=='Unknown': continue
            key=normalized(value)
            assert key not in identities or identities[key]==record['id'], f'Duplicate identity: {value}'
            identities[key]=record['id']
    assert len({r['id'] for r in records})==len(records), 'Duplicate ID'
    return records

def source_rows():
    text=(ROOT/'SOURCES.md').read_text()
    return [dict(source_id=i,url=u,assessment=a.strip()) for i,u,a in re.findall(r'## (S\d+)\n\nURL: (\S+)\n\nAssessment: (.*?)(?=\n\n## |\Z)',text,re.S)]

def main():
    records=read_markdown(); regions=json.loads((ROOT/'data/regions.json').read_text()); sources=source_rows()
    assert len(regions)==32 and len({r['name'] for r in regions})==32
    assert all(r['status'] in {'NOT_STARTED','IN_PROGRESS','COMPLETED','NEEDS_VERIFICATION'} for r in regions)
    assert all(r['region'] in {x['name'] for x in regions} for r in records)
    source_ids={s['source_id'] for s in sources}
    assert all(set(r['source_ids'].split('; '))<=source_ids for r in records)
    progress=(ROOT/'PROGRESS.md').read_text()
    total=int(re.search(r'Total universities discovered: (\d+)',progress)[1])
    published=int(re.search(r'Universities published to GitHub: (\d+)',progress)[1])
    pending=int(re.search(r'New universities since last successful push: (\d+)',progress)[1])
    assert total==len(records) and total-published==pending, 'Counter mismatch'
    if '--check' not in sys.argv:
        (ROOT/'data/universities.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
        with (ROOT/'data/universities.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator="\n");writer.writeheader();writer.writerows(records)
        book=Workbook();book.remove(book.active)
        for name,rows in [('Universities',records),('Regions',regions),('Sources',sources)]:
            sheet=book.create_sheet(name);sheet.append(list(rows[0]))
            for row in rows: sheet.append([row[k] for k in rows[0]])
            sheet.freeze_panes='A2';sheet.auto_filter.ref=sheet.dimensions
            for cell in sheet[1]: cell.font=Font(bold=True)
            for column in sheet.columns:
                sheet.column_dimensions[column[0].column_letter].width=min(60,max(16,max(len(str(c.value or '')) for c in column)+2))
        book.save(ROOT/'exports/CHINA_CSC_TYPE_B_2027_2028.xlsx')
    assert json.loads((ROOT/'data/universities.json').read_text())==records
    with (ROOT/'data/universities.csv').open(newline='') as f: assert list(csv.DictReader(f))==records
    book=load_workbook(ROOT/'exports/CHINA_CSC_TYPE_B_2027_2028.xlsx',read_only=True)
    for name,rows in [('Universities',records),('Regions',regions),('Sources',sources)]:
        values=list(book[name].values)
        assert list(values[0])==list(rows[0])
        assert [dict(zip(values[0],v)) for v in values[1:]]==rows, f'{name} mismatch'
    book.close()
    print(f'Validated {len(records)} unique universities, {len(regions)} regions, {len(sources)} sources; Markdown/CSV/JSON/XLSX agree. Pending: {pending}.')
if __name__=='__main__': main()
