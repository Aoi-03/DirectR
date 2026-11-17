"""
Module 2: Inpainting Pipeline & Sketch-to-Production Assistant
Synthesizes localized inpainting masks, semantic brush guidance schedules,
and ControlNet conditioning profiles for iterative art edits.
"""

from typing import Dict, Tuple, Optional, Any, List
from ..schemas import InpaintingMaskSpec


class InpaintingPipeline:
    """
    Manages semantic sketch brush guidance, localized mask generation,
    and diffusion inpainting parameterization.
    """

    DENOISING_PRESETS: Dict[str, float] = {
        "subtle_touchup": 0.35,      # Preserves lineart and form, refines lighting/texture
        "feature_redesign": 0.68,    # Alters specific elements (e.g., weapon, clothing detail)
        "generative_inpaint": 0.85,  # Completely regenerates contents inside mask bounding box
        "background_replace": 0.95,  # Replaces entire background plate while preserving foreground
    }

    STUDIO_NEGATIVE_PROMPT: str = (
        "blurry, bad anatomy, deformed limbs, floating artifacts, out of frame, "
        "poorly drawn hands, missing fingers, extra digit, mutated, poorly drawn face, "
        "mutation, ugly, JPEG compression artifacts, pixelated vector"
    )

    @classmethod
    def create_inpainting_task(
        cls,
        task_id: str,
        target_layer_id: str,
        bounding_box: Tuple[int, int, int, int],
        semantic_label: str,
        mode: str = "feature_redesign",
        prompt_guidance: str = "",
        feather_radius: int = 8,
    ) -> InpaintingMaskSpec:
        """
        Creates a structured inpainting specification for localized edits.
        bounding_box: (x_min, y_min, x_max, y_max)
        """
        denoising = cls.DENOISING_PRESETS.get(mode, 0.68)

        guidance = prompt_guidance or f"Refined detailed {semantic_label.replace('_', ' ')} with studio lineart"

        return InpaintingMaskSpec(
            task_id=task_id,
            target_layer_id=target_layer_id,
            bounding_box=bounding_box,
            feather_radius_px=feather_radius,
            semantic_label=semantic_label,
            denoising_strength=denoising,
            prompt_guidance=guidance,
            negative_prompt=cls.STUDIO_NEGATIVE_PROMPT,
        )

    @classmethod
    def generate_mask_svg(
        cls,
        width: int,
        height: int,
        bounding_box: Tuple[int, int, int, int],
        feather_radius: int = 8,
    ) -> str:
        """
        Generates an SVG alpha mask representation for the localized inpainting region.
        Black (0,0,0) = preserved unmasked regions. White (255,255,255) = inpaint target.
        """
        x_min, y_min, x_max, y_max = bounding_box
        box_w = max(1, x_max - x_min)
        box_h = max(1, y_max - y_min)

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}">\n'
            f'  <defs>\n'
            f'    <filter id="featherMask">\n'
            f'      <feGaussianBlur stdDeviation="{feather_radius}" />\n'
            f'    </filter>\n'
            f'  </defs>\n'
            f'  <rect width="{width}" height="{height}" fill="#000000" />\n'
            f'  <rect x="{x_min}" y="{y_min}" width="{box_w}" height="{box_h}" '
            f'fill="#ffffff" rx="{feather_radius}" filter="url(#featherMask)" />\n'
            f'</svg>'
        )
