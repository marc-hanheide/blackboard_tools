from zipfile import ZipFile
from re import match
from datetime import datetime

zf = ZipFile('gradebook.zip')

records = []

for f in zf.namelist():
    m = match('([^_]*)_([0-9]*)_attempt_(.*).txt$', f)
    if m:
        record = {
            'assignment': m.group(1),
            'sid': m.group(2),
            'date': datetime.strptime(m.group(3), '%Y-%m-%d-%H-%M-%S')
        }
        records.append(record)
        print record
