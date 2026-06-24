#app/routes/registrations.py
from app.utils.event_helpers import sync_event_status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
from app.database.dependencies import get_db
from app.database.models import User, Event, Registration
from app.schemas.registration import RegistrationCreate
from app.schemas.cancel_registration import CancelRegistration
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/register")
def register_for_event(
    registration: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        event = (
            db.query(Event)
            .filter(Event.id == registration.event_id)
            .with_for_update()
            .first()
        )

        event = sync_event_status(event, db)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )
        
        if not event.registration_open:
            raise HTTPException(
            status_code=400,
            detail="Registrations are closed"
        )

        if event.status != "ACTIVE":
            raise HTTPException(
            status_code=400,
            detail="Event not active"
        )

        if event.event_date < datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail="Event already completed"
            )

        existing = db.query(Registration).filter(
            Registration.user_id == current_user.id,
            Registration.event_id == registration.event_id,
            Registration.status.in_(["CONFIRMED", "WAITLISTED"])
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Already registered"
            )
        
        cancelled_registration= (db.query(Registration).filter(
            Registration.user_id == current_user.id,
            Registration.event_id == registration.event_id,
            Registration.status == "CANCELLED"
        )
        .with_for_update()
        .first()
        )


        confirmed_count = db.query(Registration).filter(
            Registration.event_id == registration.event_id,
            Registration.status == "CONFIRMED"
        ).count()

        if confirmed_count < event.capacity:
            status = "CONFIRMED"
        else:
            status = "WAITLISTED"


        if cancelled_registration:
            cancelled_registration.status = status
            cancelled_registration.created_at = datetime.utcnow()
            db.commit()
            db.refresh(cancelled_registration)
            return cancelled_registration

        new_registration = Registration(
            user_id=current_user.id,
            event_id=registration.event_id,
            status=status
        )

        db.add(new_registration)

        db.commit()

        db.refresh(new_registration)

        return new_registration

    except Exception:
        db.rollback()
        raise

@router.post("/cancel-registration")
def cancel_registration(
    request: CancelRegistration,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):  
    try:
        registration = (
            db.query(Registration)
        .filter(
            Registration.id == request.registration_id
        )
        .with_for_update()
        .first()
        )

        if not registration:
            raise HTTPException(
                status_code=404,
                detail="Registration not found"
            )
        
        if registration.user_id != current_user.id:
            raise HTTPException(
            status_code=403,
            detail="You cannot cancel another user's registration"
        )

        if registration.status == "CANCELLED":
            raise HTTPException(
                status_code=400,
                detail="Registration already cancelled"
            )
        
        old_status = registration.status

        waitlisted=None
        
        registration.status = "CANCELLED"


        if old_status == "CONFIRMED":
            waitlisted = db.query(Registration).filter(
                Registration.event_id == registration.event_id,
                Registration.status == "WAITLISTED"
            ).order_by(
                Registration.created_at
            ).with_for_update().first()

            if waitlisted:
                waitlisted.status = "CONFIRMED"

        db.commit()
        if waitlisted:
            return{
                "message": "Registration cancelled",
                "promoted_registration_id": waitlisted.id
            }
        
        return{
            "message": "Registration cancelled"
        }

    except Exception:
        db.rollback()
        raise


@router.get("/events/{event_id}/registrations")
def get_event_registrations(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    event=db.query(Event).filter(
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
            detail="You cannot view registrations for events you did not create"
        )

    return db.query(Registration).filter(
        Registration.event_id == event_id
    ).all()

@router.get("/my-registrations")
def get_my_registrations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Registration).filter(
        Registration.user_id == current_user.id
    ).all()