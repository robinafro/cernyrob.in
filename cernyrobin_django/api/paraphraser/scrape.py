import requests
import json

# Define the URL
url = 'https://api.paraphrase.app/paraphrase-modes'

# Define headers with Content-Type
headers = {
    'authority': 'api.paraphrase.app',
    'method': 'POST',
    'path': '/paraphrase-modes',
    'scheme': 'https',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Authorization': 'Bearer f9a9cc1b-67ba-4920-ba47-05faa4646974',
    'Cache-Control': 'no-cache',
    'Content-Length': '1574',
    'Content-Type': 'application/json',
    'Expires': 'no-cache',
    'Origin': 'https://paraphrasetool.com',
    'Pragma': 'no-cache',
    'Referer': 'https://paraphrasetool.com/',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Gpc': '1',
    'Sectoken': 'a74714d4-d055-4830-b9c8-c80c6641cd8d',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def send_request(input_text):
    # Define the payload as a dictionary
    payload = {'lang': 'cs', 'mode': 'standard', 'text': input_text}

    # Convert payload to JSON format
    json_payload = json.dumps(payload)

    # Send the POST request with JSON payload and headers
    response = requests.post(url, data=json_payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print("POST request failed with status code:", response.status_code)
        return None
