from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from bson.objectid import ObjectId
from core.mongo_client import db
from notification.handlers import get_handler


notification_collection = db.notifications
notification_log_collection = db.notification_logs

@shared_task(bind=True, max_retries=3)
def send_notification_task(self, notification_id):
    try:
        notification = notification_collection.find_one({"_id": ObjectId(notification_id)})
    except Exception as e:
        pass

    if not notification:
        return

    for medium in notification.get("mediums", []):
        handler = get_handler(medium)
        if not handler:
            continue

        try:
            result = handler.send(notification)
            notification_log_collection.insert_one({
                "notification_id": notification["_id"],
                "medium": medium,
                "status": "success",
                "response": {"result": result}
            })
        except Exception as e:
            notification_log_collection.insert_one({
                "notification_id": notification["_id"],
                "medium": medium,
                "status": "failed",
                "response": {"error": str(e)}
            })
            continue

    notification_collection.update_one(
        {"_id": notification["_id"]},
        {"$set": {"status": "sent"}}
    )


@shared_task
def retry_failed_notifications():
    failed_notifications = notification_collection.find({
        "status": {"$in": ["failed", "retrying"]},
        "retry_count": {"$lt": 3},
        "updated_at": {"$lte": timezone.now() - timedelta(minutes=5)}
    })

    for notification in failed_notifications:
        notification_collection.update_one(
            {"_id": notification["_id"]},
            {
                "$set": {"status": "retrying"},
                "$inc": {"retry_count": 1}
            }
        )
        send_notification_task.delay(str(notification["_id"]))
