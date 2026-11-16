"""
DirectR Core Schemas
Defines shared Pydantic data models connecting all 4 modules.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


# -------------------------------------------------------------------------
# Shared Base & Project Context
# -------------------------------------------------------------------------

class CharacterProfile(BaseModel):
    id: str
    name: str
    archetype: str
    psychology_constraints: List[str] = Field(
        default_factory=list,
        description="Non-negotiable psychological traits preserved across chapters"
    )
    dialect_rules: Dict[str, str] = Field(
        default_factory=dict,
        description="Speech patterns, slang, and dialect constraints"
    )
    backstory: str = ""


class ProjectBrief(BaseModel):
    project_id: str
    title: str
    genre: str
    logline: str
    characters: List[CharacterProfile] = Field(default_factory=list)
    target_duration_minutes: int = 5
    metadata: Dict[str, Any] = Field(default_factory=dict)


# -------------------------------------------------------------------------
# Module 1: Narrative & Screenplay Data Models
# -------------------------------------------------------------------------

class DialogueLine(BaseModel):
    speaker: str
    line: str
    emotion: str
    dialect_applied: bool = False
    delivery_note: Optional[str] = None


class FoleyCue(BaseModel):
    cue_name: str
    description: str
    trigger_beat_second: float


class SceneBeat(BaseModel):
    scene_number: int
    title: str
    location: str
    setting_time: str = "DAY"
    action_description: str
    visual_mood: str
    tension_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Emotional tension rating from 0.0 (calm) to 1.0 (climax)"
    )
    dialogue: List[DialogueLine] = Field(default_factory=list)
    foley_cues: List[FoleyCue] = Field(default_factory=list)


# -------------------------------------------------------------------------
# Module 2: Visual Art & Design Assist Data Models
# -------------------------------------------------------------------------

class VisualAsset(BaseModel):
    asset_id: str
    scene_number: int
    asset_type: str = Field(
        ...,
        description="Type: 'layered_svg', 'turnaround_sheet', or 'storyboard_frame'"
    )
    prompt: str
    svg_data: Optional[str] = None
    anchor_nodes_count: Optional[int] = None
    character_id: Optional[str] = None
    turnaround_angles: List[str] = Field(
        default_factory=lambda: ["front", "three_quarters", "side", "back"]
    )
    render_url: Optional[str] = None


# -------------------------------------------------------------------------
# Module 3: Music & Audio Studios Data Models
# -------------------------------------------------------------------------

class StemArrangement(BaseModel):
    scene_number: int
    tempo_bpm: int
    tension_matched: float
    active_stems: List[str] = Field(
        ...,
        description="Active musical layers e.g. ['drums', 'bass', 'lead_synth', 'strings']"
    )
    emotional_valence: str
    audio_stream_uri: Optional[str] = None


class FoleyAsset(BaseModel):
    cue_name: str
    synthesized_from_text: str
    duration_seconds: float
    audio_format: str = "wav"
    audio_uri: Optional[str] = None


# -------------------------------------------------------------------------
# Module 4: Content Strategy & Distribution Data Models
# -------------------------------------------------------------------------

class CreatorReel(BaseModel):
    reel_id: str
    source_scene_number: int
    hook_text: str
    start_second: float
    end_second: float
    tension_score: float
    vertical_aspect_ratio: str = "9:16"
    subtitles_burned: bool = True


class ThumbnailVariant(BaseModel):
    variant_id: str
    headline: str
    visual_focal_point: str
    attention_heatmap_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Predicted viewer gaze fixation score out of 100"
    )
    predicted_ctr: float = Field(..., description="Estimated click-through rate %")


class CommunityResponse(BaseModel):
    comment_id: str
    incoming_comment: str
    persona_voice: str
    generated_response: str
    sentiment: str


# -------------------------------------------------------------------------
# Core Swarm Production Package (The Integrated Output)
# -------------------------------------------------------------------------

class ProductionPackage(BaseModel):
    project_id: str
    brief: ProjectBrief
    scenes: List[SceneBeat]
    visual_assets: List[VisualAsset]
    stem_arrangements: List[StemArrangement]
    foley_assets: List[FoleyAsset]
    reels: List[CreatorReel]
    thumbnails: List[ThumbnailVariant]
    distribution_ready: bool = True
