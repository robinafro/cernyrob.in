import urllib.request
import urllib
import json

import requests, re

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
            print(data["description"])
            # full_html = requests.get(url).text
            # y = re.search(r'shortDescription":"', full_html)
            # desc = ""
            # count = y.start() + 19  # adding the length of the 'shortDescription":"
            # while True:
            #     # get the letter at current index in text
            #     letter = full_html[count]

            #     if letter == "\"" and full_html[count - 1] != "\\":
            #         break
            #     else:
            #         desc += letter
            #         count += 1
            
            # data["description"] = desc

            data = json.dumps(data)
            
            return data
    except Exception as e:
        print(e)
        return None
    
# def get_video_info_new(url):
#     full_html = requests.get("YOUR YOUTUBE LINK HERE").text
#     y = re.search(r'shortDescription":"', full_html)
#     desc = ""
#     count = y.start() + 19  # adding the length of the 'shortDescription":"
#     while True:
#         # get the letter at current index in text
#         letter = full_html[count]
#         if letter == "\"":
#             if full_html[count - 1] == "\\":
#                 # this is case where the letter before is a backslash, meaning it is not real end of description
#                 desc += letter
#                 count += 1
#             else:
#                 break
#         else:
#             desc += letter
#             count += 1

#     print(f'description: {desc}')
#     return desc

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=e3KoPorzYtU"
    print(get_video_info(url))