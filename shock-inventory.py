#!/usr/bin/env python3

import os
from restclient import RestClient
import json

# Example constructor with OAuth
c = RestClient("http://shock.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })

count = 0

#params={"querynode":True, "type":"basic"}


inventory={}
inventory['basic']={}
inventory['basic']['non-virtual']={}
inventory['basic']['virtual']={}
inventory['basic']['non-virtual']['count']=0
inventory['basic']['non-virtual']['size']=0
inventory['basic']['non-virtual']['types']={}

inventory['basic']['virtual']['count']=0
inventory['basic']['virtual']['size']=0
inventory['basic']['virtual']['types']={}

for node in c.get_stream("/node", limit=100):
    count +=1
    
    if count % 10 == 0:
        print("count: %d" % (count))
   
    node_type = node['type']
    if node_type != "basic":
        if not node_type in inventory:
            inventory[node_type]=0
            
        inventory[node_type]+=1
        continue
   
   
    
    if not "file" in node:
        print(node)
        print("node has no file")
        sys.exit(1)
    node_file = node['file']
    
   
    
    
    size = 0
    if "size" in node_file:
        size = node_file["size"]
    
    virtual = False
    if 'virtual' in node and node['virtual']:
         virtual = True
    
    virtual_key = "virtual"
         
    if not virtual:
        virtual_key = 'non-virtual'
        
    if "attributes" in node:
        
        
        attributes = node["attributes"]
        node_attr_type = "unknown"
        
        if attributes != None:
            if "type" in attributes:
                node_attr_type = attributes["type"]
        
        if not node_attr_type in inventory['basic'][virtual_key]['types']:
            inventory['basic'][virtual_key]['types'][node_attr_type]= {}
            inventory['basic'][virtual_key]['types'][node_attr_type]['count']=0
            inventory['basic'][virtual_key]['types'][node_attr_type]['size']=0
            
            
        inventory['basic'][virtual_key]['types'][node_attr_type]['count'] += 1
        inventory['basic'][virtual_key]['types'][node_attr_type]['size'] += size
        
    inventory['basic'][virtual_key]['count'] += 1
    inventory['basic'][virtual_key]['size'] += size
        

        
    if count % 100 == 0:
        print(json.dumps(inventory, indent=4, sort_keys=True))


print(json.dumps(inventory, indent=4, sort_keys=True))

mb = inventory['basic']['non-virtual']['size'] / 1000000

print("\nmegabyte: %d" % (mb))