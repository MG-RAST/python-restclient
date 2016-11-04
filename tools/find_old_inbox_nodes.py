#!/usr/bin/env python3

import os
import json
from restclient import RestClient


# Example constructor with OAuth
c = RestClient("http://shock.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })

params={"querynode":1, "attributes.type" : "inbox"} #, 'attributes.expiration' : "0001-01-01T00:00:00Z"

creation_total_size = {}
expiration_total_size = {}

mix_total_size = {}

combined_size = 0
count =0

delete_nodes=[]

for elem in c.get_stream("/node", limit=100, params=params):
    #print(elem)
    
    creation_month = elem['created_on'][:7]
    expiration_month = elem['expiration'][:7]
    #print("creation_month: "+creation_month)
    
    mix  = creation_month+"_"+expiration_month
    
    if not mix in mix_total_size:
        mix_total_size[mix]=0
    
    if not creation_month in creation_total_size:
        creation_total_size[creation_month]=0
    
    if not expiration_month in expiration_total_size:
        expiration_total_size[expiration_month]=0
    
    #if creation_month.startswith('2016-10') and expiration_month.startswith('0001-01'):
        #delete_nodes.append(elem['id'])
        
    size = elem['file']['size']
  
    
    creation_total_size[creation_month] += size
    expiration_total_size[expiration_month] += size
    mix_total_size[mix] += size
    
    
    combined_size += size
    count +=1
    if count % 1000 == 0:
        print(json.dumps(expiration_total_size, indent=4, sort_keys=True))
    #count >= 1000:
    #    break

#print("total_size: %d MB" % (total_size /1000000))
print("creation_total_size\n")
print(json.dumps(creation_total_size, indent=4, sort_keys=True))

print("expiration_total_size\n")
print(json.dumps(expiration_total_size, indent=4, sort_keys=True))

print("mix_total_size\n")
print(json.dumps(mix_total_size, indent=4, sort_keys=True))

print("combined_size: %d GB" % (combined_size / 1000000000))
print("\n")
print(delete_nodes)
print("\n")
for node_id in delete_nodes:
    result = c.delete("/node/"+node_id, debug=True)
    print(result.text)