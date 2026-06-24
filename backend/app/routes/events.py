# app/routes/events.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.database.dependencies import get_db
from app.database.models import Event
from app.schemas.event import EventCreate
from app.auth.dependencies import get_current_user
from app.utils.event_helpers import sync_event_status

router = APIRouter()

@router.post("/events")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user.role != "ORGANIZER":
        raise HTTPException(
            status_code=403,
            detail="Only organizers can create events"
    )
    
    new_event = Event(
        title=event.title,
        description=event.description,
        capacity=event.capacity,
        event_date=event.event_date,
        creator_id=current_user.id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get("/events")
def get_events(
    db: Session = Depends(get_db)
):
    events= db.query(Event).all()

    for event in events:
        sync_event_status(event, db)
    
    db.commit()  

    return db.query(Event).filter(Event.status == "ACTIVE").all()

@router.get("/events/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    event = sync_event_status(event, db)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event

@router.get("/my-events")
def get_my_events(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "ORGANIZER":
        raise HTTPException(
            status_code=403,
            detail="Only organizers can view their events"
        )

    events=db.query(Event).filter(
        Event.creator_id == current_user.id
    ).all()

    for event in events:
        sync_event_status(event, db)
    
    return events

@router.post("/events/{event_id}/close-registration")
def close_event_registration(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    event = sync_event_status(event, db)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot close registration for events you did not create"
        )

    event.registration_open = False
    db.commit()
    db.refresh(event)

    return {
        "message": "Event registration closed",
        "event": event
    }

@router.post("/events/{event_id}/open-registration")
def open_event_registration(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    event = sync_event_status(event, db)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot open registration for events you did not create"
        )
    
    if event.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Only active events can accept registrations"
        )

    event.registration_open = True
    db.commit()
    db.refresh(event)

    return {
        "message": "Event registration opened",
        "event": event
    }

@router.post("/events/{event_id}/cancel")
def cancel_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    event = sync_event_status(event, db)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot cancel events you did not create"
        )

    event.status = "CANCELLED"
    event.registration_open = False
    db.commit()
    db.refresh(event)

    return {
        "message": "Event cancelled"
    }

@router.post("/events/{event_id}/complete")
def complete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    event = sync_event_status(event, db)

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot complete events you did not create"
        )

    event.status = "COMPLETED"
    event.registration_open = False
    db.commit()
    db.refresh(event)

    return {
        "message": "Event marked as completed"
    }
