import os
import time
import threading
import requests
import configparser
import argparse
from pytube import YouTube
from prettytable import PrettyTable

logo = '''
                    ,     ,
                    |\---/|
                   /  , , |
              __.-'|  / \ /
     __ ___.-'        ._O|
  .-'  '        :      _/
 / ,    .        .     |
:  ;    :        :   _/
|  |   .'     __:   /
|  :   /'----'| \  |
\  |\  |      | /| |
 '.'| /       || \ |
 | /|.'       '.l \\_
 || ||             '-'
 '-''-'
YouTube downloader
'''


def cli():
    parser = argparse.ArgumentParser(
        description='This app downloads every single video you want on YouTube'
    )
    parser.add_argument(
        '-q',
        '--query',
        type=str,
        default=None,
        help='Topic name that you want to search'
    )
    parser.add_argument(
        '-u',
        '--url',
        type=str,
        default=None,
        help='url of the video you want to download'
    )

    return parser.parse_args()


def set_connection(search_query):
    API_TOKEN = get_api_token()
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


def get_api_token():
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    API_TOKEN = parser['app']['api_token']

    return API_TOKEN


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
        selections.append(url)
        i += 1

    print('Press 0 to cancel.')
    user_option = int(input("Which video do you like to download? (number): "))

    if not user_option:
        exit(0)

    download_video(selections[user_option - 1])


def download_video(url):
    video = YouTube(url)
    stream = video.streams.first()
    title = video.title
    video_size = int(stream.filesize)
    thread = threading.Thread(target=progress_bar, args=(title, video_size))
    thread.start()
    stream.download('./downloads/')


def progress_bar(video_name, video_size):
    route = f'./downloads/{video_name}.mp4'
    percentage = 0.1
    partition_sizes = list()
    total_partitions = 10
    partitions_recovered = 1
    video_size_mb = round(video_size / 1000000, 2)

    for i in range(1, total_partitions):
        partition_sizes.append(round(video_size * percentage, 1))
        percentage = round(percentage + 0.1, 1)

    while True:
        time.sleep(0.1)
        try:
            current_size = os.stat(route).st_size
        except FileNotFoundError:
            continue

        if current_size >= video_size:
            break

        try:
            if current_size >= partition_sizes[0]:
                partition_sizes.pop(0)
                partitions_left = total_partitions - partitions_recovered
                current_size_mb = round(current_size / 1000000, 2)
                download_left = f'{current_size_mb} / {video_size_mb} mb'
                print('[', '##'*partitions_recovered, '**' *
                      partitions_left, ']', download_left, end='\r')
                partitions_recovered += 1
        except IndexError:
            break


def main():
    print(logo)
    args = cli()

    if args.url:
        download_video(args.url)

    if args.query:
        json_response = set_connection(args.query)
        urls = get_videos_urls(json_response)
        show_info_to_user(urls)


if __name__ == '__main__':
    main()
