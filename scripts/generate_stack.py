#!/usr/bin/env python3
"""Generate the animated Nasaske specialties and technology panel."""

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

SPECIALTY_ROWS = [
    [
        "WORKFLOW AUTOMATION",
        "RPA",
        "AI AGENTS",
        "API INTEGRATIONS",
        "WEB SCRAPING",
        "FULL-STACK SYSTEMS",
    ],
    [
        "MODULAR MONOLITH",
        "CQRS",
        "CLEAN ARCHITECTURE",
        "EVENT-DRIVEN",
        "REST APIS",
        "WEBHOOKS",
    ],
]

SECTIONS = [
    (
        "AI + AUTOMATION",
        [
            ("AI AGENTS", "AI_Agents", "huggingface", "#FFD21E"),
            ("MULTI-AGENT", "Multi--Agent", "langchain", "#00A67E"),
            ("MCP", "MCP", "modelcontextprotocol", "#F2F2EE"),
            ("N8N", "n8n", "n8n", "#EA4B71"),
            ("RPA", "RPA", "robotframework", "#00C0B5"),
            ("API ENGINEERING", "API_Engineering", "openapiinitiative", "#6BA539"),
        ],
    ),
    (
        "LANGUAGES + RUNTIME",
        [
            ("TYPESCRIPT", "TypeScript", "typescript", "#3178C6"),
            ("JAVASCRIPT", "JavaScript", "javascript", "#F7DF1E"),
            ("NODE.JS", "Node.js", "nodedotjs", "#5FA04E"),
            ("APPS SCRIPT", "Apps_Script", "googleappsscript", "#4285F4"),
        ],
    ),
    (
        "FRONT-END + UI",
        [
            ("REACT", "React", "react", "#61DAFB"),
            ("NEXT.JS", "Next.js", "nextdotjs", "#F2F2EE"),
            ("VITE", "Vite", "vite", "#646CFF"),
            ("TAILWIND CSS", "Tailwind_CSS", "tailwindcss", "#06B6D4"),
            ("TANSTACK QUERY", "TanStack_Query", "reactquery", "#FF4154"),
            ("FRAMER MOTION", "Framer_Motion", "framer", "#0055FF"),
        ],
    ),
    (
        "BACK-END + FRAMEWORKS",
        [
            ("NESTJS", "NestJS", "nestjs", "#E0234E"),
            ("PRISMA", "Prisma", "prisma", "#5B7FFF"),
            ("ZOD", "Zod", "zod", "#3E67B1"),
            ("REDIS", "Redis", "redis", "#FF4438"),
        ],
    ),
    (
        "DATA + PLATFORM",
        [
            ("POSTGRESQL", "PostgreSQL", "postgresql", "#4169E1"),
            ("SUPABASE", "Supabase", "supabase", "#3FCF8E"),
            ("GOOGLE CLOUD", "Google_Cloud", "googlecloud", "#4285F4"),
            ("DOCKER", "Docker", "docker", "#2496ED"),
            ("GITHUB ACTIONS", "GitHub_Actions", "githubactions", "#2088FF"),
            ("OBSIDIAN", "Obsidian", "obsidian", "#A88BFA"),
        ],
    ),
]


def fetch_icon_paths(badge: str, logo: str) -> list[str]:
    encoded_badge = urllib.parse.quote(badge, safe="._-")
    url = (
        f"https://img.shields.io/badge/{encoded_badge}-11151E"
        f"?style=flat-square&logo={logo}&logoColor=FFFFFF"
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


def specialty_width(label: str) -> float:
    return max(54.0, len(label) * 7.35 + 30)


def badge_width(label: str) -> float:
    return max(102.0, len(label) * 7.45 + 58)


def render_specialties() -> str:
    elements: list[str] = []
    sequence = 0
    for row_index, labels in enumerate(SPECIALTY_ROWS):
        widths = [specialty_width(label) for label in labels]
        total_width = sum(widths) + 10 * (len(widths) - 1)
        x = (930 - total_width) / 2
        y = 77 + row_index * 42
        for label, width in zip(labels, widths):
            delay = -sequence * 0.45
            elements.append(
                f"""
    <g transform="translate({x:.1f} {y})">
      <rect width="{width:.1f}" height="32" rx="4" fill="#075960">
        <animate attributeName="fill-opacity" values=".78;1;.78"
                 dur="{5.0 + sequence * 0.16:.2f}s" begin="{delay:.2f}s"
                 repeatCount="indefinite"/>
      </rect>
      <rect width="3" height="32" rx="1.5" fill="#25D0C8"/>
      <text x="16" y="21" class="specialty">{html.escape(label)}</text>
    </g>"""
            )
            x += width + 10
            sequence += 1
    return "".join(elements)


def render_badge(
    index: int,
    x: float,
    y: float,
    label: str,
    color: str,
    paths: list[str],
) -> tuple[str, float]:
    width = badge_width(label)
    duration = 3.7 + (index % 6) * 0.41
    delay = -(index % 9) * 0.33
    icon_paths = "".join(
        f'<path d="{html.escape(path, quote=True)}"/>' for path in paths
    )

    markup = f"""
    <g transform="translate({x:.1f} {y:.1f})">
      <rect width="{width:.1f}" height="40" rx="7" fill="#11151e"
            stroke="{color}" stroke-opacity=".34">
        <animate attributeName="stroke-opacity" values=".24;.68;.24"
                 dur="{duration + 1.8:.2f}s" begin="{delay:.2f}s"
                 repeatCount="indefinite"/>
      </rect>
      <rect width="4" height="40" rx="2" fill="{color}"/>
      <circle cx="29" cy="20" r="15" fill="{color}" fill-opacity=".075">
        <animate attributeName="r" values="14;16;14"
                 dur="{duration:.2f}s" begin="{delay:.2f}s"
                 repeatCount="indefinite"/>
        <animate attributeName="fill-opacity" values=".04;.15;.04"
                 dur="{duration:.2f}s" begin="{delay:.2f}s"
                 repeatCount="indefinite"/>
      </circle>
      <g transform="translate(19 10) scale(.8333)" fill="{color}"
         filter="url(#colorGlow)">
        <g>
          {icon_paths}
          <animateTransform attributeName="transform" type="translate"
                            values="0 1.2;0 -1.2;0 1.2" dur="{duration:.2f}s"
                            begin="{delay:.2f}s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values=".76;1;.76"
                   dur="{duration:.2f}s" begin="{delay:.2f}s"
                   repeatCount="indefinite"/>
        </g>
      </g>
      <text x="52" y="25" class="badge-label">{html.escape(label)}</text>
      <circle cx="{width - 14:.1f}" cy="11" r="1.7" fill="{color}">
        <animate attributeName="opacity" values=".12;1;.12"
                 dur="{duration + 1.1:.2f}s" begin="{delay:.2f}s"
                 repeatCount="indefinite"/>
      </circle>
    </g>"""
    return markup, width


def render_sections() -> str:
    elements: list[str] = []
    badge_index = 0
    for section_index, (section_label, badges) in enumerate(SECTIONS):
        widths = [badge_width(label) for label, *_ in badges]
        total_width = sum(widths) + 10 * (len(widths) - 1)
        row_x = (930 - total_width) / 2
        label_y = 226 + section_index * 78
        badge_y = label_y + 14
        marker_color = badges[0][3]
        elements.append(
            f"""
    <g transform="translate({row_x:.1f} {label_y})">
      <circle cx="4" cy="4" r="4" fill="{marker_color}"/>
      <text x="17" y="8" class="category">{html.escape(section_label)}</text>
    </g>"""
        )

        x = row_x
        for (label, badge, logo, color), width in zip(badges, widths):
            paths = fetch_icon_paths(badge, logo)
            markup, _ = render_badge(
                badge_index, x, badge_y, label, color, paths
            )
            elements.append(markup)
            x += width + 10
            badge_index += 1
    return "".join(elements)


def main() -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="930" height="630"
     viewBox="0 0 930 630" role="img" aria-labelledby="title description">
  <title id="title">Nasaske animated specialties and technology stack</title>
  <desc id="description">Animated colored technology icons and specialty tags for AI, automation, software engineering, data, and cloud systems.</desc>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#07090e"/>
      <stop offset=".58" stop-color="#0a0d13"/>
      <stop offset="1" stop-color="#0d1118"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#25D0C8" stop-opacity="0"/>
      <stop offset=".48" stop-color="#25D0C8" stop-opacity=".055"/>
      <stop offset=".52" stop-color="#D946EF" stop-opacity=".06"/>
      <stop offset="1" stop-color="#D946EF" stop-opacity="0"/>
    </linearGradient>
    <pattern id="microGrid" width="18" height="18" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".7" fill="#F2F6FC" opacity=".045"/>
    </pattern>
    <filter id="colorGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="1.65" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <style>
      text {{
        font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      .section-title {{
        fill: #E6EDF3;
        font-size: 19px;
        font-weight: 720;
        letter-spacing: .15px;
      }}
      .specialty {{
        fill: #F4FFFF;
        font-size: 10.5px;
        font-weight: 760;
        letter-spacing: 1.1px;
      }}
      .category {{
        fill: #A8B3C2;
        font-size: 10.5px;
        font-weight: 720;
        letter-spacing: 1.35px;
      }}
      .badge-label {{
        fill: #E6EDF3;
        font-size: 11px;
        font-weight: 680;
        letter-spacing: .75px;
      }}
    </style>
  </defs>
  <rect width="930" height="630" rx="18" fill="url(#background)"/>
  <rect width="930" height="630" rx="18" fill="url(#microGrid)"/>
  <rect x="-280" width="190" height="630" fill="url(#scan)">
    <animate attributeName="x" values="-280;1020" dur="10s" repeatCount="indefinite"/>
  </rect>

  <g transform="translate(48 35)">
    <g fill="#D946EF" filter="url(#colorGlow)">
      <rect x="0" y="0" width="5" height="5"/>
      <rect x="8" y="0" width="5" height="5"/>
      <rect x="4" y="8" width="5" height="5"/>
    </g>
    <text x="24" y="13" class="section-title">SPECIALTIES</text>
  </g>
  <path d="M48 62H882" stroke="#8B949E" stroke-opacity=".32"/>
{render_specialties().lstrip()}

  <g transform="translate(48 176)">
    <path d="M1 11L8 4L15 11L8 18Z" fill="none" stroke="#25D0C8" stroke-width="1.8"/>
    <circle cx="8" cy="11" r="2.5" fill="#25D0C8"/>
    <text x="26" y="17" class="section-title">CORE STACK</text>
  </g>
  <path d="M48 203H882" stroke="#8B949E" stroke-opacity=".32"/>
{render_sections().lstrip()}
</svg>
"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"generated {OUTPUT}")


if __name__ == "__main__":
    main()
