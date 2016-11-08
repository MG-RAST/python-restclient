#!/usr/bin/env python3


import os
import sys
sys.path.insert(0, "..")
from restclient import RestClient


c = RestClient("http://shock.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })

delete_nodes=[]

#http://shock.metagenomics.anl.gov/node?querynode&owner=f6b96a9e-471b-4a24-beb4-840472b33a5a&attributes=null&offset=100000&type=basic&direction=asc
params={"querynode":1 , "owner":"f6b96a9e-471b-4a24-beb4-840472b33a5a" , "attributes" : "null", "type":"basic", "file.size":"0", "direction" : "asc"}
#params={"query":1 , "type":"metagenome" , "data_type" : "profile"}

count=0
for node in c.get_stream("/node", limit=1000, params=params, debug=True):
    count += 1
    
    if node['file']['size'] > 0:
        continue
        
    if 'attributes' in node:
        leave = False
        leave_reason="none"
        attributes = node['attributes']
        if attributes != None:
            if type(attributes) is str:
                attributes_str = attributes
                if not attributes_str == 'None':
                    print("attributes_str: %s" % (attributes_str))
                    leave = True
                    leave_reason="is a string, but not None (%s)" % (attributes_str)
            
            else:
                print("attributes not str")
                leave = True
                leave_reason="something other than string (%s)" % (str(type(attributes)))
            
            if leave:
                print(node)
                print("found attributes")
                print("leave_reason: %s" % (leave_reason))
                print(attributes)
                sys.exit(0)
    
    created_on = node["created_on"]
    #created_on_month = created_on[:7]
    created_on_year = int(created_on[:4])
    
    if created_on_year > 2014:
        break
    
    print(node)
    if created_on_year < 2016:
        print("delete old %d" % (created_on_year))
        delete_nodes.append(node['id'])
    else:
        print("keep new")

print("count: %d" % (count))

for node_id in delete_nodes:
    result = c.delete("/node/"+node_id, debug=True)
    print(result.text)
