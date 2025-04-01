import os
import json
def load_history():
    if not os.path.exists(DATA_FILE):  # אם הקובץ לא קיים, יוצרים אותו עם תוכן ריק
        with open(DATA_FILE, "w") as f:
            json.dump({}, f, indent=4)  # כותבים מילון ריק כדי למנוע שגיאות
        return {}
