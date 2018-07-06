import requests


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        defined_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url, headers=defined_headers)
        if response.status_code != 200:
            return None
        else:
            return response.content
