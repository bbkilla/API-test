import json
import requests
from datetime import datetime, UTC, timedelta

API = "https://api.torn.com/torn/?key=6Jy84Y0h663nyzu3&comment=TornAPI&selections=shoplifting"
logs = "status_history.json"

with open(logs, "r") as f:
    history = json.load(f)
response = requests.get(API)
data = response.json()

new_time_str = datetime.now(UTC).isoformat()
old_time_str = history["old_time"]
new_time = datetime.fromisoformat(new_time_str)
old_time = datetime.fromisoformat(old_time_str)

def format_td(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m"
    elif minutes:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


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
            old_item["status"] = f"In {shop} the {old_item["title"]} is off."
            
        else:
            old_item["run_type"] = "wait for it..."
            min_cycle = eval(old_item["min_cycle"])
            max_cycle = eval(old_item["max_cycle"])
            h, m, s = map(int, old_item["this_run_time"].split(":"))
            current_time = timedelta(hours=h, minutes=m, seconds=s)
            if current_time < min_cycle:
                left_min = min_cycle - current_time
                left_max = max_cycle - current_time
                old_item["status"] = f"In {shop} the {old_item['title']} is active, will disable in {format_td(left_min)} - {format_td(left_max)}."
            elif min_cycle <= current_time < max_cycle:
                left_max = max_cycle - current_time
                old_item["status"] = f"In {shop} the {old_item['title']} is active, can be disable off any minute, max in {format_td(left_max)}."
            else:
                old_item["status"] = f"In {shop} the {old_item['title']} is active, but due to error, can't give estimated time."
        print(old_item['status'])


print(f"{old_time}")
history["old_time"] = new_time_str

with open(logs, "w") as f:
    json.dump(history, f, indent=4)
