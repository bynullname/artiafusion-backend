import requests
import json

url = "https://api.midjourneyapi.io/v2/imagine"

payload = json.dumps({
  "prompt": "high texture quality portrait of a young woman with freckles and crystal blue eyes with wreath in her hair, 4k"
})
headers = {
  'Authorization': 'd06e3b29-bf2d-417e-a975-9aafdc6ea778',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)