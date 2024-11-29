from typing import List, Union, Optional, Dict
from typing_extensions import TypedDict, NotRequired

from threading import Lock, RLock
import uuid

LockType = Union[Lock, RLock]

# Structs for the different Event types
class NewEvent(TypedDict):
    """struct of the Event before is saved in the database.
    """
    user_id: str
    description: str

class UpdateEvent(TypedDict):
    """stuct of the Event when is going to be updated
    """
    user_id: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[str]

class Event(NewEvent):
    """struct of the event that is going to be stored within the database class
    """
    event_id: uuid.UUID
    status: str


# Functions to modify the Type between Events
def event_creator(entry: NewEvent) -> Event:
    """creates and event given the NewEvent.
    """
    event: Event = {"event_id": uuid.uuid1(), "status": "NotProcessed", **entry}
    return event

def event_updater(entry: UpdateEvent, event: Event) -> Event:
    """Given the information in the UpdateEvent, the main Event is updated.
    """
    for key, value in entry.items():
        event[key] = value
    return event


# Simple thread safe databse
class DatabaseEvents:
    def __init__(self) -> None:
        """Simple thread safe storage system for events.
        """
        self.storage: List[Event] = []
        self.lock: LockType = Lock()

    def add(self, entry_data: NewEvent) -> Event:
        """Event adder to the storage.
        """
        with self.lock:
            data : Event = event_creator(entry_data)
            self.storage.append(data)
        return data

    def all(self) -> List[Event]:
        """Returns all the events from the storage.
        """
        with self.lock:
            return self.storage

    def filter_by(self, key: str, value: Union[str, uuid.UUID]) -> List[Event]:
        """filter_by returns a filtrated list of events by the key, value pair
        from the storage.
        """
        if key not in Event.__annotations__.keys():
            raise ValueError("Invalid key")
        with self.lock:
            filtered_list: List[Event] = [event for event in self.storage if event[key] == value]
        return filtered_list

    def get_by(self, key: str, value: Union[str, uuid.UUID]) -> Optional[Event]:
        """get_by returns the first matching element of a key value pair from
        the storage or None.
        """
        if key not in Event.__annotations__.keys():
            raise ValueError("Invalid key")
        event: Optional[Event] = None
        with self.lock:
            for e in self.storage:
                if e[key] == value:
                    event = e
                    break
        return event

    def update_event(self, event_id: uuid.UUID, update_info: UpdateEvent) -> Optional[Event]:
        """Given the UUID of the event and the new information, the first match
        of the UUID within the DatabaseEvents.storage is updated with the new
        information.
        """
        index: Optional[int] = None
        event_to_update: Optional[Event] = None
        with self.lock:
            for i, event in enumerate(self.storage):
                if event["event_id"] == event_id:
                    index, event_to_update = i, event
                    break
            if index is not None and event_to_update is not None:
                updated_event: Event = event_updater(update_info, event_to_update)
                self.storage[index] = updated_event
                return updated_event
        return None

    def clear_by(self, key: str, value: str) -> None:
        """clear_by deletes all the matching events with the pair key, value
        from the storage.
        """
        if key not in Event.__annotations__.keys():
            raise ValueError("Invalid key")
        with self.lock:
            self.storage: List[Event] = [event for event in self.storage if event[key] != value]

    def clear(self) -> None:
        """Deletes all the elements from the storage.
        """
        with self.lock:
            self.storage.clear()
