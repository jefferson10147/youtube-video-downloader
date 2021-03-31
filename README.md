# Youtube downloader cli

This cli app allows you to download every single video you want from YouTube, It works with Pytube which is a python 3 library and YouTube API.

## How to run this cli (linux)

1- Clone this project, on your local machine:

```bash
$ git clone https://github.com/jefferson10147/youtube-video-downloader
```

2- Inside project root directory, you have to create a virtual enviroment if you don't want to install all dependencies in your machine

```bash
$ python3 -m venv your_env_name
```

3- Turn on your virtual enviroment 

```bash
$ source your_env_name/bin/activate
```

4- Finally you have to install dependencies

```bash
$ pip install -r requirements.txt
```

## How to use this cli

1- To download a video you can use the url, just passing -u or --url flag
```bash
$ python3 yt_downloader.py -u 'https://www.youtube.com/watch?v=8SbUC-UaAxE'
```

2- You can navigate through youtube, search results, and download a desired video, for this you need a developer key of the YouTube api, you can get it in Google api's. Once you have the key you just have to create a config.ini file with the following structure:

```
    [app]
    api_token = your_youtube_api_token
```

Now you are ready to use cli YouTube navigation just passing -q or --query flag following by the query you want to search
```bash
$ python3 yt_downloader.py -q 'python courses'
```

3- To see all commands you can type in your console
```bash
$ python3 yt_downloader.py --help
```

