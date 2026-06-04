#!/usr/bin/env python3
"""Generate weekly Matrix-themed profile visuals from public GitHub data."""

from __future__ import annotations

import json
import math
import os
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape


PROFILE_USERNAME = os.getenv("GITHUB_PROFILE_USERNAME", "msrishav-28")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ROOT = pathlib.Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"

COLORS = {
    "bg": "#0d1117",
    "panel": "#101820",
    "panel_dark": "#07110b",
    "neon": "#00FF41",
    "lime": "#39FF14",
    "chartreuse": "#B6FF00",
    "emerald": "#00E676",
    "teal": "#00BFA5",
    "deep": "#005F2F",
    "muted": "#7CFF6B",
    "text": "#D7FFE0",
}

PIE_COLORS = [
    COLORS["neon"],
    COLORS["chartreuse"],
    COLORS["emerald"],
    COLORS["teal"],
    "#00A000",
    COLORS["deep"],
]


def github_get(path: str):
    url = f"https://api.github.com/{path.lstrip('/')}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "msrishav-profile-visuals",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"warning: could not fetch {url}: {exc}")
        return None


def load_public_data():
    user = github_get(f"users/{PROFILE_USERNAME}") or {}
    repos = github_get(f"users/{PROFILE_USERNAME}/repos?per_page=100&sort=updated&type=owner")
    if not isinstance(repos, list):
        repos = []

    repos = [repo for repo in repos if not repo.get("fork")]
    language_bytes: dict[str, int] = {}

    for repo in repos:
        name = repo.get("name")
        if not name:
            continue
        langs = github_get(f"repos/{PROFILE_USERNAME}/{name}/languages")
        if not isinstance(langs, dict):
            continue
        for language, byte_count in langs.items():
            language_bytes[language] = language_bytes.get(language, 0) + int(byte_count)

    return user, repos, language_bytes


def polar_to_xy(cx: float, cy: float, radius: float, angle: float):
    radians = math.radians(angle)
    return cx + radius * math.cos(radians), cy + radius * math.sin(radians)


def pie_path(cx: float, cy: float, radius: float, start: float, end: float):
    x1, y1 = polar_to_xy(cx, cy, radius, start)
    x2, y2 = polar_to_xy(cx, cy, radius, end)
    large_arc = 1 if end - start > 180 else 0
    return (
        f"M {cx:.0f} {cy:.0f} L {x1:.2f} {y1:.2f} "
        f"A {radius:.0f} {radius:.0f} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z"
    )


def language_rows(language_bytes: dict[str, int]):
    rows = sorted(language_bytes.items(), key=lambda item: item[1], reverse=True)[:6]
    if not rows:
        rows = [
            ("Python", 569),
            ("TypeScript", 212),
            ("Dart", 155),
            ("JavaScript", 38),
            ("Kotlin", 21),
            ("PLpgSQL", 3),
        ]
    total = sum(value for _, value in rows) or 1
    return [(name, value, (value / total) * 100) for name, value in rows]


def generate_language_svg(language_bytes: dict[str, int]):
    rows = language_rows(language_bytes)
    total = sum(value for _, value, _ in rows) or 1
    cx, cy, radius = 220, 170, 108
    current = -90.0
    slices = []

    for index, (name, value, _) in enumerate(rows):
        sweep = (value / total) * 360
        next_angle = current + sweep
        slices.append(
            f'<path d="{pie_path(cx, cy, radius, current, next_angle)}" '
            f'fill="{PIE_COLORS[index % len(PIE_COLORS)]}" '
            'stroke="#0d1117" stroke-width="3"/>'
        )
        current = next_angle

    legend = []
    for index, (name, _, pct) in enumerate(rows):
        x = 455 if index < 5 else 715
        y = 105 + (index * 35) if index < 5 else 245
        color = PIE_COLORS[index % len(PIE_COLORS)]
        legend.append(
            f'''<g transform="translate({x} {y})">
      <rect width="18" height="18" rx="2" fill="{color}"/>
      <text x="30" y="14" font-size="14" fill="{COLORS["text"]}">{escape(name)}</text>
      <text x="250" y="14" font-size="14" fill="{color}" text-anchor="end">{pct:.1f}%</text>
    </g>'''
        )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return f'''<svg width="900" height="340" viewBox="0 0 900 340" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="neon">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{COLORS["panel"]}"/>
      <stop offset="100%" stop-color="{COLORS["panel_dark"]}"/>
    </linearGradient>
  </defs>
  <rect width="900" height="340" rx="8" fill="{COLORS["bg"]}"/>
  <rect x="18" y="18" width="864" height="304" rx="6" fill="url(#panel)" stroke="{COLORS["neon"]}" stroke-opacity="0.35"/>
  <text x="42" y="52" font-family="Courier New, monospace" font-size="18" font-weight="700" fill="{COLORS["neon"]}" filter="url(#neon)">&gt; LANGUAGE_MATRIX</text>
  <text x="42" y="76" font-family="Courier New, monospace" font-size="12" fill="{COLORS["muted"]}">Weekly public-repo language snapshot. Distinct green slices, no noisy README rewrites.</text>
  <g transform="translate(35 10)">
    {"".join(slices)}
    <circle cx="{cx}" cy="{cy}" r="55" fill="{COLORS["bg"]}" stroke="{COLORS["neon"]}" stroke-opacity="0.45"/>
    <text x="{cx}" y="{cy - 6}" font-family="Courier New, monospace" font-size="12" fill="{COLORS["muted"]}" text-anchor="middle">TOP</text>
    <text x="{cx}" y="{cy + 17}" font-family="Courier New, monospace" font-size="21" font-weight="700" fill="{COLORS["neon"]}" text-anchor="middle">{len(rows)}</text>
  </g>
  <g font-family="Courier New, monospace">
    {"".join(legend)}
  </g>
  <text x="42" y="302" font-family="Courier New, monospace" font-size="11" fill="{COLORS["muted"]}">Updated weekly from GitHub API: {generated}</text>
</svg>
'''


def generate_proof_svg(user: dict, repos: list[dict], language_bytes: dict[str, int]):
    public_repos = int(user.get("public_repos") or len(repos) or 0)
    source_repos = len(repos)
    live_links = sum(1 for repo in repos if repo.get("homepage"))
    top_language = language_rows(language_bytes)[0][0]
    latest_push = max((repo.get("pushed_at") or "" for repo in repos), default="")
    latest_push = latest_push[:10] if latest_push else "tracked"
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    cards = [
        ("PUBLIC REPOS", f"{public_repos}", "GitHub visible"),
        ("SOURCE REPOS", f"{source_repos}", "Non-fork repos"),
        ("LIVE LINKS", f"{live_links}", "Homepage fields"),
        ("TOP LANGUAGE", top_language.upper()[:12], "By repo bytes"),
        ("RECENT PUSH", latest_push, "Public metadata"),
        ("REFRESH", "WEEKLY", generated),
    ]

    card_svg = []
    for index, (title, value, meta) in enumerate(cards):
        x = 42 + index * 140
        color = COLORS["neon"] if index % 2 == 0 else COLORS["chartreuse"]
        card_svg.append(
            f'''<g class="float" transform="translate({x} 108)" style="animation-delay:{index * 0.45:.2f}s">
    <rect width="126" height="72" rx="6" fill="{COLORS["bg"]}" stroke="{color}" stroke-opacity=".48"/>
    <text x="14" y="24" class="label">{escape(title)}</text>
    <text x="14" y="50" fill="{color}" font-size="20" font-weight="700">{escape(value)}</text>
    <text x="14" y="64" class="meta">{escape(meta)}</text>
  </g>'''
        )

    return f'''<svg width="900" height="220" viewBox="0 0 900 220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="signalPanel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{COLORS["panel_dark"]}"/>
      <stop offset="50%" stop-color="{COLORS["panel"]}"/>
      <stop offset="100%" stop-color="{COLORS["panel_dark"]}"/>
    </linearGradient>
    <style>
      .mono {{ font-family: "Courier New", monospace; }}
      .title {{ fill: {COLORS["neon"]}; font-size: 14px; font-weight: 700; }}
      .label {{ fill: {COLORS["text"]}; font-size: 11px; font-weight: 700; }}
      .meta {{ fill: {COLORS["muted"]}; font-size: 9px; }}
      @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-4px); }}
      }}
      .float {{ animation: float 6s ease-in-out infinite; }}
    </style>
  </defs>
  <rect width="900" height="220" rx="8" fill="{COLORS["bg"]}"/>
  <rect x="18" y="18" width="864" height="184" rx="6" fill="url(#signalPanel)" stroke="{COLORS["neon"]}" stroke-opacity=".28"/>
  <g opacity=".14" class="mono" fill="{COLORS["neon"]}" font-size="10">
    <text x="42" y="44">01001 11010 00101 11100 01011 10010 01101</text>
    <text x="585" y="190">10110 00111 01001 11000 01110 10001</text>
  </g>
  <text x="42" y="56" class="mono title" filter="url(#softGlow)">&gt; PROOF_SIGNALS</text>
  <text x="42" y="78" class="mono meta">A restrained signal board: public GitHub evidence, not inflated trophies.</text>
  {"".join(card_svg)}
</svg>
'''


def main():
    ASSETS.mkdir(exist_ok=True)
    user, repos, language_bytes = load_public_data()
    (ASSETS / "matrix-languages.svg").write_text(generate_language_svg(language_bytes), encoding="utf-8")
    (ASSETS / "matrix-achievements.svg").write_text(generate_proof_svg(user, repos, language_bytes), encoding="utf-8")
    print("Generated matrix-languages.svg and matrix-achievements.svg")


if __name__ == "__main__":
    main()
