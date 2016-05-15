import requests
from pprint import pprint
from re import match

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
            m = match(r'[(]([a-z]*) .*[)]', action)
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


pprint(plan('domain.txt', 'problem.txt'))
