import xml.etree.ElementTree as ET
import re
from math import log
tree = ET.parse('index.xml')
root = tree.getroot()


nodes = set([])
edges = set([])

def parse(s):
    r = re.search('^.*/(.*)\.py \(([0-9]*)%\)$', s)
    return (r.group(1), r.group(2))

cutoff = 10.0

for r in  root.findall(".//tr[td]"):
    f1 = parse(list(r[0])[0].text)
    f2 = parse(list(r[1])[0].text)
    value = max(int(f1[1]), int(f2[1]))
    if (value >= cutoff):
        nodes.add(f1[0])
        nodes.add(f2[0])
        edges.add((f1, f2))

print "graph {"
for e in edges:
    value = max(float(e[0][1]), float(e[1][1]))
    print '%s -- %s [penwidth=%f]' % (e[0][0], e[1][0], log(value-cutoff+2,2))
print "}"