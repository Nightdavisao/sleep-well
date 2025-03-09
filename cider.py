import requests

# https://github.com/ciderapp/Cider-2/blob/main/docs/Cider%202.5.0%20Preview%20API.md
class CiderAPI:
    def __init__(self, app_token):
        self.BASE_URL = 'http://localhost:10767/api/v1'
        self.APP_TOKEN = app_token
        self.headers = {
            "apptoken": self.APP_TOKEN
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def play(self):
        return self.session.post(self.BASE_URL + "/playback/play").json()
    
    def pause(self):
        return self.session.post(self.BASE_URL + "/playback/pause").json()
        
    def get_autoplay_state(self):
        result = self.session.get(self.BASE_URL + "/playback/autoplay").json()
        return result['value']
    
    def toggle_autoplay(self):
        return self.session.post(self.BASE_URL + "/playback/toggle-play").json()
    
    def get_volume(self):
        return self.session.get(self.BASE_URL + "/volume").json()
    
    def set_volume(self, volume):
        return self.session.post(self.BASE_URL + "/volume", json={
            "volume": volume
        }).json()
        
    def is_active(self):
        return self.session.get(self.BASE_URL + "/active").json()
    
    def is_playing(self):
        return self.session.get(self.BASE_URL + "/is-playing").json()
    
    def play_url(self, url):
        return self.session.post(self.BASE_URL + "/playback/play-url", json={
            "url": url
        }).json()