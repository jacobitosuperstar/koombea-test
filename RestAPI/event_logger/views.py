from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException

from ..settings import settings
from .producer import rabbit_mq_sender, rabbit_mq_checker
from .models import (
    NewEvent,
    Event,
    UpdateEvent,
    DatabaseEvents,
)


router: APIRouter = APIRouter(
    prefix="/events",
    tags=["events"],
)

# initializing the database
db: DatabaseEvents = DatabaseEvents()


@router.get("/")
def get_events() -> List[Event]:
    """List all the Events.
    """
    return db.all()


@router.post("/")
def create_event(new_event: NewEvent) -> Event:
    """Event creator.
    """
    event: Event = db.add(new_event)
    if not rabbit_mq_checker():
        print("There was an error connecting with the message broker.")
        return event
    rabbit_mq_sender(
        event,
        settings.rabbit_mq_host,
        settings.rabbit_mq_port,
        "test",
        "test",
        "test",
    )
    return event


@router.get("/{event_id}")
def get_event(event_id: UUID) -> Optional[Event]:
    """Returns the information from a singular event.
    """
    event: Optional[Event] = db.get_by("event_id", event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}")
def update_event(event_id: UUID, info_for_update: UpdateEvent) -> Optional[Event]:
    """Event updater.
    """
    event: Optional[Event] = db.update_event(event_id, info_for_update)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
