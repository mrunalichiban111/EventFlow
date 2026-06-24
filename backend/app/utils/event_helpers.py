# app/utils/event_helpers.py

from datetime import datetime, UTC

def sync_event_status(event, db):

    if (
        event.status == "ACTIVE"
        and event.event_date < datetime.utcnow()
    ):
        event.status = "COMPLETED"
        event.registration_open = False

        db.commit()
        db.refresh(event)

    return event