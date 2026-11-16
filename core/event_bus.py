"""
DirectR Core Event Bus
Provides lightweight pub/sub event communication for multi-agent coordination.
"""

from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger("DirectR.EventBus")


class EventBus:
    """
    Central event distributor enabling decoupled agent communication.
    Any module can subscribe to events or publish events.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        """Subscribe a callback handler to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed handler to '{event_type}'")

    def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event to all registered listeners."""
        handlers = self._subscribers.get(event_type, [])
        logger.info(f"Publishing '{event_type}' to {len(handlers)} subscribers")
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error handling event '{event_type}': {e}", exc_info=True)

    def clear(self):
        """Clear all event subscriptions."""
        self._subscribers.clear()
