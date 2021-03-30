import requests
import pytube
from prettytable import PrettyTable
import json
import configparser
from bs4 import BeautifulSoup


parser = configparser.ConfigParser()
parser.read('config.ini')
API_TOKEN = parser['app']['api_token']


def set_connection(search_query):
    search_query = search_query.replace(' ', '%20')
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&key={API_TOKEN}&type=video&q={search_query}'

    try:
        response = requests.get(url)
    except:
        print('Something went wrong trying to connect with YouTube API')
        exit(0)

    if response.status_code == 200:
        return response.json()
    else:
        print('There is not YouTube API response')
        exit(0)


def get_videos_urls(json_response):
    videos_info = json_response['items']
    urls = {}

    for video_info in videos_info:
        video_key = video_info['id']['videoId']
        video_title = video_info['snippet']['title']
        video_title = video_title.replace('\u200b', ' ')
        channel_title = video_info['snippet']['channelTitle']
        urls[video_key] = [channel_title, video_title]

    return urls


def show_info_to_user(urls):
    base_url = 'https://www.youtube.com/watch?v='
    selections = []
    i = 1
    
    for key, value in urls.items():
        channel = f'{i}-{value[0]}'
        title = value[1]
        url = f'{base_url}{key}'
        table = PrettyTable()
        table.add_column(channel, [title, url])
        print(table, '\n')
        selections.append(selections)
        i += 1

    user_option = int(input("Which video do you like to download? (number):"))


def download_video(url):
    pass


def main():
    json_response = set_connection(
        search_query='auron reacciona cine argentino')
    urls = get_videos_urls(json_response)
    show_info_to_user(urls)
    # print(json.dumps(urls, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
