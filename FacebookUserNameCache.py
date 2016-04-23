import httplib
import json

facebook_api_server = 'graph.facebook.com'
facebook_user_endpoint = '/v2.6/%s?access_token=%s&method=get&format=json'

class FacebookUserNameCache:
    
    def __init__(self, access_token_filename):
        with open(access_token_filename, 'r') as access_token_file:
            self.access_token = access_token_file.read()
        self.cache = {}
        self.missed_ids = []


    def get_name_for_id(self, id):
        if id not in self.cache:
            name = self.get_name_from_facebook(id)
            self.cache[id] = name

        return self.cache[id]


    def get_stored_names_count(self):
        return len(self.cache)


    def get_missed_count(self):
        return len(self.missed_ids)


    def get_name_from_facebook(self, id):
        print "Getting name from facebook for ID %s" % id
        conn = httplib.HTTPSConnection(facebook_api_server)
        conn.request('GET', facebook_user_endpoint % (id, self.access_token))
        response = conn.getresponse()
        responseJson = json.loads(response.read())

        if 'name' in responseJson:
            name = responseJson['name']
            print "Found name: %s" % name
            return name
        else:
            self.missed_ids.append(id)
            print "No name for ID %s" % id
            return None