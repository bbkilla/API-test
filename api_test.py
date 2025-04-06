import json
import requests
from datetime import datetime, UTC, timedelta

API = "https://api.torn.com/torn/?key=PHjfnNpLPwYwlM7l&comment=TornAPI&selections=shoplifting"
logs = "status_history.json"

with open(logs, "r") as f:
    history = json.load(f)
response = requests.get(API)
data = response.json()

new_time_str = datetime.now(UTC).isoformat()
old_time_str = history["old_time"]
new_time = datetime.fromisoformat(new_time_str)
old_time = datetime.fromisoformat(old_time_str)

for shop, old_items in history["shoplifting"].items():
    new_items = {item["title"]: item for item in data["shoplifting"].get(shop, [])}  

    for old_item in old_items:
        title = old_item["title"]
        
        new_item = new_items[title]  
            
        if old_item["disabled"] == new_item["disabled"]:
            old_item["CHANGE?"] = "No!!"
            if old_item["this_run_time"] == "00:00:00":
                time_dif = new_time - old_time
                total_seconds = int(time_dif.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                old_item["this_run_time"] = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                h, m, s = map(int, old_item["this_run_time"].split(":"))
                old_run_time = timedelta(hours=h, minutes=m, seconds=s)
                time_dif = new_time - old_time + old_run_time
                total_seconds = int(time_dif.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                old_item["this_run_time"] = f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            old_item["CHANGE?"] = "YES!!"
            old_item["old_run"] = old_item["this_run_time"]
            old_item["this_run_time"] = "00:00:00"
            old_item["disabled"] = new_item["disabled"]

        if new_item["disabled"] == True:
            old_item["run_type"] = "GO GO GO"
        else:
            old_item["run_type"] = "wait for it..."
        old_item["min_cycle"] = ""
        old_item["max_cycle"] = ""

print(f"{old_time}")
history["old_time"] = new_time_str

with open(logs, "w") as f:
    json.dump(history, f, indent=4)
