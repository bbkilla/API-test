import json
import requests
from datetime import datetime

API = "https://api.torn.com/torn/?key=PHjfnNpLPwYwlM7l&comment=TornAPI&selections=shoplifting"
DATA_FILE = "status_history.json"
response = requests.get(API)
data = response.json()
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)
print(data)
timestamp = datetime.utcnow().isoformat()
print(timestamp)
with open(DATA_FILE, "a") as f:
    json.dump(timestamp, f, indent=4)
