import requests
import json
import configparser
from bs4 import BeautifulSoup


parser = configparser.ConfigParser()
parser.read('config.ini')
API_TOKEN = parser['app']['api_token']


def set_connection(search_query):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&key={API_TOKEN}&type=video&q={search_query}'
    
    try:
        response = requests.get(url)
    except:
        exit(0)

    if response.status_code == 200:
        return response.json()
    else:
        print('Can not stablish connection with YouTube')
        exit(0)


def get_videos_urls(soup):
    pass


def main():
    json_response = set_connection(search_query='react')
    print(json.dumps(json_response, indent=4, sort_keys=True))
    #get_videos_urls(soup)
    pass

if __name__ == '__main__':
    main()