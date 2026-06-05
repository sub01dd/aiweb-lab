"""Generate a browser-screenshot-style thumbnail for the SIGNAL demo card."""
import os, sys, base64
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY not set"); sys.exit(1)

from openai import OpenAI
client = OpenAI()

OUT = Path("c:/Users/zenno/aiweb-lab/assets/img/demos/academy.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

PROMPT = (
    "A clean web browser screenshot capture of a Japanese marketing course landing page. "
    "Top of the screenshot shows a thin dark sticky banner. Below that, a narrow soft beige "
    "sticky info bar. Below that, a white header bar containing a small red square brand "
    "mark on the left (looks like a small red tag), brand text in dark, a horizontal nav "
    "menu of short Japanese link labels, and a blue rectangular CTA button on the right. "
    "Main hero section below: large bold Japanese-Latin mixed headline filling most of the "
    "left half (suggest blurred dense kanji text with one word having a soft highlight "
    "behind it), a subtitle paragraph in two lines, three statistic tiles in a row "
    "(separated by thin vertical lines, each showing a large number and a small uppercase "
    "label), two CTA buttons (one filled muted blue, one outlined dark). Right half of "
    "the hero is intentionally empty white space. "
    "Style: realistic browser screenshot at 1440px width viewport, off-white background "
    "#fbfaf7, dark charcoal text #33333a, muted dusty blue accent #355a8c, no neon, "
    "restrained editorial business tone. No real readable letters needed, just clean "
    "layout structure. 16:10 horizontal composition. Looks like a tasteful Japanese SaaS "
    "marketing landing page."
)

print("generating: academy.png (browser screenshot style) ...", flush=True)
res = client.images.generate(model="gpt-image-1", prompt=PROMPT, size="1536x1024", n=1)
OUT.write_bytes(base64.b64decode(res.data[0].b64_json))
print(f"  saved: {OUT} ({OUT.stat().st_size:,} bytes)", flush=True)
