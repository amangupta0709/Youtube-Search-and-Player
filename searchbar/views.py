import requests
from isodate import parse_duration
from datetime import datetime

from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

search_url = 'https://www.googleapis.com/youtube/v3/search'
video_url = 'https://www.googleapis.com/youtube/v3/videos'

def videodata(request):

    required_data = []

    if request.method == "POST":
        if request.POST['searchbar'] == '':
            messages.error(request, 'Please type something.')
        else:
            search_parameters = {
                'key': settings.YOUTUBE_API_KEY,
                'part': 'snippet',
                'q':request.POST['searchbar'],
                'type':'video',
                'videoEmbeddable': True,
                'maxResults':12,
            }

            fetched_data = requests.get(search_url, params=search_parameters).json()['items']
            
            video_id_list = []
            for data in fetched_data:
                video_id_list.append(data['id']['videoId'])
            
            video_parameters = {
                'key': settings.YOUTUBE_API_KEY,
                'part':'snippet,contentDetails,statistics',
                'id': ','.join(video_id_list),
            }

            video_data = requests.get(video_url, params=video_parameters).json()['items']

            for i in range(search_parameters['maxResults']):
                views = formatted_views(video_data[i]['statistics']['viewCount'])
                try:
                    thumbnail = video_data[i]['snippet']['thumbnails']['standard']['url']
                except KeyError:
                    thumbnail = video_data[i]['snippet']['thumbnails']['high']['url']
                videos = {
                    'id': video_id_list[i],
                    'title': video_data[i]['snippet']['title'],
                    'description': video_data[i]['snippet']['description'],
                    'thumbnail': thumbnail,
                    'duration': str(int(parse_duration(video_data[i]['contentDetails']['duration']).total_seconds()//60))+' mins',
                    'views': views + ' views',
                }
                required_data.append(videos)

    return render(request, 'index.html', { 'videos':required_data })

def formatted_views(views):
    views = int(views)
    index = 0
    while views>1000:
        index +=1
        views /= 1000

    if int(views)>=10:
        views = int(views)
        return '%s%s' %(views, ['','K','M','B'][index])
    else:
        return '%.1f%s' % (views, ['','K','M','B'][index])

def player(request, videoid):
    video_parameters = {
        'key': settings.YOUTUBE_API_KEY,
        'part':'snippet,contentDetails,statistics',
        'id': videoid,
    }
    video_data = requests.get(video_url, params=video_parameters).json()['items'][0]
    date = str(video_data['snippet']['publishedAt']).split('T')[0]
    date = datetime.fromisoformat(date)
    month = date.strftime('%b')
    videos = {
        'id':videoid,
        'title': video_data['snippet']['title'],
        'date': f'Uploaded on {month} {date.day}, {date.year}',
        'views': video_data['statistics']['viewCount'] + ' views',
    }

    return render(request, 'videoplayer.html', {'videos':videos})
        