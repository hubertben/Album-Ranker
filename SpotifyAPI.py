import requests
import base64
import spotipy
import datetime

from urllib.parse import urlencode


class SpotifyAPI(object):

    access_token = None
    access_token_exp = None
    access_token_prev_exp = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def auth_access_token(self): # Returns true if Auth Completed
        
        r = requests.post(self.token_url, data = self.get_token_data(), headers = self.get_token_heading())

        if(r.status_code not in range(200, 299)):
            return False
        data = r.json()
        cur = datetime.datetime.now()
        access = data['access_token']
        self.access_token = access
        exp_in = data['expires_in']
        exp = cur + datetime.timedelta(seconds=exp_in)
        self.access_token_exp = exp
        access_token_prev_exp = exp < cur
        return True
        
    
    def get_token_heading(self):
        self.client_id = self.client_id
        self.client_secret = self.client_secret
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        return {"Authorization": f"Basic {client_creds_b64.decode()}" }

    def get_token_data(self):   
        return {"grant_type": "client_credentials"}

    def get_access_token(self):
        self.auth_access_token()
        exp = self.access_token_exp
        cur = datetime.datetime.now()
        if(exp < cur or self.access_token == None):
            self.get_access_token()
        return self.access_token

    def get_bearer(self, query):
        
        endpoint_url = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint_url}?{query}"
        r = requests.get(lookup_url, headers = self.get_header())
        if(r.status_code not in range(200, 299)):
            return {}
        return r.json()
        
    def get_header(self):
        access_token = self.get_access_token()
        header = {
            "Authorization": f"Bearer {access_token}" 
        }
        return header

    def search(self, query, search_type):

        if(isinstance(query, dict)):
            query = ' '.join([f'{k}:{v}' for k,v in query.items()])

        data = urlencode({'q': query,'type': search_type.lower()})
        
        return self.get_bearer(data)

    def get_resource(self, _id, resource_type):
        endpoint_url = f'https://api.spotify.com/v1/{resource_type}/{_id}'
        r = requests.get(endpoint_url, headers = self.get_header())
        if(r.status_code not in range(200, 299)):
            return {}
        return r.json()
        

    def get_album(self, _id):  
        return self.get_resource(_id, 'albums')
    def get_artist(self, _id):
        return self.get_resource(_id, 'artists')
    def get_features(self, _id):
        return self.get_resource(_id, 'audio-features')
