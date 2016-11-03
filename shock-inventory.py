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
inventory['basic']={}
inventory['basic']={}
inventory['basic']['count']=0
inventory['basic']['size']=0
inventory['basic']['types']={}

inventory['basic']['count']=0
inventory['basic']['size']=0
inventory['basic']['types']={}

for node in c.get_stream("/node", limit=100):
    count +=1
    
    #if count % 10 == 0:
    #    print("count: %d" % (count))
   
    node_type = node['type']

        
    if node_type == "parts":
        created_on = node["created_on"]
        created_on_month = created_on[:7]
        if not node_type in inventory:
            inventory[node_type]={}
        
        if not created_on_month in inventory[node_type]:
            inventory[node_type][created_on_month]={}
            inventory[node_type][created_on_month]['count']=0
            
            
        inventory[node_type][created_on_month]['count']+=1
       
        continue
    
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
    
    
    
    
    
   
        
    if "attributes" in node:
        
        
        attributes = node["attributes"]
        node_attr_type = "unknown"
        
        if attributes != None:
            if "type" in attributes:
                node_attr_type = attributes["type"]
        
        if not node_attr_type in inventory['basic']['types']:
            inventory['basic']['types'][node_attr_type]= {}
            inventory['basic']['types'][node_attr_type]['count']=0
            inventory['basic']['types'][node_attr_type]['size']=0
            
            
        inventory['basic']['types'][node_attr_type]['count'] += 1
        inventory['basic']['types'][node_attr_type]['size'] += size
        
        if node_attr_type == "metagenome":
            data_type = "unknown"
            if "data_type" in attributes:
                data_type = attributes["data_type"]
            
            if not "data_types" in inventory['basic']['types'][node_attr_type]:
                inventory['basic']['types'][node_attr_type]["data_types"]={}
            
            if not data_type in inventory['basic']['types'][node_attr_type]["data_types"]:
                inventory['basic']['types'][node_attr_type]["data_types"][data_type]={}
                inventory['basic']['types'][node_attr_type]["data_types"][data_type]['count']=0
                inventory['basic']['types'][node_attr_type]["data_types"][data_type]['size']=0
                
            inventory['basic']['types'][node_attr_type]["data_types"][data_type]['count']+=1
            inventory['basic']['types'][node_attr_type]["data_types"][data_type]['size']+=size

        
    inventory['basic']['count'] += 1
    inventory['basic']['size'] += size
        

        
    if count % 500 == 0:
        print("count: %d" % (count))
        print(json.dumps(inventory, indent=4, sort_keys=True))
        print("\ndata_type\tcount\tsize(GiB)")
        for data_type in inventory['basic']['types']['metagenome']["data_types"]:
            data_type_obj= inventory['basic']['types']['metagenome']["data_types"][data_type]
            
            print("metagenome_%s\t%d\t%d" % (data_type , data_type_obj['count'], data_type_obj['size']/1073741824 ))
        for basic_type in inventory['basic']['types']:
            if basic_type != "metagenome":
                basic_type_obj = inventory['basic']['types'][basic_type]
                print("%s\t%d\t%d" % (basic_type , basic_type_obj['count'], basic_type_obj['size']/1073741824 ))
                
                

print(json.dumps(inventory, indent=4, sort_keys=True))

mb = inventory['basic']['size'] / 1000000

print("\nmegabyte: %d" % (mb))