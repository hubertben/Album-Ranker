
class Track:

    def __init__(self, data, features):
        self.data = data
        self.features = features
        self.parse_data()

        self.confined_value = 0
        

        self.feature_list = []
        self.parse_features()

        self.rating = 0

    def parse_data(self):
        self._id = self.data['id']
        self.name = self.data['name']
        self.track_number = self.data['track_number']
        self.artists = [self.data['artists'][i]['name'] for i in range(len(self.data['artists']))]

    def parse_features(self):

        self.feature_list.append(('dance',self.features['danceability']))
        self.feature_list.append(('energy',self.features['energy']))
        self.feature_list.append(('key',self.features['key']))
        self.feature_list.append(('loud',self.features['loudness']))
        self.feature_list.append(('mode',self.features['mode']))
        self.feature_list.append(('instrument',self.features['instrumentalness']))
        self.feature_list.append(('speech',self.features['speechiness']))
        self.feature_list.append(('acoustic',self.features['acousticness']))
        self.feature_list.append(('liveness',self.features['liveness']))
        self.feature_list.append(('valance',self.features['valence']))
        self.feature_list.append(('tempo',self.features['tempo']))

    def get_feature(self, feature):
        for i in self.feature_list:
            if(i[0] == feature):
                return i[1]
        return 'Feature Not Found'
        



