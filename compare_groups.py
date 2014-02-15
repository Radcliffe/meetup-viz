#!/usr/bin/env python
from collections import defaultdict
from itertools import combinations
import csv

membership = defaultdict(set)
group_names = dict()
num_members = dict()
group_ids = []

with open("groups.csv", "rb") as csvfile:
    f = csv.reader(csvfile, delimiter=',', quotechar='"')
    f.next()
    for row in f:
        print row
        group_id, group_name, link, members, created, join_mode = row
        if int(members) > 0:
            group_ids.append(group_id)
            group_names[group_id] = group_name
            num_members[group_id] = members


# 'group_id', 'member_id', 'joined'
f = open("members.csv", "r")
f.readline()
for line in f.readlines():
    group_id, member_id, joined = line.split(",")
    membership[group_id].add(member_id)
f.close()

f = open("common_members.csv", "w")
output = ["id1, name1, members1, id2, name2, members2, common, correlation\n"]
for group1, group2 in combinations(group_ids, 2):
    g1 = len(membership[group1])
    g2 = len(membership[group2])
    common_members = len(membership[group1].intersection(membership[group2]))
    if common_members > 0:
        corr = common_members / (g1*g2)**0.5
        if corr > 0.1:
            row = [group1, '"'+group_names[group1]+'"', num_members[group1],
                   group2, '"'+group_names[group2]+'"', num_members[group2], str(common_members), str(corr)]
            output.append(', '.join(row)+'\n')
f.writelines(output)
f.close()
