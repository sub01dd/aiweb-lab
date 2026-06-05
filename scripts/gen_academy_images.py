"""Regenerate 4 images — Stripe Press style: low-saturation, editorial, restrained."""
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
OUT = Path("c:/Users/zenno/aiweb-lab/assets/img/demos/academy")
OUT.mkdir(parents=True, exist_ok=True)

PROMPTS = {
    "fv.png": (
        "Editorial documentary photograph for a Stripe Press style publishing site. "
        "A 30-something Japanese marketing strategist sits at a clean light wood desk in a "
        "quiet bright study. He is shown in three-quarter back view, looking down at an "
        "open paperback book on the desk, face obscured. Soft diffused window light fills "
        "the room. On the desk: the open paperback (cream pages, small vermilion red ribbon "
        "bookmark visible), a closed notebook, a single ceramic mug, a Pilot fountain pen, "
        "neat papers. He wears a plain dark grey crewneck sweater. Background is soft "
        "off-white wall with a subtle hint of a bookshelf. Low saturation, warm neutral "
        "tones, fine film grain, gentle natural shadows, very restrained composition with "
        "generous negative space. A single small vermilion accent (the bookmark ribbon) as "
        "the only color note. Vertical 4:5 framing. No text, no logos, no UI."
    ),
    "portrait.png": (
        "Overhead flat-lay editorial photograph in Stripe Press publishing aesthetic. "
        "Top-down view of a quiet light wood desk. Composition: an open hardcover book "
        "showing typeset Japanese text (blurred so unreadable) with a small vermilion red "
        "ribbon bookmark, a closed paper notebook in cream linen cover, a Pilot fountain "
        "pen, a single ceramic espresso cup, a folded pair of round reading glasses, neat "
        "stack of off-white papers. No human visible. Soft diffused daylight from upper "
        "left, gentle shadows. Low saturation, warm neutral palette of cream, oat, soft "
        "grey, with a single vermilion accent as the only color note. Generous negative "
        "space around objects. Vertical 4:5 framing. No text, no readable UI."
    ),
    "voice01.png": (
        "Editorial portrait photograph in restrained publishing aesthetic. A young man's "
        "hands rest on a clean desk beside a closed paper notebook and a thin laptop "
        "(closed). One hand holds a Pilot fountain pen, the other rests on the notebook. "
        "Soft natural daylight from a large window, plain off-white wall behind. He wears a "
        "plain grey shirt with rolled-up sleeves, a simple watch. No face visible, only "
        "hands and forearms. Restrained, contemplative atmosphere. Low saturation, warm "
        "neutral palette, fine film grain. Vertical 4:5 framing. No text, no readable UI."
    ),
    "voice02.png": (
        "Editorial documentary photograph in Stripe Press aesthetic. Overhead view of a "
        "calm cafe table by a window during early afternoon. A young man's right hand "
        "annotates a paper printout of a simple line chart with a Pilot fountain pen. "
        "Beside the printout: a small ceramic espresso cup, a closed paperback book with a "
        "vermilion red ribbon bookmark, round reading glasses, a folded grey wool scarf. "
        "Only the hand visible, no face. Soft daylight from the window, warm wooden table. "
        "Low saturation, restrained warm neutral palette with a single vermilion accent. "
        "Vertical 4:5 framing. No text, no readable UI."
    ),
}

for name, prompt in PROMPTS.items():
    out = OUT / name
    print(f"generating: {name} ...", flush=True)
    try:
        res = client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1536", n=1)
        out.write_bytes(base64.b64decode(res.data[0].b64_json))
        print(f"  saved: {out} ({out.stat().st_size:,} bytes)", flush=True)
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
