"""wetch CLI – Convert markdown to WeChat-ready HTML."""

import sys
import argparse
from pathlib import Path

from wetch import (
    __version__,
    TEMPLATES,
    parse_markdown,
    render_html,
    render_cover_html,
)


def main():
    parser = argparse.ArgumentParser(
        prog="wetch",
        description="WeChat Article Formatter – Convert markdown to WeChat-ready HTML",
        epilog="Examples:\n"
               "  wetch article.md -o output.html           # Convert to HTML\n"
               "  wetch article.md --theme blue              # Use blue theme\n"
               "  wetch article.md --cover                   # Generate cover HTML\n"
               "  wetch --list-themes                        # List available themes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="Input markdown file (or '-' for stdin)")
    parser.add_argument("-o", "--output", help="Output HTML file (default: stdout)")
    parser.add_argument("-t", "--theme", default="default", choices=list(TEMPLATES.keys()),
                        help=f"Color theme (default: default)")
    parser.add_argument("--cover", action="store_true",
                        help="Generate cover image HTML instead of article HTML")
    parser.add_argument("--list-themes", action="store_true",
                        help="List available themes and exit")
    parser.add_argument("-V", "--version", action="version", version=f"wetch {__version__}")

    args = parser.parse_args()

    # List themes
    if args.list_themes:
        print("Available themes:\n")
        for key, t in TEMPLATES.items():
            print(f"  {key:12s} {t['name']}  (accent: {t['accent']})")
        sys.exit(0)

    # Read input
    if args.input == "-" or not args.input:
        text = sys.stdin.read()
    elif args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"Error: file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
    else:
        parser.print_help()
        sys.exit(1)

    # Parse and render
    article = parse_markdown(text)

    if args.cover:
        html = render_cover_html(article, theme=args.theme)
    else:
        html = render_html(article, theme=args.theme)

    # Output
    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
        print(f"✓ Written to {args.output}", file=sys.stderr)
    else:
        print(html, end="")


if __name__ == "__main__":
    main()