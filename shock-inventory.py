#!/usr/bin/env python3

import os
from restclient import RestClient


# Example constructor with OAuth
c = RestClient("http://shock.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })

count = 0

params={"querynode":True, "type":"basic"}


inventory={}
inventory['basic']={}
inventory['basic']['non-virtual']={}
inventory['basic']['virtual']={}
inventory['basic']['non-virtual']['count']=0
inventory['basic']['non-virtual']['size']=0

inventory['basic']['virtual']['count']=0
inventory['basic']['virtual']['size']=0


for node in c.get_stream("/node", params=params):
    print(node)
   
    size = 0
    if not "file" in node:
        print("node has no file")
        sys.exit(1)
    node_file = node['file']
    
    if "size" in node_file:
        size = node_file["size"]
    
    virtual = False
    if 'virtual' in node and node['virtual']:
         virtual = True
    
    virtual_key = "virtual"
         
    if not virtual:
        virtual_key = 'non-virtual'
        
    inventory['basic'][virtual_key]['count'] += 1
    inventory['basic'][virtual_key]['size'] += size
        

    count +=1
    if count >= 1000:
        break


print(inventory)

mb = inventory['basic']['non-virtual']['size'] / 1000000

print("\nmegabyte: %d" % (mb))