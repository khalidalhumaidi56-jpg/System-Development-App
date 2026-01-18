import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from google.cloud import datastore

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
ds_client = datastore.Client(project=PROJECT_ID)

def log_activity(user_email: str, action: str, item_title: str):
    # Kind name in Datastore (like a table name, but NoSQL)
    kind = "activity_logs"

    # Auto-ID key
    key = ds_client.key(kind)

    entity = datastore.Entity(key=key)
    entity.update({
        "user": user_email,
        "action": action,
        "item": item_title,
        "timestamp": datetime.now(timezone.utc),
    })

    ds_client.put(entity)
    print(f"✅ Activity logged to Datastore: {action} - {item_title}")