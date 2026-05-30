"""
wetch - WeChat Article Formatter

Convert structured markdown to WeChat Official Account-compatible HTML.
"""

__version__ = "1.0.0"

import re
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── Template Registry ──────────────────────────────────────────────────

TEMPLATES = {
    "default": {
        "name": "默认 · 极简红",
        "accent": "#cc3333",
        "bg_dark": "#2d0a0a",
        "bg_light": "#fdf0f0",
        "text_dark": "#8b0000",
        "body_bg": "#ffffff",
        "body_color": "#333333",
    },
    "blue": {
        "name": "科技蓝",
        "accent": "#4a6cf7",
        "bg_dark": "#1a1a2e",
        "bg_light": "#eef1ff",
        "text_dark": "#2a3db0",
        "body_bg": "#ffffff",
        "body_color": "#333333",
    },
    "green": {
        "name": "自然绿",
        "accent": "#2d8a57",
        "bg_dark": "#0a1a12",
        "bg_light": "#e8f5ee",
        "text_dark": "#1a6b3d",
        "body_bg": "#ffffff",
        "body_color": "#333333",
    },
    "purple": {
        "name": "典雅紫",
        "accent": "#7c3aed",
        "bg_dark": "#1a0a2e",
        "bg_light": "#f3eefb",
        "text_dark": "#5b21b6",
        "body_bg": "#ffffff",
        "body_color": "#333333",
    },
    "minimal": {
        "name": "极简灰",
        "accent": "#636366",
        "bg_dark": "#1c1c1e",
        "bg_light": "#f2f2f7",
        "text_dark": "#48484a",
        "body_bg": "#ffffff",
        "body_color": "#333333",
    },
}


@dataclass
class Article:
    """Parsed article from markdown input."""
    title: str = ""
    subtitle: str = ""
    author: str = "wetch"
    date: str = ""
    tags: list = field(default_factory=list)
    sections: list = field(default_factory=list)
    cover_text: str = ""


@dataclass
class Section:
    type: str  # "header", "paragraph", "quote", "emphasis", "image", "list", "divider"
    content: str = ""
    level: int = 0  # for headers
    items: list = field(default_factory=list)  # for lists


# ── Parser ─────────────────────────────────────────────────────────────

def parse_markdown(text: str) -> Article:
    """Parse structured markdown into an Article object."""
    article = Article()
    lines = text.split("\n")
    i = 0
    current_section = None
    current_list_items = []
    in_list = False
    in_code_block = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code block toggle
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            i += 1
            continue

        if in_code_block:
            # Treat code block as paragraph content
            article.sections.append(Section(type="code", content=line.replace("\t", "  ")))
            i += 1
            continue

        # Skip empty lines (except as dividers between sections)
        if not stripped:
            if in_list:
                in_list = False
                if current_list_items:
                    article.sections.append(Section(type="list", items=current_list_items))
                    current_list_items = []
            i += 1
            continue

        # Title (h1 with ##)
        if stripped.startswith("## ") and not stripped.startswith("#### "):
            article.title = stripped[3:].strip()
            i += 1
            continue

        # Subtitle (h2 with ###)
        if stripped.startswith("### ") and not stripped.startswith("##### "):
            article.subtitle = stripped[4:].strip()
            i += 1
            continue

        # Subsection header (h3 with ####)
        if stripped.startswith("#### "):
            article.sections.append(Section(type="header", content=stripped[5:].strip(), level=3))
            i += 1
            continue

        # Cover text directive
        if stripped.startswith("> cover:") or stripped.startswith("> 封面:"):
            article.cover_text = stripped.split(":", 1)[1].strip()
            i += 1
            continue

        # Tags
        if stripped.startswith("tags:") or stripped.startswith("标签:"):
            tag_str = stripped.split(":", 1)[1].strip()
            article.tags = [t.strip().strip("#") for t in tag_str.split(",")]
            i += 1
            continue

        # Date
        if stripped.startswith("date:") or stripped.startswith("日期:"):
            article.date = stripped.split(":", 1)[1].strip()
            i += 1
            continue

        # Author
        if stripped.startswith("author:") or stripped.startswith("作者:"):
            article.author = stripped.split(":", 1)[1].strip()
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            content = stripped[1:].strip()
            article.sections.append(Section(type="quote", content=content))
            i += 1
            continue

        # Unordered list
        if stripped.startswith("- ") or stripped.startswith("* "):
            in_list = True
            current_list_items.append(stripped[2:].strip())
            i += 1
            continue

        # Ordered list
        if re.match(r"^\d+\.\s", stripped):
            in_list = True
            current_list_items.append(re.sub(r"^\d+\.\s", "", stripped))
            i += 1
            continue

        # Flush pending list
        if in_list:
            in_list = False
            if current_list_items:
                article.sections.append(Section(type="list", items=current_list_items))
                current_list_items = []

        # Divider
        if stripped in ("---", "***", "———"):
            article.sections.append(Section(type="divider"))
            i += 1
            continue

        # Regular paragraph
        # Check for bold markers: **text**
        content = stripped
        article.sections.append(Section(type="paragraph", content=content))
        i += 1

    # Flush lingering list
    if in_list and current_list_items:
        article.sections.append(Section(type="list", items=current_list_items))

    return article


# ── HTML Rendering ─────────────────────────────────────────────────────

def _render_paragraph(content: str, theme: str) -> str:
    """Render a paragraph with inline formatting."""
    colors = TEMPLATES.get(theme, TEMPLATES["default"])

    # Inline bold: **text**
    content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
    # Inline italic: *text*
    content = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", content)
    # Inline code: `text`
    content = re.sub(r"`([^`]+)`", r"<code style=\"font-family: Menlo, monospace; font-size: 13px; background: #f5f5f5; padding: 2px 6px; border-radius: 3px;\">\1</code>", content)
    # Links: [text](url)
    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" style="color: \1; text-decoration: underline;">\1</a>', content)

    return f'<p style="margin-bottom: 16px; line-height: 1.8;">{content}</p>'


def render_html(article: Article, theme: str = "default") -> str:
    """Render Article to WeChat-compatible HTML."""
    colors = TEMPLATES.get(theme, TEMPLATES["default"])
    accent = colors["accent"]
    bg_dark = colors["bg_dark"]
    bg_light = colors["bg_light"]
    text_dark = colors["text_dark"]
    body_bg = colors["body_bg"]
    body_color = colors["body_color"]

    parts = []

    # Header card
    parts.append(f'''<section style="padding: 20px 16px; line-height: 1.8; font-size: 15px; color: {body_color}; max-width: 640px; margin: 0 auto;">

<!-- Header Card -->
<section style="background: {bg_dark}; border-radius: 12px; padding: 32px 24px; margin-bottom: 28px;">
  <h1 style="font-size: 20px; color: #ffffff; margin: 0 0 8px 0; font-weight: 700; line-height: 1.4;">{article.title}</h1>
  {f'<p style="font-size: 14px; color: rgba(255,255,255,0.6); margin: 0; line-height: 1.5;">{article.subtitle}</p>' if article.subtitle else ''}
</section>''')

    # Sections
    for section in article.sections:
        if section.type == "paragraph":
            parts.append(_render_paragraph(section.content, theme))

        elif section.type == "header":
            parts.append(
                f'<h2 style="font-size: 17px; color: {accent}; border-left: 4px solid {accent}; padding-left: 12px; margin: 28px 0 16px 0;">{section.content}</h2>'
            )

        elif section.type == "quote":
            parts.append(
                f'''<table style="width: 100%; margin: 24px 0;" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="background: {bg_light}; border-radius: 8px; padding: 16px 20px; border-left: 4px solid {accent};">
      <p style="margin: 0; font-size: 14px; color: {text_dark}; line-height: 1.6;">{section.content}</p>
    </td>
  </tr>
</table>'''
            )

        elif section.type == "emphasis":
            parts.append(
                f'''<table style="width: 100%; margin: 24px 0;" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="background: {bg_dark}; border-radius: 8px; padding: 20px 24px;">
      <p style="margin: 0; font-size: 16px; color: #ffffff; line-height: 1.5; text-align: center;">
      <strong>{section.content}</strong>
      </p>
    </td>
  </tr>
</table>'''
            )

        elif section.type == "list":
            items_html = ""
            for item in section.items:
                items_html += f'<tr><td style="padding: 4px 0; line-height: 1.6; color: {body_color};">• {item}</td></tr>\n'
            parts.append(
                f'<table style="width: 100%; margin: 16px 0;" cellpadding="0" cellspacing="0" border="0">\n{items_html}</table>'
            )

        elif section.type == "code":
            # Escape HTML entities
            code = section.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parts.append(
                f'<pre style="background: #1c1c1e; border-radius: 8px; padding: 16px; font-size: 13px; line-height: 1.5; overflow-x: auto; margin: 12px 0;"><code style="color: #e4e4e4; font-family: Menlo, monospace;">{code}</code></pre>'
            )

        elif section.type == "divider":
            parts.append(
                f'''<table style="width: 100%; margin: 24px 0;" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="height: 1px; background: {accent}; opacity: 0.3;"></td>
  </tr>
</table>'''
            )

    # Tags
    if article.tags:
        tags_html = ""
        for tag in article.tags:
            tags_html += f'<td style="background: {accent}; border-radius: 20px; padding: 4px 14px; margin-right: 8px; display: inline-block;"><span style="font-size: 13px; color: #ffffff;">#{tag}</span></td>\n'
        parts.append(
            f'''<div style="margin-top: 24px;">{tags_html}</div>'''
        )

    # Footer
    parts.append(
        f'''<p style="font-size: 12px; color: #999999; margin-top: 32px; border-top: 1px solid #eeeeee; padding-top: 16px;">
Generated by wetch · {article.date if article.date else ''}
</p>

</section>'''
    )

    return "\n\n".join(parts)


# ── Cover HTML Generator ───────────────────────────────────────────────

def render_cover_html(article: Article, theme: str = "default") -> str:
    """Generate an HTML file for screenshot-based cover image."""
    colors = TEMPLATES.get(theme, TEMPLATES["default"])
    accent = colors["accent"]
    bg_dark = colors["bg_dark"]

    cover_main = article.cover_text or article.title[:30] if len(article.title) <= 30 else article.title[:26] + "..."

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1200px; height: 675px;
    background: linear-gradient(160deg, {bg_dark} 0%, #000000 100%);
    font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    overflow: hidden; position: relative;
  }}
  .grid {{
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
  }}
  .circle {{
    position: absolute; top: -80px; right: -60px; width: 350px; height: 350px;
    border-radius: 50%;
    background: radial-gradient(circle, {accent}22 0%, transparent 70%);
  }}
  .ring {{
    position: absolute; top: 80px; right: 100px; width: 150px; height: 150px;
    border-radius: 50%; border: 1px solid {accent}33;
  }}
  .brand {{
    position: absolute; top: 36px; left: 60px;
    padding: 6px 16px; border: 1px solid {accent}44;
    border-radius: 20px; font-size: 13px; color: {accent}99;
    letter-spacing: 2px;
  }}
  .title-area {{
    position: absolute; left: 60px; right: 80px; bottom: 200px;
  }}
  .title {{
    font-size: 44px; font-weight: 800; color: #ffffff;
    line-height: 1.2; letter-spacing: 1px;
  }}
  .title .hl {{
    background: linear-gradient(135deg, #ffffff, {accent});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .sub {{
    font-size: 18px; color: rgba(255,255,255,0.5); margin-top: 16px;
    letter-spacing: 3px;
  }}
  .footer {{
    position: absolute; left: 60px; right: 80px; bottom: 32px;
    display: flex; justify-content: space-between;
    font-size: 12px; color: rgba(255,255,255,0.2);
  }}
</style>
</head>
<body>
<div class="grid"></div>
<div class="circle"></div>
<div class="ring"></div>
<div class="brand">wetch · {theme}</div>
<div class="title-area">
  <div class="title"><span class="hl">{cover_main}</span></div>
  <div class="sub">{article.subtitle[:40] if article.subtitle else "WeChat · 公众号文章"}</div>
</div>
<div class="footer">
  <span>wetch · 一键格式化</span>
  <span>{article.date if article.date else ""}</span>
</div>
</body>
</html>'''