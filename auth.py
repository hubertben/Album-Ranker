import json
from SpotifyAPI import *
from track import *
import math

def form(JSON):
    json_formatted_str = json.dumps(JSON, indent=2)
    return json_formatted_str

def generate_question_list():
    with open('questions.json') as f:
        data = json.load(f)
    questions = []
    for d in data['questions']:
        questions.append((d['question'], d['attr']))
    return questions

def distribution(x, center):

    c1 = (x - center/3)
    c2 = (-1/2) * (c1 * c1)
    c3 = math.pow(math.e, c2)
    c4 = math.sqrt(2 * math.pi)
    return c3/c4

def confine(target, min, max, bound_min, bound_max):
    inc = (bound_max - bound_min) / (max - min)
    return bound_min + ((target - min) * inc)


album_name = input('Album Name : ')
artist = input('Artist Name (not required): ')



client_id = "9b9d033e087f4e96b3c8e2a7548ee7c3"
client_secret = "350fce8a98014d10a84929d62767236f"

client = SpotifyAPI(client_id, client_secret)
if(artist == ''):
    JSON = client.search({'album': album_name}, search_type='album')
else:
    JSON = client.search({'album': album_name, 'artist': artist}, search_type='album')


album_id = JSON['albums']['items'][0]['id']
tracks = client.get_album(album_id)

track_count = int(tracks['total_tracks'])

track_list = []


for i in range(track_count):
    print(f'{math.ceil((i/track_count)*100)}%')
    track = client.get_album(album_id)['tracks']['items'][i]
    features = client.get_features(track['id'])
    track_list.append(Track(track, features))

questions = generate_question_list()

for i in range(len(questions)):

    print(questions[i][0])
    responce = int(input('(1-10) : '))
    print(responce)
    new_track_list = sorted(track_list, key=lambda track: track.get_feature(questions[i][1]), reverse=True)
    for i,n in enumerate(new_track_list):  
        c = confine(i, 1, 10, 1, track_count)
        n.rating += distribution(c, responce)
    

new_track_list = sorted(track_list, key=lambda track: track.rating, reverse=True)

for i in range(track_count):
    print(new_track_list[i].rating, '\t\t', new_track_list[i].name)
