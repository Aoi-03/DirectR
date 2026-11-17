"""
Module 2: Rigging Engine & Character Turnaround Synthesizer
Generates 5-angle production turnaround model sheets, rig-ready skeletal
topology landmarks, and ControlNet / IP-Adapter conditioning profiles.
"""

from typing import List, Dict, Any, Optional
from core.schemas import CharacterProfile, VisualAsset
from ..schemas import (
    TurnaroundAngleSpec,
    CharacterTurnaroundSpec,
    SkeletalTopology,
    JointLandmark,
)


class CharacterTurnaroundEngine:
    """
    Synthesizes multi-angle orthographic model sheets with skeletal joint topology
    for 3D rigging and ControlNet pose conditioning.
    """

    STANDARD_ANGLES: List[TurnaroundAngleSpec] = [
        TurnaroundAngleSpec(
            angle_name="front",
            degrees=0,
            orthographic=True,
            focal_features=["facial expression", "chest armor / collar", "belt buckle", "knee caps"],
            prompt_modifier="full frontal orthographic view, direct eye-level, neutral lighting",
        ),
        TurnaroundAngleSpec(
            angle_name="three_quarters_front",
            degrees=45,
            orthographic=True,
            focal_features=["jawline contour", "shoulder pad volume", "depth silhouette", "cape drape"],
            prompt_modifier="three-quarters dynamic angle, 45 degree rotation, visible depth contours",
        ),
        TurnaroundAngleSpec(
            angle_name="profile",
            degrees=90,
            orthographic=True,
            focal_features=["nasal bridge", "ear placement", "spinal curvature", "heel-to-toe balance"],
            prompt_modifier="true 90-degree side profile silhouette, zero perspective distortion",
        ),
        TurnaroundAngleSpec(
            angle_name="three_quarters_back",
            degrees=135,
            orthographic=True,
            focal_features=["scapula line", "rear hair flow", "side holster", "calf definition"],
            prompt_modifier="three-quarters rear angle, 135 degree perspective, back silhouette details",
        ),
        TurnaroundAngleSpec(
            angle_name="back",
            degrees=180,
            orthographic=True,
            focal_features=["dorsal spine alignment", "backpack / power cell", "posterior belt gear"],
            prompt_modifier="direct rear orthographic view, 180 degrees, back armor and seam lines",
        ),
    ]

    @classmethod
    def generate_skeletal_topology(cls, stance: str = "A-Pose") -> SkeletalTopology:
        """
        Generates humanoid bipedal skeletal joint landmarks (normalized coordinates 0.0 - 1.0).
        Follows standard OpenPose 18-point format.
        """
        joints = [
            JointLandmark(name="nose", x=0.50, y=0.12, z=0.0),
            JointLandmark(name="neck", x=0.50, y=0.18, z=0.0),
            JointLandmark(name="right_shoulder", x=0.40, y=0.22, z=0.0),
            JointLandmark(name="right_elbow", x=0.34, y=0.34, z=0.0),
            JointLandmark(name="right_wrist", x=0.28, y=0.46, z=0.0),
            JointLandmark(name="left_shoulder", x=0.60, y=0.22, z=0.0),
            JointLandmark(name="left_elbow", x=0.66, y=0.34, z=0.0),
            JointLandmark(name="left_wrist", x=0.72, y=0.46, z=0.0),
            JointLandmark(name="spine_mid", x=0.50, y=0.36, z=0.0),
            JointLandmark(name="right_hip", x=0.44, y=0.50, z=0.0),
            JointLandmark(name="right_knee", x=0.42, y=0.70, z=0.0),
            JointLandmark(name="right_ankle", x=0.40, y=0.92, z=0.0),
            JointLandmark(name="left_hip", x=0.56, y=0.50, z=0.0),
            JointLandmark(name="left_knee", x=0.58, y=0.70, z=0.0),
            JointLandmark(name="left_ankle", x=0.60, y=0.92, z=0.0),
        ]
        return SkeletalTopology(
            rig_type="humanoid_bipedal",
            stance=stance,
            head_ratio=7.5,
            joints=joints,
        )

    @classmethod
    def build_turnaround_spec(
        cls, character: CharacterProfile, stance: str = "A-Pose"
    ) -> CharacterTurnaroundSpec:
        """
        Builds a comprehensive turnaround specification for diffusion conditioning.
        """
        skeletal_rig = cls.generate_skeletal_topology(stance=stance)

        # ControlNet OpenPose configuration
        controlnet_config = {
            "model": "control_v11p_sd15_openpose",
            "weight": 1.0,
            "guidance_start": 0.0,
            "guidance_end": 1.0,
            "body_parts_detected": len(skeletal_rig.joints),
            "render_resolution": 1024,
        }

        ip_adapter_prompt = (
            f"Consistency reference: {character.name}, archetype: {character.archetype}. "
            f"Preserve facial geometry, costume seams, silhouette silhouette volume across 360 degree rotation. "
            f"Character backstory cues: {character.backstory}."
        )

        return CharacterTurnaroundSpec(
            character_id=character.id,
            character_name=character.name,
            archetype=character.archetype,
            stance=stance,
            angles=cls.STANDARD_ANGLES,
            skeletal_rig=skeletal_rig,
            controlnet_openpose_config=controlnet_config,
            ip_adapter_consistency_prompt=ip_adapter_prompt,
        )

    @classmethod
    def generate_turnaround_asset(
        cls, character: CharacterProfile, stance: str = "A-Pose"
    ) -> VisualAsset:
        """
        Creates a core VisualAsset model populated with full turnaround metadata.
        """
        spec = cls.build_turnaround_spec(character, stance=stance)
        angles_list = [a.angle_name for a in spec.angles]

        prompt = (
            f"Production turnaround model sheet of {character.name}, {character.archetype}. "
            f"5-angle orthogonal orthographic view: {', '.join(angles_list)}. "
            f"Rig-ready topology, clean edge loops, {stance} neutral stance, flat studio lighting. "
            f"Joint landmarks: 15 skeletal points tracked."
        )

        return VisualAsset(
            asset_id=f"turnaround_{character.id}",
            scene_number=0,
            asset_type="turnaround_sheet",
            prompt=prompt,
            character_id=character.id,
            turnaround_angles=angles_list,
            render_url=f"https://directr.internal/assets/turnarounds/{character.id}.json",
        )
