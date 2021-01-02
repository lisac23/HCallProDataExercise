import ndjson
from datetime import datetime

visits = []
hits = []

with open('ga_sessions_20160801.json') as f:
    data = ndjson.load(f)

for d in data:
    visit_start_time = int(d['visitStartTime'])
    visit_insert_dict = {'full_visitor_id:': d['fullVisitorId'],
                         'visit_id': d['visitId'],
                         'visit_start_time': d['visitStartTime'],
                         'browser': d['device']['browser'],
                         'country': d['geoNetwork']['country']}
    visits.append(visit_insert_dict)
    for hit in d['hits']:
        hit_time = int(hit['time'])
        hit_ts = datetime.utcfromtimestamp(int(hit['time']) + int(d['visitStartTime']))
        hits_insert_dict = {'full_visitor_id': d['fullVisitorId'], 'visit_id': d['visitId'],
                            'hit_number': hit['hitNumber'], 'type': hit['type'], 'hit_timestamp': str(hit_ts),
                            'page_path': hit['page']['pagePath'], 'page_title': hit['page']['pageTitle'],
                            'hostname': hit['page']['hostname']
                            }
        hits.append(hits_insert_dict)

with open('visits.json', 'w') as of_visits:
    ndjson.dump(visits, of_visits)

with open('hits.json', 'w') as of_hits:
    ndjson.dump(hits, of_hits)