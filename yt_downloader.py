import requests
from bs4 import BeautifulSoup


def set_connection(search_query):
    url = f'https://www.youtube.com/results?search_query={search_query}'
    
    try:
        response = requests.get(url)
    except:
        exit(0)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content,'html.parser')
        # print(soup.prettify())
        # yt-simple-endpoint style-scope ytd-video-renderer
        return soup
    else:
        print('Can not stablish connection with YouTube')
        exit(0)



def main():
    set_connection(search_query='react')


if __name__ == '__main__':
    main()