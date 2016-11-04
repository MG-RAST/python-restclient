#!/usr/bin/env python3


import os
from restclient import RestClient


c = RestClient("http://shock.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })

delete_nodes=[]

params={"query":1 , "type":"metagenome" , "data_type" : "profile"}

count=0
for node in c.get_stream("/node", limit=100, params=params):
    count += 1
    print(node)
    delete_nodes.append(node['id'])

print("count: %d" % (count))

for node_id in delete_nodes:
    result = c.delete("/node/"+node_id, debug=True)
    print(result.text)
