# To play, you must upgrade your lichess fork account to bot first!
import requests

# Enter here Lichess clone, were your bot is registered (e.g. https://lichess.org)
site = "https://lichess.org"

# Enter here your API token (generate one on https://your-clone.org/account/oauth/token)
# Note that if account played at least 1 game before upgrating, you will get an error from server!
api = "Bearer GrKdhWV5rrYAu0tX"

# Sending our request..
r = requests.post(site + "/api/bot/account/upgrade", headers = {"Authorization" : api})

# Printing result
print(r.status_code, r.text)
