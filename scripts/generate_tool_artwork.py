"""Generate the dependency-free CONFIGDOCTOR Tool Center SVG sprite.

The sprite is keyed by the canonical Flask endpoint so every real tool gets its
own line icon and framed illustration without 60 separate image requests.
Run from any directory with: python scripts/generate_tool_artwork.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from blueprints.tools_static import TOOL_CENTER_GROUPS

SOURCE_PATH = PROJECT_ROOT / "static" / "img" / "tool-artwork-sprite.svg"
PUBLIC_PATH = PROJECT_ROOT / "public" / "static" / "img" / "tool-artwork-sprite.svg"

# Purpose-drawn FPV line art. All marks inherit the category accent through
# currentColor, while the shared scene frame supplies a restrained flight-deck grid.
ICON_MARKS = {
    "tools_analysis.index": '<circle cx="10" cy="11" r="4"/><circle cx="38" cy="11" r="4"/><circle cx="10" cy="37" r="4"/><circle cx="38" cy="37" r="4"/><path d="m14 14 7 6m13-6-7 6m-13 8 7-6m13 6-7-6M21 18h6v12h-6z"/><path d="M23 21h2m-2 4h2"/>',
    "tools_static.blackbox_page": '<path d="M6 8h36v31H6z"/><path d="M10 33h28M11 29l5-7 5 4 5-11 5 8 6-5"/><circle cx="16" cy="22" r="1.4"/><circle cx="26" cy="15" r="1.4"/>',
    "tools_static.cli_surgeon_page": '<rect x="5" y="7" width="38" height="33" rx="4"/><path d="M5 14h38M11 22l5 4-5 4m10 0h8"/><path d="m32 22 7 7-8 8-7-7zM30 37l-3 4"/>',
    "tools_static.cli_comparator": '<rect x="5" y="7" width="16" height="33" rx="2"/><rect x="27" y="7" width="16" height="33" rx="2"/><path d="M9 14h8m-8 5h6m-6 5h8m-8 5h5m15-15h8m-8 5h5m-5 5h8m-8 5h5"/><path d="M22 18h4m-4 12h4"/>',
    "tools_static.loop_analyzer": '<circle cx="24" cy="24" r="16" stroke-dasharray="4 3"/><path d="M32 11h8v8M40 15a17 17 0 0 0-29 2m-3 16v-8h8m-8 4a17 17 0 0 0 29 1"/><circle cx="24" cy="24" r="4"/><path d="M24 8v4m16 12h-4M24 40v-4M8 24h4"/>',
    "content_pages.military_uas": '<path d="m24 5 4 13 15 6v4l-15-2-3 13-3-1 1-12-13 4v-4l13-8-2-12z"/><path d="M8 11a22 22 0 0 1 32 0M12 15a16 16 0 0 1 24 0"/><circle cx="24" cy="24" r="2"/>',
    "tools_advisor.pid_advisor": '<path d="M6 12h36M6 24h36M6 36h36"/><circle cx="16" cy="12" r="4"/><circle cx="31" cy="24" r="4"/><circle cx="21" cy="36" r="4"/><path d="M8 7v10m32-10v10M8 19v10m32-10v10M8 31v10m32-10v10"/>',
    "tools_advisor.quick_tune": '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="3"/><path d="M24 7v5m17 12h-5M24 41v-5M7 24h5m12 0 8-9M17 30l-5 5m17 0 5 5"/><path d="m29 31 3 3 7-8"/>',
    "tools_rpm.rpm_filter": '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="4"/><path d="M24 20c-3-6-3-11 1-14 5 5 6 9 2 15m-3 7c-7 2-11 1-13-3 5-4 9-4 15 0m-2-2c4 6 5 10 2 14-5-4-6-8-3-15m-1-2c6-4 10-5 14-2-4 5-8 6-15 3"/>',
    "tools_static.rates_visualizer": '<path d="M7 7v34h35M11 34c8-2 8-17 15-17 4 0 5 10 9 10 3 0 4-4 7-10"/><path d="M12 36c8-1 11-5 14-10m0 0 2 6m-2-6 6 1"/><circle cx="26" cy="17" r="2"/><circle cx="35" cy="27" r="2"/>',
    "tools_static.bf_wizard": '<path d="M8 10h32v28H8z"/><circle cx="15" cy="18" r="3"/><circle cx="24" cy="25" r="3"/><circle cx="33" cy="32" r="3"/><path d="M18 20l4 3m4 3 4 3M13 31l-2 2m21-18 3-3"/>',
    "tools_static.tuning_log": '<path d="M11 6h22l7 7v29H11z"/><path d="M33 6v8h7M16 20h18M16 25h8m-8 11 5-6 4 3 5-9 4 5"/><circle cx="25" cy="33" r="1.4"/>',
    "tools_static.build_card": '<rect x="6" y="7" width="36" height="34" rx="5"/><path d="M12 13h14m-14 5h8"/><circle cx="33" cy="23" r="5"/><path d="M28 23h-3m13 0h-3m-2-5v-3m0 16v-3m-5-9-2-2m14 14-2-2m0-10 2-2m-14 14 2-2M12 31h23m-23 5h15"/>',
    "tools_static.osd_page": '<rect x="5" y="7" width="38" height="34" rx="5"/><path d="M24 9v7m0 16v7M7 24h7m18 0h9M16 16l4 4m8 8 4 4m0-16-4 4m-8 8-4 4"/><circle cx="24" cy="24" r="5"/><path d="M10 12h4m20 0h4M10 36h4m20 0h4"/>',
    "tools_analysis.motor_prop": '<circle cx="24" cy="25" r="7"/><path d="M21 18c-4-6-4-10-1-13 5 3 7 7 5 13m4 9c7 1 10 3 11 7-5 3-10 2-15-2m-6-2c-2 7-5 10-9 10-2-6 0-10 6-15m4 0c-7-2-10-5-10-9 6-2 10 0 14 6"/><path d="M24 32v8m-6 3h12"/>',
    "tools_static.esc_checker": '<rect x="10" y="8" width="28" height="32" rx="5"/><path d="M15 8V4m6 4V4m6 4V4m6 4V4M15 40v4m6-4v4m6-4v4m6-4v4"/><rect x="15" y="14" width="7" height="7" rx="1"/><rect x="26" y="14" width="7" height="7" rx="1"/><path d="M16 29h16m-16 5h11m5-6 2 2 4-5"/>',
    "tools_static.battery_health": '<rect x="8" y="13" width="32" height="24" rx="4"/><path d="M40 20h3v10h-3M13 18h6v14h-6m10-12h5v12h-5m9-12h4v12h-4"/><path d="M16 9c4-4 12-4 16 0m-16 32c4 4 12 4 16 0"/>',
    "tools_static.motor_thermal": '<rect x="18" y="7" width="12" height="27" rx="6"/><circle cx="24" cy="36" r="7"/><path d="M24 18v18m8-25h5m-5 8h5m-5 8h4M8 14c3 2 3 5 0 7m0 6c3 2 3 5 0 7m32-20c-3 2-3 5 0 7m0 6c-3 2-3 5 0 7"/>',
    "tools_vtx.vtx": '<path d="M24 9v30m-5 0h10m-7-30c-1-5 5-5 4 0"/><path d="M16 16a12 12 0 0 0 0 16m16-16a12 12 0 0 1 0 16M10 10a21 21 0 0 0 0 28m28-28a21 21 0 0 1 0 28"/><circle cx="24" cy="9" r="2"/>',
    "tools_vtx.vtx_range": '<circle cx="11" cy="30" r="4"/><circle cx="37" cy="18" r="4"/><path d="M15 29c6-9 12-12 18-11M11 19a11 11 0 0 1 10-10m-10 3v-4m-4 4h4M37 30a11 11 0 0 1-10 10m10-3v4m4-4h-4"/><path d="M18 34h10m-8 4h6"/>',
    "tools_vtx.vtx_smartaudio": '<path d="M24 7v28m-5 5h10m-5-33c-1-5 5-5 4 0"/><path d="M9 20h4l3-6 5 19 5-13 4 9 3-9 3 0"/><circle cx="24" cy="8" r="2"/>',
    "tools_gear.fpv_gear": '<path d="M6 18a7 7 0 0 1 7-7h22a7 7 0 0 1 7 7v12a7 7 0 0 1-7 7h-6l-5-5-5 5h-6a7 7 0 0 1-7-7z"/><path d="M13 23h8m-4-4v8m15-5h.01m4 4h.01M18 13l3-5h6l3 5"/><circle cx="32" cy="23" r="3"/>',
    "tools_static.fpv_trainer": '<path d="M7 18a6 6 0 0 1 6-6h22a6 6 0 0 1 6 6v12a6 6 0 0 1-6 6h-5l-6-5-6 5h-5a6 6 0 0 1-6-6z"/><path d="M14 22h9m-4-4v8m12-6h.01m4 4h.01"/><path d="M24 4v5m-7-2 3 4m11-4-3 4"/>',
    "tools_static.flight_quiz": '<circle cx="24" cy="10" r="4"/><circle cx="10" cy="36" r="4"/><circle cx="24" cy="36" r="4"/><circle cx="38" cy="36" r="4"/><path d="M22 14 12 32m14-18 10 18M24 14v18"/><path d="m8 36 2-2 2 2m10 0 2-2 2 2m10 0 2-2 2 2"/>',
    "tools_static.leaderboard": '<path d="M7 39h34M10 39V25h9v14m5 0V14h9v25m5 0V7h9v32"/><path d="m29 5 1.5 3.5L34 10l-3.5 1.5L29 15l-1.5-3.5L24 10l3.5-1.5z"/><circle cx="14.5" cy="20" r="3"/>',
    "tools_static.fpv_hub": '<path d="M6 12c7-2 13 0 18 4v23c-5-4-11-6-18-4zm36 0c-7-2-13 0-18 4v23c5-4 11-6 18-4z"/><path d="M12 18h7m-7 5h7m10-5h7m-7 5h7"/><circle cx="24" cy="10" r="3"/><path d="M24 13v3"/>',
    "downloads.downloads_index": '<path d="M12 5h18l8 8v30H12z"/><path d="M30 5v9h8M17 21h13m-13 5h16m-16 5h10"/><path d="M24 24v12m-5-5 5 5 5-5"/>',
    "content_pages.about": '<path d="M24 4 41 11v12c0 10-7 17-17 21C14 40 7 33 7 23V11z"/><circle cx="24" cy="22" r="8"/><path d="M24 20v6m0-10h.01"/><path d="M19 13h10"/>',
    "content_pages.team": '<circle cx="24" cy="15" r="6"/><circle cx="10" cy="20" r="4"/><circle cx="38" cy="20" r="4"/><path d="M12 39v-4a12 12 0 0 1 24 0v4zm-9 0v-3a7 7 0 0 1 9-7m33 10v-3a7 7 0 0 0-9-7"/><path d="M17 28h14"/>',
    "content_pages.changelog": '<path d="M12 6v36m0-31h8l4 4h12m-24 9h12l4 4h8m-24 9h8l4 4h12"/><circle cx="12" cy="6" r="3"/><circle cx="12" cy="19" r="3"/><circle cx="12" cy="32" r="3"/><path d="M36 14v4m-4-2h4m-1 12 3 3m0-3-3 3"/>',
}

CATEGORY_SCENES = {
    "analyze": '<g fill="none" stroke="currentColor" stroke-width=".85" opacity=".31"><circle cx="56" cy="74" r="28" stroke-dasharray="2 4"/><circle cx="56" cy="74" r="19"/><path d="M18 74h20m36 0h15M56 36v16m0 44v16M252 47h40m-28 9h18m-30 56h40"/></g>',
    "tune": '<g fill="none" stroke="currentColor" stroke-width=".9" opacity=".32"><path d="M18 101c16 0 16-36 32-36s16 36 32 36 16-36 32-36m104 0h44m-34 8h28m-40 37h42"/><circle cx="50" cy="65" r="3"/><circle cx="82" cy="101" r="3"/></g>',
    "build": '<g fill="none" stroke="currentColor" stroke-width=".85" opacity=".31"><path d="M18 46h34v14H18zm0 42h26v14H18zm234-42h40v14h-40zm6 42h34v14h-34z"/><path d="M52 53h18v21m-26 21h28V74h32m116-21h20v21m-14 21h26V74h-32"/></g>',
    "learn": '<g fill="none" stroke="currentColor" stroke-width=".9" opacity=".32"><path d="M25 45c20 0 20 28 39 28s19 29 39 29m192-57c-20 0-20 28-39 28s-19 29-39 29" stroke-dasharray="2 4"/><circle cx="25" cy="45" r="3"/><circle cx="103" cy="102" r="3"/><circle cx="295" cy="45" r="3"/><circle cx="217" cy="102" r="3"/></g>',
}


def _art_id(endpoint: str) -> str:
    return endpoint.replace(".", "-")


def build_sprite() -> str:
    tools = [
        (group["id"], tool)
        for group in TOOL_CENTER_GROUPS
        for tool in group["tools"]
    ]
    endpoints = [tool["endpoint"] for _, tool in tools]
    if len(endpoints) != len(set(endpoints)):
        raise ValueError("Tool Center endpoints must be unique before artwork generation")

    missing = sorted(set(endpoints) - set(ICON_MARKS))
    extra = sorted(set(ICON_MARKS) - set(endpoints))
    if missing or extra:
        raise ValueError(f"Artwork/catalog mismatch: missing={missing}; unknown={extra}")

    chunks = [
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">',
        '<defs><linearGradient id="tool-scene-wash" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#122b2a"/><stop offset="1" stop-color="#071416"/></linearGradient></defs>',
    ]
    for category, tool in tools:
        endpoint = tool["endpoint"]
        ident = _art_id(endpoint)
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", ident):
            raise ValueError(f"Unsafe SVG symbol id for {endpoint!r}")
        mark = ICON_MARKS[endpoint]
        chunks.append(
            f'<symbol id="icon-{ident}" viewBox="0 0 48 48">'
            f'<g fill="none" stroke="currentColor" stroke-width="2.15" '
            f'stroke-linecap="round" stroke-linejoin="round">{mark}</g></symbol>'
        )
        chunks.append(
            f'<symbol id="art-{ident}" viewBox="0 0 320 148">'
            '<rect width="320" height="148" rx="16" fill="url(#tool-scene-wash)"/>'
            '<g fill="none" stroke="#d4f2e8" stroke-width=".55" opacity=".12">'
            '<path d="M0 29h320M0 118h320M30 0v148M290 0v148"/>'
            '<path d="M0 55h320M0 92h320" stroke-dasharray="1 7"/>'
            '</g>'
            f'{CATEGORY_SCENES[category]}'
            '<g transform="translate(126 40) scale(1.36)" color="currentColor">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{mark}</g></g>'
            '<path d="M126 128h68" fill="none" stroke="currentColor" stroke-width="1.2" opacity=".7"/>'
            '<circle cx="160" cy="128" r="2.2" fill="currentColor" opacity=".88"/>'
            '</symbol>'
        )
    chunks.append("</svg>")
    return "\n".join(chunks) + "\n"


def main() -> None:
    sprite = build_sprite()
    for path in (SOURCE_PATH, PUBLIC_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(sprite, encoding="utf-8")
    print(f"Generated {len(ICON_MARKS)} icons and {len(ICON_MARKS)} framed illustrations.")
    print(f"Source: {SOURCE_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Mirror: {PUBLIC_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
