import requests
from pprint import pprint
from re import match
import argparse
from glob import glob
import csv


def plan(domain_file, problem_file):
    url_prefix = "http://lcas.lincoln.ac.uk/fast-downward/"
    #headers = {'content-type': 'application/x-www-form-urlencoded'}

    with open(domain_file, 'r') as domain,\
            open(problem_file, 'r') as problem:
        d = domain.read()
        p = problem.read()
        # payload = 'domain=' + d + '&problem=' + p
        payload = {'domain': d, 'problem': p}
        r = requests.post(url_prefix,
                          data=payload)
    json = r.json()
    plan = json['plan'].splitlines()
    sout = json['sout'].splitlines()

    actions = []
    if len(plan) > 1:
        for action in plan:
            m = match('[(]([a-z,_]*) .*[)]', action)
            if m:
                actions.append(m.group(1))

    result = {
        'plan': plan,
        'sout': sout,
        'solution_found': 'Solution found.' in sout,
        'length': len(plan) - 1,
        'actions': actions
    }
    return result


parser = argparse.ArgumentParser(description='compute similarity')
parser.add_argument('glob',
                    help='path glob pattern')

parser.add_argument('--problem',
                    help='list of problem files',
                    action='append')

parser.add_argument('--csv_file',
                    help='result csv file', default='pddl-results.csv')



args = parser.parse_args()

files = glob(args.glob)

with open(args.csv_file, "w") as csv_file:
    csv_writer = csv.writer(csv_file, dialect='excel')

    csv_row = ['domain_file']
    for p in args.problem:
        csv_row.append(p + ' plan')
        csv_row.append(p + ' sout')
        csv_row.append(p + ' plan length')
    csv_writer.writerow(csv_row)

    for domain_file in files:
        print domain_file
        csv_row = [domain_file]
        for problem_file in args.problem:
            try:
                p = plan(domain_file, problem_file)
                #pprint(p)
                csv_row.append(' '.join(p['actions']))
                if p['solution_found']:
                    csv_row.append('TRUE')
                else:
                    csv_row.append(p['sout'])
                csv_row.append(p['length'])
            except Exception as e:
                print "  ", e
                csv_row.append(str(e))
                csv_row.append('')
                csv_row.append('')
        csv_writer.writerow(csv_row)
