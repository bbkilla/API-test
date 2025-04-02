import json
import requests
from datetime import datetime

API = "https://api.torn.com/torn/?key=PHjfnNpLPwYwlM7l&comment=TornAPI&selections=shoplifting"
Data = "status_history.json"

response = requests.get(API)
time = datetime.utcnow().isoformat()
data = response.json()
with open(Data, "w") as f:
    json.dump(data, f, indent=4)
with open(Data, "a") as f:
    json.dump(timestamp, f, indent=4)

print(data)
print(timestamp)
