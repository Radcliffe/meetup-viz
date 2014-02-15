#!/usr/bin/env python
from collections import defaultdict
import csv
import json

membership = defaultdict(set)
group_names = dict()
num_members = dict()
group_ids = []
graph = {"nodes": [], "edges": []}

with open("groups.csv", "rb") as csv_file:
    f = csv.reader(csv_file, delimiter=',', quotechar='"')
    f.next()
    for row in f:
        print row
        group_id, group_name, link, members, created, join_mode = row
        if int(members) > 0:
            group_ids.append(group_id)
            group_names[group_id] = group_name
            num_members[group_id] = members
            graph["nodes"].append({"name": group_name})
num_groups = len(group_ids)

with open("members.csv", "r") as f:
    f.readline()
    for line in f.readlines():
        group_id, member_id, joined = line.split(",")
        membership[group_id].add(member_id)

for i in xrange(num_groups-1):
    group1 = group_ids[i]
    g1 = len(membership[group1])
    for j in xrange(i+1, num_groups):
        group2 = group_ids[j]
        g2 = len(membership[group2])
        common_members = len(membership[group1].intersection(membership[group2]))
        if common_members > 0:
            corr = common_members / (g1*g2)**0.5
            if corr > 0.1:
                graph["links"].append({"source": i, "target": j, "value": corr})

with open("common_members.csv", "wt") as f:
    f.writeline(json.dumps(graph, sort_keys=True, indent=2, separators=(',', ': ')))