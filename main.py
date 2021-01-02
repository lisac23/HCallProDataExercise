import ndjson
from datetime import datetime

# Initialize containers to hold results from extraction
visits = []
hits = []

# open json file and convert ndjson to a data array of json objects
with open('ga_sessions_20160801.json') as f:
    data = ndjson.load(f)

# initilialize outer loop for visits information
for d in data:
    # inline initialization of a dict to hold visits output
    visit_insert_dict = {'full_visitor_id:': d['fullVisitorId'],
                         'visit_id': d['visitId'],
                         'visit_start_time': d['visitStartTime'],
                         'browser': d['device']['browser'],
                         'country': d['geoNetwork']['country']}
    # append results to results container
    visits.append(visit_insert_dict)
    # initialize inner loop to get information for hits
    for hit in d['hits']:
        # hit_ts is a variable to hold the converted timestamp data for each hit
        hit_ts = datetime.utcfromtimestamp(int(hit['time']) + int(d['visitStartTime']))
        # inline initialization of dict to hold hits output
        # the hit_timestamp field is a string cast of the hit_ts variable calculated above, which is in datetime format
        # added information for join including the fullVisitorId and the visitId
        hits_insert_dict = {'full_visitor_id': d['fullVisitorId'], 'visit_id': d['visitId'],
                            'hit_number': hit['hitNumber'], 'type': hit['type'], 'hit_timestamp': str(hit_ts),
                            'page_path': hit['page']['pagePath'], 'page_title': hit['page']['pageTitle'],
                            'hostname': hit['page']['hostname']
                            }
        # append results to results container
        hits.append(hits_insert_dict)

# output contents of results containers to separate files in ndjson format
with open('visits.json', 'w') as of_visits:
    ndjson.dump(visits, of_visits)

with open('hits.json', 'w') as of_hits:
    ndjson.dump(hits, of_hits)