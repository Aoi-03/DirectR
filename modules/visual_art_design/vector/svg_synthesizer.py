"""
Module 2: SVG Synthesizer
Generates layered, parametric vector SVGs preserving controllable Bezier anchor nodes.
"""

from typing import List, Dict, Tuple, Optional, Any
import math
from ..schemas import (
    ColorPalette,
    AnchorNode,
    SVGLayer,
    LayeredSVGDocument,
)
from .palette_generator import PaletteGenerator


class SVGSynthesizer:
    """
    Parametric SVG synthesis engine creating multi-layered vector compositions
    with metadata-tagged Bezier anchor nodes for interactive manipulation.
    """

    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height

    def synthesize_scene_svg(
        self,
        scene_number: int,
        prompt: str,
        visual_mood: str = "Moody Cinematic",
        setting_time: str = "NIGHT",
        tension_score: float = 0.5,
        layers: Optional[List[str]] = None,
    ) -> LayeredSVGDocument:
        """
        Synthesizes a complete layered SVG document with parametric vector paths,
        gradients, filters, and controllable anchor nodes.
        """
        palette = PaletteGenerator.get_palette_for_scene(
            visual_mood=visual_mood,
            setting_time=setting_time,
            tension_score=tension_score,
        )

        layer_names = layers or [
            "background_plate",
            "midground_structures",
            "foreground_characters",
            "lighting_overlays",
            "vfx_particles",
        ]

        svg_layers: List[SVGLayer] = []
        total_nodes = 0

        for idx, layer_name in enumerate(layer_names):
            layer = self._build_layer(
                layer_index=idx,
                layer_name=layer_name,
                palette=palette,
                tension=tension_score,
                scene_num=scene_number,
            )
            svg_layers.append(layer)
            total_nodes += len(layer.anchor_nodes)

        defs_markup = self._generate_defs(palette, scene_number)
        layers_markup = "\n".join(layer.raw_svg_markup for layer in svg_layers)

        full_svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.width} {self.height}" '
            f'width="{self.width}" height="{self.height}" '
            f'data-scene="{scene_number}" data-tension="{tension_score:.2f}">\n'
            f'{defs_markup}\n'
            f'{layers_markup}\n'
            f'</svg>'
        )

        return LayeredSVGDocument(
            scene_number=scene_number,
            viewbox=f"0 0 {self.width} {self.height}",
            width=self.width,
            height=self.height,
            palette=palette,
            layers=svg_layers,
            total_anchor_nodes=total_nodes,
            svg_source=full_svg,
        )

    def _generate_defs(self, palette: ColorPalette, scene_num: int) -> str:
        """Generates reusable SVG gradients and glow filters."""
        return (
            f'  <defs>\n'
            f'    <linearGradient id="bgGrad_{scene_num}" x1="0%" y1="0%" x2="0%" y2="100%">\n'
            f'      <stop offset="0%" stop-color="{palette.background}" />\n'
            f'      <stop offset="100%" stop-color="{palette.primary}" />\n'
            f'    </linearGradient>\n'
            f'    <linearGradient id="accentGrad_{scene_num}" x1="0%" y1="0%" x2="100%" y2="0%">\n'
            f'      <stop offset="0%" stop-color="{palette.secondary}" />\n'
            f'      <stop offset="100%" stop-color="{palette.accent}" />\n'
            f'    </linearGradient>\n'
            f'    <filter id="neonGlow_{scene_num}" x="-50%" y="-50%" width="200%" height="200%">\n'
            f'      <feGaussianBlur stdDeviation="8" result="blur1" />\n'
            f'      <feGaussianBlur stdDeviation="16" result="blur2" />\n'
            f'      <feMerge>\n'
            f'        <feMergeNode in="blur2" />\n'
            f'        <feMergeNode in="blur1" />\n'
            f'        <feMergeNode in="SourceGraphic" />\n'
            f'      </feMerge>\n'
            f'    </filter>\n'
            f'  </defs>'
        )

    def _build_layer(
        self,
        layer_index: int,
        layer_name: str,
        palette: ColorPalette,
        tension: float,
        scene_num: int,
    ) -> SVGLayer:
        """Constructs individual SVG layer with parametric Bezier paths and anchor nodes."""
        w, h = self.width, self.height
        anchor_nodes: List[AnchorNode] = []
        path_elements = []

        if "background" in layer_name.lower():
            layer_type = "background"
            # Horizon backdrop path
            pts = [
                (0.0, 0.0),
                (float(w), 0.0),
                (float(w), float(h)),
                (0.0, float(h)),
            ]
            for i, (x, y) in enumerate(pts):
                anchor_nodes.append(
                    AnchorNode(
                        node_id=f"node_bg_{i}",
                        point_type="corner",
                        x=x,
                        y=y,
                        controllable=False,
                    )
                )
            path_elements.append(
                f'    <rect width="{w}" height="{h}" fill="url(#bgGrad_{scene_num})" />'
            )

        elif "midground" in layer_name.lower() or "structure" in layer_name.lower():
            layer_type = "midground"
            # Skyline / architectural silhouette with parametric curve
            base_y = h * 0.55
            ctrl_y = base_y - (tension * 150)
            p0 = (0.0, float(h))
            p1 = (0.0, base_y)
            p2 = (w * 0.35, ctrl_y)
            p3 = (w * 0.65, base_y - 80)
            p4 = (float(w), base_y)
            p5 = (float(w), float(h))

            nodes_spec = [
                ("node_mg_0", p0[0], p0[1], None, None),
                ("node_mg_1", p1[0], p1[1], None, (w * 0.1, ctrl_y)),
                ("node_mg_2", p2[0], p2[1], (w * 0.25, ctrl_y), (w * 0.45, ctrl_y)),
                ("node_mg_3", p3[0], p3[1], (w * 0.55, base_y - 80), (w * 0.75, base_y - 80)),
                ("node_mg_4", p4[0], p4[1], (w * 0.85, base_y), None),
                ("node_mg_5", p5[0], p5[1], None, None),
            ]
            for nid, x, y, hin, hout in nodes_spec:
                anchor_nodes.append(
                    AnchorNode(
                        node_id=nid,
                        point_type="smooth" if (hin or hout) else "corner",
                        x=x,
                        y=y,
                        handle_in=hin,
                        handle_out=hout,
                        controllable=True,
                    )
                )

            d = (
                f"M {p0[0]} {p0[1]} L {p1[0]} {p1[1]} "
                f"C {p2[0]-100} {ctrl_y}, {p2[0]} {ctrl_y}, {p2[0]} {ctrl_y} "
                f"S {p3[0]} {p3[1]}, {p4[0]} {p4[1]} L {p5[0]} {p5[1]} Z"
            )
            path_elements.append(
                f'    <path d="{d}" fill="{palette.primary}" stroke="{palette.shadow}" stroke-width="3" />'
            )

        elif "foreground" in layer_name.lower() or "character" in layer_name.lower():
            layer_type = "foreground"
            # Focal character silhouette / hero element
            cx = w * 0.45
            cy = h * 0.68
            char_nodes = [
                ("node_fg_head", cx, cy - 140, (cx - 30, cy - 140), (cx + 30, cy - 140)),
                ("node_fg_shoulder_r", cx + 70, cy - 90, (cx + 40, cy - 110), (cx + 80, cy - 70)),
                ("node_fg_torso_r", cx + 55, cy + 80, (cx + 60, cy), (cx + 50, cy + 120)),
                ("node_fg_base", cx, cy + 160, (cx + 40, cy + 160), (cx - 40, cy + 160)),
                ("node_fg_torso_l", cx - 55, cy + 80, (cx - 50, cy + 120), (cx - 60, cy)),
                ("node_fg_shoulder_l", cx - 70, cy - 90, (cx - 80, cy - 70), (cx - 40, cy - 110)),
            ]
            for nid, x, y, hin, hout in char_nodes:
                anchor_nodes.append(
                    AnchorNode(
                        node_id=nid,
                        point_type="smooth",
                        x=x,
                        y=y,
                        handle_in=hin,
                        handle_out=hout,
                        controllable=True,
                    )
                )

            d_char = (
                f"M {cx} {cy-140} "
                f"C {cx+40} {cy-110}, {cx+70} {cy-90}, {cx+70} {cy-90} "
                f"C {cx+80} {cy-70}, {cx+60} {cy}, {cx+55} {cy+80} "
                f"C {cx+50} {cy+120}, {cx+40} {cy+160}, {cx} {cy+160} "
                f"C {cx-40} {cy+160}, {cx-50} {cy+120}, {cx-55} {cy+80} "
                f"C {cx-60} {cy}, {cx-80} {cy-70}, {cx-70} {cy-90} "
                f"C {cx-40} {cy-110}, {cx-30} {cy-140}, {cx} {cy-140} Z"
            )
            path_elements.append(
                f'    <path d="{d_char}" fill="{palette.shadow}" stroke="{palette.secondary}" stroke-width="4" />'
            )

        elif "lighting" in layer_name.lower():
            layer_type = "lighting"
            # Volumetric neon lighting cone / beam
            lx = w * 0.45
            ly = h * 0.25
            light_nodes = [
                ("node_light_source", lx, ly, None, None),
                ("node_light_spread_r", lx + 450, float(h), None, None),
                ("node_light_spread_l", lx - 450, float(h), None, None),
            ]
            for nid, x, y, hin, hout in light_nodes:
                anchor_nodes.append(
                    AnchorNode(
                        node_id=nid,
                        point_type="corner",
                        x=x,
                        y=y,
                        handle_in=hin,
                        handle_out=hout,
                        controllable=True,
                    )
                )

            d_light = f"M {lx} {ly} L {lx+450} {h} L {lx-450} {h} Z"
            path_elements.append(
                f'    <path d="{d_light}" fill="{palette.secondary}" opacity="0.18" '
                f'filter="url(#neonGlow_{scene_num})" />'
            )
            # Accent neon rim
            path_elements.append(
                f'    <line x1="{lx-150}" y1="{ly+80}" x2="{lx+150}" y2="{ly+80}" '
                f'stroke="{palette.accent}" stroke-width="6" filter="url(#neonGlow_{scene_num})" />'
            )

        else:  # vfx / particles
            layer_type = "vfx"
            # High tension spark or rain lines
            for i in range(4):
                px = (w * 0.25) + (i * 220)
                py = h * 0.4 + (i * 30)
                anchor_nodes.append(
                    AnchorNode(
                        node_id=f"node_vfx_{i}",
                        point_type="corner",
                        x=px,
                        y=py,
                        controllable=True,
                    )
                )
                path_elements.append(
                    f'    <circle cx="{px}" cy="{py}" r="{4 + i*2}" fill="{palette.highlight}" '
                    f'filter="url(#neonGlow_{scene_num})" />'
                )

        # Build group element with data attributes
        raw_markup = (
            f'  <g id="layer_{layer_name}" data-layer-type="{layer_type}" data-anchor-group="{layer_index}">\n'
            + "\n".join(path_elements)
            + "\n  </g>"
        )

        return SVGLayer(
            layer_id=f"layer_{layer_name}",
            layer_name=layer_name,
            layer_type=layer_type,
            opacity=1.0,
            blend_mode="screen" if layer_type in ("lighting", "vfx") else "normal",
            paths_count=len(path_elements),
            anchor_nodes=anchor_nodes,
            raw_svg_markup=raw_markup,
        )
