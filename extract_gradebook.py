from zipfile import ZipFile
from re import match, split, IGNORECASE
from datetime import datetime
from collections import defaultdict
from pprint import pprint
from os.path import exists, join, basename
from os import makedirs, rename
from shutil import rmtree

from tempfile import mkdtemp


def parse_txt(txt):
    lines = txt.splitlines()
    pattern = '(Name|Assignment|Filename): '
    entry = defaultdict(list)
    for line in lines:
        pairs = split(pattern, line)[1:]
        if pairs:
            if pairs[0] == 'Filename':
                entry['files'].append(pairs[1])
            else:
                entry[pairs[0]] = pairs[1]
    return entry


def extract_submission(zf, record, prefix="submissions/"):
    user_dir = join(prefix, record['sid'])
    if not exists(user_dir):
        makedirs(user_dir)
    contained_zip = False
    for f in record['files']:
        try:
            zf.extract(f, user_dir)
            if match('.*\.zip$', f, flags=IGNORECASE):
                contained_zip = True
                tmp_dir = mkdtemp()
                # with record['zipfile'].open(f) as sub_file:
                # print "ZIP file %s" % f
                with ZipFile(join(user_dir, f)) as int_zip:
                    for ifn in int_zip.namelist():
                        if not match('.*/$', ifn):  # if not dir
                            int_zip.extract(ifn, tmp_dir)
                            proper_file = ifn.decode('ascii', 'ignore')
                            rename(join(tmp_dir, ifn),
                                   join(user_dir, basename(proper_file)))
                rmtree(tmp_dir)
        except Exception as e:
            print "Couldn't process file %s => %s" % (f, e)
            pprint(record)

    if not contained_zip:
        print "  record for %s did not contain a zip " \
              "file, instead these files were included:" \
              % record['sid']
        for sf in record['files']:
            print '   > %s' % sf


def parse_gradebook_file(zf):
    records = {}

    for f in zf.namelist():
        m = match('([^_]*)_([0-9]*)_attempt_(.*).txt$', f)
        if m:
            with zf.open(f) as txt_file:
                record_txt = txt_file.read()
                entry = parse_txt(unicode(record_txt, 'UTF-8'))
                record = {
                    'assignment': m.group(1),
                    'sid': m.group(2),
                    'date': datetime.strptime(m.group(3),
                                              '%Y-%m-%d-%H-%M-%S'),
                }
                record.update(entry)
            records[record['sid']] = record
    return records


with ZipFile('gradebook.zip') as zf:

    gradebook = parse_gradebook_file(zf)

    for k, v in gradebook.items():
        extract_submission(zf, v)
