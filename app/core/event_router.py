from typing import Dict, Callable, Type
import asyncio

from app.events.instance_event_handler import InstanceEventHandler

class EventRouter:
    """Route events to the correct async event handlers based on service type."""

    def __init__(self):
        self.event_handlers: Dict[str, Callable] = {
            'compute.instance': InstanceEventHandler(),
            # Later we can add:
            # 'volume.volume': VolumeEventHandler(),
            # 'network.port': NetworkEventHandler(),
        }

    async def route_event(self, service: str, event_type: str, payload: dict):
        handler = self.event_handlers.get(service)
        if handler:
            await handler.handle_event(event_type=event_type, payload=payload)
        else:
            # If no handler exists, just log and ignore
            print(f"No handler found for service: {service} (event_type: {event_type})")

