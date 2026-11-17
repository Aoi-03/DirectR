"""
Module 2: Visual Art & Design Assist - Internal Schemas
Provides detailed data models for parametric vector SVGs,
character turnaround topology, inpainting masks, and storyboard framing.
"""

from typing import List, Dict, Optional, Tuple, Any
from pydantic import BaseModel, Field


class ColorPalette(BaseModel):
    palette_name: str
    mood: str
    background: str
    primary: str
    secondary: str
    accent: str
    highlight: str
    shadow: str
    glow: Optional[str] = None


class AnchorNode(BaseModel):
    node_id: str
    point_type: str = "corner"  # "corner", "smooth", "symmetric"
    x: float
    y: float
    handle_in: Optional[Tuple[float, float]] = None
    handle_out: Optional[Tuple[float, float]] = None
    controllable: bool = True


class SVGLayer(BaseModel):
    layer_id: str
    layer_name: str
    layer_type: str  # "background", "midground", "foreground", "lighting", "vfx"
    opacity: float = 1.0
    blend_mode: str = "normal"
    paths_count: int = 1
    anchor_nodes: List[AnchorNode] = Field(default_factory=list)
    raw_svg_markup: str


class LayeredSVGDocument(BaseModel):
    scene_number: int
    viewbox: str = "0 0 1920 1080"
    width: int = 1920
    height: int = 1080
    palette: ColorPalette
    layers: List[SVGLayer]
    total_anchor_nodes: int
    svg_source: str


class JointLandmark(BaseModel):
    name: str
    x: float
    y: float
    z: float = 0.0
    confidence: float = 1.0


class SkeletalTopology(BaseModel):
    rig_type: str = "humanoid_bipedal"
    stance: str = "A-Pose"
    head_ratio: float = 7.5
    joints: List[JointLandmark]


class TurnaroundAngleSpec(BaseModel):
    angle_name: str  # "front", "three_quarters_front", "profile", "three_quarters_back", "back"
    degrees: int
    orthographic: bool = True
    focal_features: List[str]
    prompt_modifier: str


class CharacterTurnaroundSpec(BaseModel):
    character_id: str
    character_name: str
    archetype: str
    stance: str = "A-Pose"
    angles: List[TurnaroundAngleSpec]
    skeletal_rig: SkeletalTopology
    controlnet_openpose_config: Dict[str, Any]
    ip_adapter_consistency_prompt: str


class InpaintingMaskSpec(BaseModel):
    task_id: str
    target_layer_id: str
    bounding_box: Tuple[int, int, int, int]  # x_min, y_min, x_max, y_max
    feather_radius_px: int = 8
    semantic_label: str
    denoising_strength: float = Field(
        ..., ge=0.0, le=1.0, description="Denoising strength for diffusion model"
    )
    prompt_guidance: str
    negative_prompt: str


class StoryboardShot(BaseModel):
    scene_number: int
    shot_index: int
    shot_type: str  # "extreme_wide", "wide", "medium", "close_up", "extreme_close_up", "dutch_tilt"
    camera_movement: str  # "static", "pan_left", "tracking_forward", "dutch_roll"
    focal_length_mm: int
    depth_of_field: str
    lighting_scheme: str
    tension_level: float
    aspect_ratio_16_9_bounds: Tuple[int, int, int, int]
    vertical_9_16_safe_bounds: Tuple[int, int, int, int]
    prompt: str
