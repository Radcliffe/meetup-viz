#!/usr/bin/env python

# Generate a force-directed graph layout using D3.js to visualize relationships between
# meetup groups in the Twin Cities area related to information technology.

import urllib2
import json
import time

ZIP = '55401'
TECH = 34

# Get API key
f = open("meetup.key", "r")
API_KEY = f.readline().strip()
f.close()

groups_table = []
members_table = []


def get_request_url(search_type, **kwargs):
    url = "http://api.meetup.com/2/%s.json/?key=%s" % (search_type, API_KEY)
    for key, value in kwargs.iteritems():
        url += "&%s=%s" % (key, value)
    return url

if __name__ == "__main__":
    request_url = get_request_url('groups', zip=ZIP, category_id=TECH)
    data = urllib2.urlopen(request_url).read()
    groups_json = json.loads(data)['results']
    counter = 0
    print len(groups_json), " groups"
    for group in groups_json:
        counter += 1
        print counter, group['name']
        group_id = str(group['id'])
        group_name = '"' + group['name'] + '"'
        link = group['link']
        members = str(group['members'])
        created = str(group['created'])
        join_mode = str(group['join_mode'])
        row = [group_id, group_name, link, members, created, join_mode]
        groups_table.append(','.join(row)+'\n')

        for offset in range(1+(group['members']-1)/100):
            request_url = get_request_url('members', group_id=group['id'], offset=offset)
            time.sleep(0.5)
            data = urllib2.urlopen(request_url).read()
            members_json = json.loads(data)['results']
            for member in members_json:
                members_table.append(str(group['id'])+','+str(member['id'])+','+str(member['joined'])+'\n')

    f = open("groups.csv", "w")
    f.write('id,name,link,members,created,join_mode\n')
    f.writelines(groups_table)
    f.close()

    f = open("members.csv", "w")
    f.write('group_id,member_id,joined\n')
    f.writelines(members_table)
    f.close()
