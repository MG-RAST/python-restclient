
import requests



class RestClient:
    
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers

    def get(self, path="/", headers=None, params=None):
        r = requests.get(self.url+"/"+path, headers=headers, params=params)
        return r
        
    # get function that handles REST pagination
    def get_stream(self, path, headers=None, params=None, offset=0, end=None, limit = 50):
        position = offset
    
        # merge values
        if self.headers != None:
            if headers == None:
                headers = {}
                
            for k, v in self.headers.items():
                headers[k]=v
    
        while True:
            offset = position
        
            params['limit'] = limit
            params['offset'] = offset
            results = self.get(path, params=params, headers = headers)
            obj = results.json()
            if not "data" in obj:
                break
            
            if len(obj['data']) == 0:
                break
            
            for element in obj['data']:
                yield element
                position += 1
                
                if end != None:
                    if position >= end:
                        break
                



