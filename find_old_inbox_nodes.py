#!/usr/bin/env python3

import os
import json
from restclient import RestClient


# Example constructor with OAuth
c = RestClient("http://shock.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })

params={"querynode":1, "type": "basic", "attributes.type" : "inbox"}

total_size = {}
combined_size = 0
count =0
for elem in c.get_stream("/node", limit=100, params=params):
    #print(elem)
    
    creation_month = elem['created_on'][:7]
    #print("creation_month: "+creation_month)
    
    if not creation_month in total_size:
        total_size[creation_month]=0
    
    if  elem['expiration'] == "0001-01-01T00:00:00Z":
        size = elem['file']['size']
        #print("%s      %s      %d" %(elem['created_on'], elem['expiration'], size))
        
        total_size[creation_month] += size
        combined_size += size
    count +=1
    if count % 1000 == 0:
        print(json.dumps(total_size, indent=4, sort_keys=True))
    #count >= 1000:
    #    break

#print("total_size: %d MB" % (total_size /1000000))

print(json.dumps(total_size, indent=4, sort_keys=True))

print("combined_size: %d GB" % (combined_size / 1000000000))