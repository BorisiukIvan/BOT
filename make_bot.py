import requests

api = "Bearer GrKdhWV5rrYAu0tX"
r = requests.post("https://lidraughts.org/api/bot/account/upgrade", headers = {"Authorization" : api})
print(r.status_code, r.text)