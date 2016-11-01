#!/usr/bin/env python3

import os
from restclient import RestClient


# Example constructor with OAuth
c = RestClient("http://api.metagenomics.anl.gov", headers = { "Authorization" : "mgrast "+os.environ['MGRKEY'] })


# Example 1
response = c.get("/")
print(response.json())


# Example 2
response = c.get("/metagenome", params={"verbosity": "minimal"})
print(response.json())



print("------------------------------\n")

# Example 3: with pagination

params={"verbosity": "minimal"}
count = 0
for elem in c.get_stream("/metagenome", limit=5, params=params):
    print(elem)
    count +=1
    if count >= 10:
        break


