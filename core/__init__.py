"""
DirectR Core Module
Contains shared schemas, event bus, and the central swarm orchestrator.
"""

from .schemas import (
    ProjectBrief,
    CharacterProfile,
    DialogueLine,
    SceneBeat,
    VisualAsset,
    StemArrangement,
    FoleyAsset,
    CreatorReel,
    ThumbnailVariant,
    CommunityResponse,
    ProductionPackage,
)
from .event_bus import EventBus
from .orchestrator import DirectROrchestrator

__all__ = [
    "ProjectBrief",
    "CharacterProfile",
    "DialogueLine",
    "SceneBeat",
    "VisualAsset",
    "StemArrangement",
    "FoleyAsset",
    "CreatorReel",
    "ThumbnailVariant",
    "CommunityResponse",
    "ProductionPackage",
    "EventBus",
    "DirectROrchestrator",
]
