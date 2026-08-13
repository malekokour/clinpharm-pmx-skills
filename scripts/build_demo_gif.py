#!/usr/bin/env python3
"""Build a public-safe synthetic workflow demo and social preview.

Author: ClinPharm PMx Skills contributors
Date: 2026-07-30
Dependencies: Pillow
"""

from __future__ import annotations

import shutil
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs/assets"
FRAMES = ASSETS / "demo"
SITE_ASSETS = ROOT / "site/assets"
WIDTH, HEIGHT = 1280, 720
NAVY = "#102A43"
INK = "#17324D"
TEAL = "#0B7A75"
MINT = "#E9F4F2"
BLUE = "#EAF0F6"
WHITE = "#FFFFFF"
GRAY = "#5F6B76"
LINE = "#CFD8E3"
AMBER = "#FFF3D6"

STEPS = [
    {
        "step": "01  ATTACH",
        "title": "Start in an ordinary AI chat",
        "user": "Start my pharma work context. Interview me.",
        "ai": "Before we begin: is this environment approved for the material you plan to use?",
        "side": ["DOCX or Markdown", "No agents required", "Skip is always allowed"],
    },
    {
        "step": "02  BOUNDARY",
        "title": "Establish the safety kernel first",
        "user": "Use public or synthetic information only.",
        "ai": "Confirmed: PUBLIC_OR_SYNTHETIC. I will not request patient, sponsor, submission, or employer-confidential content.",
        "side": ["Classification confirmed", "Restricted inputs stopped", "Human review retained"],
    },
    {
        "step": "03  INTERVIEW",
        "title": "Capture how the professional works",
        "user": "I support ClinPharm decisions and need concise, source-traceable summaries.",
        "ai": "What deliverables recur, which sources govern them, and which decisions require qualified review?",
        "side": ["Role and outcomes", "Evidence hierarchy", "Output preferences"],
    },
    {
        "step": "04  CONSTITUTION",
        "title": "Generate reusable professional context",
        "user": "Keep unknown decision rights visible.",
        "ai": "Created My-Pharma-Work-Context with a Safety Kernel, Professional Constitution, unknowns, and review triggers.",
        "side": ["Stable context", "Unknowns stay unknown", "Markdown is canonical"],
    },
    {
        "step": "05  PROJECT",
        "title": "Add permitted project sources",
        "user": "Create a capsule for synthetic project SYN-101.",
        "ai": "The final analysis reports 14.2 L/h and 90% intervals. The draft's 12.4 L/h and 80% intervals remain visible as superseded conflicts.",
        "side": ["Sources inventoried", "Authority order applied", "Conflicts preserved"],
    },
    {
        "step": "06  EXPORT",
        "title": "Carry one governed working pack",
        "user": "Export the context needed for this task.",
        "ai": "Created AI-Working-Pack-SYN-101: focused context, governing sources, unresolved questions, and required human review.",
        "side": ["Portable attachment", "Task-focused context", "No autonomous decision"],
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf"
        ),
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def wrapped(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int], face, fill: str) -> int:
    x, y, width_chars = box
    for line in wrap(text, width=width_chars):
        draw.text((x, y), line, font=face, fill=fill)
        y += face.size + 9
    return y


def pill(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str) -> None:
    draw.rounded_rectangle(xy, radius=16, fill=MINT)
    draw.text((xy[0] + 16, xy[1] + 9), text, font=font(20, True), fill=TEAL)


def build_frame(index: int, item: dict[str, object]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#F6F9FC")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 74), fill=NAVY)
    draw.text((44, 22), "CLINPHARM SKILLS", font=font(25, True), fill=WHITE)
    draw.text((965, 24), str(item["step"]), font=font(20, True), fill="#7FE0D4")
    draw.text((44, 104), str(item["title"]), font=font(38, True), fill=INK)
    draw.text(
        (44, 156),
        "Synthetic demonstration • no real company, project, or patient data",
        font=font(18),
        fill=GRAY,
    )

    draw.rounded_rectangle((44, 202, 895, 656), radius=26, fill=WHITE, outline=LINE, width=2)
    draw.text((74, 228), "ORDINARY AI CHAT", font=font(16, True), fill=GRAY)

    draw.rounded_rectangle((274, 274, 855, 378), radius=20, fill=BLUE)
    draw.text((300, 291), "YOU", font=font(15, True), fill=NAVY)
    wrapped(draw, str(item["user"]), (300, 321, 53), font(22), INK)

    ai_fill = AMBER if index == 4 else MINT
    draw.rounded_rectangle((82, 406, 738, 602), radius=20, fill=ai_fill)
    draw.text((108, 423), "AI + CLINPHARM SKILLS", font=font(15, True), fill=TEAL)
    wrapped(draw, str(item["ai"]), (108, 456, 55), font(21), INK)

    draw.rounded_rectangle((929, 202, 1236, 656), radius=26, fill=WHITE, outline=LINE, width=2)
    draw.text((960, 230), "WHAT TRAVELS", font=font(16, True), fill=GRAY)
    y = 292
    for value in item["side"]:
        pill(draw, (958, y, 1207, y + 50), str(value))
        y += 76
    draw.text((960, 572), f"{index + 1} / {len(STEPS)}", font=font(18, True), fill=TEAL)
    draw.text((960, 608), "Human-governed by design", font=font(16), fill=GRAY)
    return image


def build_social_preview() -> Image.Image:
    image = Image.new("RGB", (1280, 640), NAVY)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((62, 62, 1218, 578), radius=34, fill=WHITE)
    draw.text((112, 116), "CLINPHARM SKILLS", font=font(28, True), fill=TEAL)
    draw.text((112, 198), "Teach AI how", font=font(62, True), fill=NAVY)
    draw.text((112, 270), "pharma professionals work.", font=font(62, True), fill=NAVY)
    draw.text(
        (112, 382),
        "Portable context • source authority • human review",
        font=font(28),
        fill=GRAY,
    )
    pill(draw, (112, 462, 346, 516), "Attach in ordinary chat")
    pill(draw, (374, 462, 568, 516), "Use in Projects")
    pill(draw, (596, 462, 824, 516), "Install as a Skill")
    draw.rounded_rectangle((920, 136, 1138, 494), radius=28, fill=MINT)
    draw.text((967, 186), "Safety", font=font(26, True), fill=TEAL)
    draw.text((962, 266), "Context", font=font(26, True), fill=TEAL)
    draw.text((964, 346), "Project", font=font(26, True), fill=TEAL)
    draw.text((958, 426), "Working Pack", font=font(21, True), fill=TEAL)
    return image


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    SITE_ASSETS.mkdir(parents=True, exist_ok=True)
    frames: list[Image.Image] = []
    for index, item in enumerate(STEPS):
        image = build_frame(index, item)
        image.save(FRAMES / f"workflow-{index + 1:02d}.png", optimize=True)
        frames.append(image)
    gif_path = ASSETS / "clinpharm-pmx-skills-workflow.gif"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=[2600, 2700, 3000, 2700, 3300, 3000],
        loop=0,
        optimize=True,
    )
    preview = build_social_preview()
    preview.save(ASSETS / "social-preview.png", optimize=True)
    shutil.copy2(gif_path, SITE_ASSETS / "workflow.gif")
    shutil.copy2(ASSETS / "social-preview.png", SITE_ASSETS / "social-preview.png")
    print(f"Built {len(frames)} workflow frames, GIF, and social preview")


if __name__ == "__main__":
    main()
