
import requests



class RestClient:
    
    def __init__(self, url, headers=None, auth=None):
        self.url = url
        self.session = requests.session()
        if headers:
            self.session.headers = headers
        if auth:
            self.session.auth = auth

    def get(self, path="/", headers=None, params=None, debug=False):
        if debug:
            print("GET %s/%s\n" % (self.url, path))
            
        r = self.session.get(self.url+"/"+path, headers=headers, params=params)
        if debug:
            print("GET %s\n" % (r.url))
        return r
    
    def delete(self, path="/", headers=None, params=None, debug=False):
                
        if debug:
            print("DELETE %s/%s\n" % (self.url, path))
        r = self.session.delete(self.url+"/"+path, headers=headers, params=params)
        if debug:
            print("DELETE %s\n" % (r.url))
        return r
        
    # get function that handles REST pagination
    def get_stream(self, path, headers=None, params=None, offset=0, end=None, limit=50, debug=False):
        position = offset
    
        if params == None:
            params={}
            
        
    
        while True:
            offset = position
        
            params['limit'] = limit
            params['offset'] = offset
            results = self.get(path, params=params, headers = headers, debug=debug)
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
                



