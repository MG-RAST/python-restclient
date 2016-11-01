#!/usr/bin/env python3


from restclient import RestClient


# You could also pass OAuth in the constructor
c = RestClient("http://api.metagenomics.anl.gov")

print("-------------\n")
response = c.get("/")
print(response.json())


print("-------------\n")
response = c.get("/metagenome", params={"verbosity": "minimal"})
print(response.json())


print("-------------\n")
for elem in c.get_stream("/metagenome", params={"verbosity": "minimal"}):
    print(elem)
