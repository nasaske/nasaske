#!/usr/bin/env python3
"""Generate the animated Nasaske stack panel from Simple Icons via Shields.io."""

from __future__ import annotations

import base64
import html
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "nasaske-stack.svg"

STACK = [
    ("AI AGENTS", "AI_Agents", "huggingface"),
    ("MULTI-AGENT", "Multi--Agent", "langchain"),
    ("MCP", "MCP", "modelcontextprotocol"),
    ("API ENGINEERING", "API_Engineering", "openapiinitiative"),
    ("AUTOMATION", "Automation", "n8n"),
    ("RPA", "RPA", "robotframework"),
    ("TYPESCRIPT", "TypeScript", "typescript"),
    ("JAVASCRIPT", "JavaScript", "javascript"),
    ("NODE.JS", "Node.js", "nodedotjs"),
    ("APPS SCRIPT", "Apps_Script", "googleappsscript"),
    ("NESTJS", "NestJS", "nestjs"),
    ("REACT", "React", "react"),
    ("NEXT.JS", "Next.js", "nextdotjs"),
    ("POSTGRESQL", "PostgreSQL", "postgresql"),
    ("SUPABASE", "Supabase", "supabase"),
    ("GOOGLE CLOUD", "Google_Cloud", "googlecloud"),
    ("DOCKER", "Docker", "docker"),
    ("OBSIDIAN", "Obsidian", "obsidian"),
]


def fetch_icon_paths(badge: str, logo: str) -> list[str]:
    encoded_badge = urllib.parse.quote(badge, safe="._-")
    url = (
        f"https://img.shields.io/badge/{encoded_badge}-18181B"
        f"?style=flat-square&logo={logo}&logoColor=C7B37A"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "nasaske-profile-generator"})
    with urllib.request.urlopen(request, timeout=20) as response:
        badge_svg = response.read().decode("utf-8")

    match = re.search(r'href="data:image/svg\+xml;base64,([^"]+)"', badge_svg)
    if not match:
        raise RuntimeError(f"Shields.io did not return an icon for {logo}")

    icon_svg = base64.b64decode(match.group(1)).decode("utf-8")
    root = ET.fromstring(icon_svg)
    paths = [
        element.attrib["d"]
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "path" and "d" in element.attrib
    ]
    if not paths:
        raise RuntimeError(f"No SVG path found for {logo}")
    return paths


def render_tile(index: int, label: str, paths: list[str]) -> str:
    column = index % 6
    row = index // 6
    x = 48 + column * 186
    y = 32 + row * 84
    duration = 3.8 + (index % 5) * 0.43
    delay = -(index % 7) * 0.37
    icon_paths = "".join(
        f'<path d="{html.escape(path, quote=True)}"/>' for path in paths
    )

    return f"""
    <g transform="translate({x} {y})">
      <rect width="174" height="72" rx="12" fill="#0c0c0d" fill-opacity=".9"
            stroke="#c7b37a" stroke-opacity=".14">
        <animate attributeName="stroke-opacity" values=".12;.3;.12"
                 dur="{duration + 2:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>
      </rect>
      <circle cx="34" cy="36" r="21" fill="#c7b37a" fill-opacity=".025"
              stroke="#c7b37a" stroke-opacity=".16">
        <animate attributeName="r" values="20;22;20"
                 dur="{duration:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>
        <animate attributeName="stroke-opacity" values=".12;.42;.12"
                 dur="{duration:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>
      </circle>
      <g transform="translate(22 24)" fill="#d7c28b" filter="url(#goldGlow)">
        <g>
          {icon_paths}
          <animateTransform attributeName="transform" type="translate"
                            values="0 1;0 -1;0 1" dur="{duration:.2f}s"
                            begin="{delay:.2f}s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values=".72;1;.72"
                   dur="{duration:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>
        </g>
      </g>
      <text x="66" y="40" class="label">{html.escape(label)}</text>
      <circle cx="154" cy="17" r="1.8" fill="#d7c28b">
        <animate attributeName="opacity" values=".12;.9;.12"
                 dur="{duration + 1.2:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>
      </circle>
    </g>"""


def main() -> None:
    tiles = [
        render_tile(index, label, fetch_icon_paths(badge, logo))
        for index, (label, badge, logo) in enumerate(STACK)
    ]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="304"
     viewBox="0 0 1200 304" role="img" aria-labelledby="title description">
  <title id="title">Nasaske animated engineering stack</title>
  <desc id="description">Eighteen animated technology icons for AI agents, automation, software engineering, and cloud systems.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#030303"/>
      <stop offset=".55" stop-color="#080808"/>
      <stop offset="1" stop-color="#100e0b"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#d7c28b" stop-opacity="0"/>
      <stop offset=".5" stop-color="#d7c28b" stop-opacity=".08"/>
      <stop offset="1" stop-color="#d7c28b" stop-opacity="0"/>
    </linearGradient>
    <pattern id="microGrid" width="18" height="18" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".7" fill="#f2eee4" opacity=".055"/>
    </pattern>
    <filter id="goldGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="1.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      text {{
        font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      .label {{
        fill: #bdb4a1;
        font-size: 11px;
        font-weight: 650;
        letter-spacing: .75px;
      }}
    </style>
  </defs>
  <rect width="1200" height="304" rx="18" fill="url(#background)"/>
  <rect width="1200" height="304" rx="18" fill="url(#microGrid)"/>
  <rect x="-260" width="180" height="304" fill="url(#scan)">
    <animate attributeName="x" values="-260;1280" dur="9s" repeatCount="indefinite"/>
  </rect>
{"".join(tiles).lstrip()}
</svg>
"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"generated {OUTPUT}")


if __name__ == "__main__":
    main()
