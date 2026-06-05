"""Generate 3 placeholder photos for salon.html and coach.html."""
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

JOBS = [
    {
        "out": "c:/Users/zenno/aiweb-lab/assets/img/demos/salon/portrait.png",
        "size": "1024x1536",
        "prompt": (
            "Editorial documentary photograph of a Japanese female osteopath in her late 30s "
            "standing in a quiet warm minimalist treatment room. Shown in three-quarter back "
            "view, face out of frame so not recognizable. She wears a simple beige linen "
            "tunic, hands gently resting at her sides. Behind her: a low wooden treatment "
            "table covered with a folded cream cotton sheet, a small ceramic vase with a "
            "single dried branch, soft tatami-tone wall, large window with soft diffused "
            "daylight from the left. Warm restrained palette: cream, oat, soft brown, hint "
            "of indigo. Fine film grain, gentle natural shadows, very calm contemplative "
            "atmosphere. Vertical 4:5 framing. No text, no logos, no signage."
        ),
    },
    {
        "out": "c:/Users/zenno/aiweb-lab/assets/img/demos/coach/hero.png",
        "size": "1024x1536",
        "prompt": (
            "Editorial documentary photograph of a Japanese woman in her late 30s sitting at "
            "a window-side wooden desk in a quiet bright study, three-quarter back view, "
            "writing in a hardcover paper notebook with a fountain pen. Face out of frame "
            "so not recognizable. She wears a plain cream cashmere sweater. On the desk: "
            "the open notebook, a vintage fountain pen, a single ceramic mug, a small stack "
            "of paperback books, a tiny vermilion-red ribbon bookmark as the only color "
            "accent. Soft natural daylight from the large window behind her, off-white wall, "
            "muted Japanese washi paper aesthetic. Low saturation, warm neutral palette, "
            "fine film grain. Vertical 4:5 framing. No text, no logos."
        ),
    },
    {
        "out": "c:/Users/zenno/aiweb-lab/assets/img/demos/coach/profile.png",
        "size": "1024x1536",
        "prompt": (
            "Editorial portrait photograph of a Japanese female career coach in her late 30s "
            "in a bright minimalist office. Shown in profile from the side, face turned "
            "downward looking at her hands resting on an open paper notebook, so the face "
            "is not recognizable. She wears a simple dark navy crewneck cashmere sweater "
            "and small pearl earrings. Soft natural window light from the left, plain "
            "off-white wall behind, a single small plant in the background. Warm restrained "
            "palette: off-white, navy, oat tones. Low saturation, fine film grain, "
            "contemplative and trustworthy atmosphere. Vertical 4:5 framing. No text, no "
            "logos, no readable signage."
        ),
    },
]

import base64

for j in JOBS:
    out = Path(j["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"generating: {out.name} ...", flush=True)
    try:
        res = client.images.generate(model="gpt-image-1", prompt=j["prompt"], size=j["size"], n=1)
        out.write_bytes(base64.b64decode(res.data[0].b64_json))
        print(f"  saved: {out} ({out.stat().st_size:,} bytes)", flush=True)
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
