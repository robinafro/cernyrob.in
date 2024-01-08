import urllib.request
import urllib
import json

from api.yt_transcriptor import answer

def get_video_info(url):
    params = {"format": "json", "url": url}
    request_url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    request_url = request_url + "?" + query_string
    try:
        with urllib.request.urlopen(request_url) as response:
            response_text = response.read()
            data = response_text.decode()

            data = json.loads(data)

            data["description"] = answer.get_video_description(url)

            data = json.dumps(data)
            
            return data
    except Exception as e:
        print(e)
        return None