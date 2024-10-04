from rasa.core.tracker_store import TrackerStore
from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.events import Event, UserUttered, BotUttered
from typing import Optional, Text, Dict, Any, List
import asyncio
from pymongo import MongoClient

class CustomTrackerStore(TrackerStore):
    def __init__(self, domain: Domain, host: Text, db: Text, username: Text, password: Text, auth_source: Text, event_broker: Optional[Any] = None, **kwargs: Any) -> None:
        super().__init__(domain, event_broker, **kwargs)
        self.client = MongoClient(host, username=username, password=password, authSource=auth_source)
        self.db = self.client[db]
        self.user_collection = self.db['user_events']
        self.bot_collection = self.db['bot_events']

    async def save(self, tracker: DialogueStateTracker) -> None:
        user_events = []
        bot_events = []
        for event in tracker.events:
            if isinstance(event, UserUttered):
                formatted_event = {
                    "event": "user",
                    "timestamp": event.timestamp,
                    "text": event.text,
                    "message_id": event.message_id,
                    "parse_data": event.parse_data,
                    "data": None
                }
                user_events.append(formatted_event)
            elif isinstance(event, BotUttered):
                formatted_event = {
                    "event": "bot",
                    "timestamp": event.timestamp,
                    "text": event.text,
                    "data": event.data,
                    "message_id": None,
                    "parse_data": None
                }
                bot_events.append(formatted_event)
        
        if user_events:
            self.user_collection.update_one(
                {"sender_id": tracker.sender_id},
                {"$set": {"events": user_events}},
                upsert=True
            )
        
        if bot_events:
            self.bot_collection.update_one(
                {"sender_id": tracker.sender_id},
                {"$set": {"events": bot_events}},
                upsert=True
            )

    async def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        user_result = self.user_collection.find_one({"sender_id": sender_id})
        bot_result = self.bot_collection.find_one({"sender_id": sender_id})
        
        user_events = user_result.get("events", []) if user_result else []
        bot_events = bot_result.get("events", []) if bot_result else []
        
        events = user_events + bot_events
        deserialized_events = [self._deserialize_event(event) for event in events]
        return self._create_tracker(sender_id, deserialized_events)

    async def keys(self) -> List[Text]:
        user_keys = [doc["sender_id"] for doc in self.user_collection.find({}, {"sender_id": 1})]
        bot_keys = [doc["sender_id"] for doc in self.bot_collection.find({}, {"sender_id": 1})]
        return list(set(user_keys + bot_keys))

    def _create_tracker(self, sender_id: Text, events: List[Event]) -> DialogueStateTracker:
        tracker = self.init_tracker(sender_id)
        for event in events:
            tracker.update(event)
        return tracker

    def _deserialize_event(self, event: Dict[Text, Any]) -> Event:
        event_type = event.get("event")
        if event_type == "user":
            return UserUttered(
                text=event.get("text"),
                parse_data=event.get("parse_data"),
                timestamp=event.get("timestamp"),
                input_channel=None,
                message_id=event.get("message_id"),
            )
        elif event_type == "bot":
            return BotUttered(
                text=event.get("text"),
                data=event.get("data"),
                timestamp=event.get("timestamp"),
            )
        else:
            # Handle other event types if necessary
            return Event.from_parameters(event)