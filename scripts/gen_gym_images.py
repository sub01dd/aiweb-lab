"""Generate 2 placeholder photos for demos/gym.html (FORGE personal gym)."""
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

OUT = Path("c:/Users/zenno/aiweb-lab/assets/img/demos/gym")
OUT.mkdir(parents=True, exist_ok=True)

PROMPTS = {
    "trainer.png": (
        "Editorial documentary photograph of a male Japanese personal trainer in his "
        "mid-30s standing inside a high-end private personal gym studio. He is shown "
        "from the side and back at three-quarter angle, arms crossed, face mostly out "
        "of frame or in deep shadow so not recognizable. He wears a fitted black "
        "training t-shirt and dark joggers. Behind him: a single squat rack, polished "
        "wood floor, exposed concrete wall, soft warm tungsten light from above. Heavy "
        "cinematic chiaroscuro, deep shadows, moody dark atmosphere. Color palette: "
        "near-black charcoal #0a0a0a, warm gold accent from the lighting, no neon, "
        "low saturation. Vertical 4:5 framing. No text, no logos, no readable signage."
    ),
    "bezel.png": (
        "Editorial documentary photograph of a high-end private personal gym training "
        "room during a session. Tight composition showing a male trainer in black t-shirt "
        "from behind crouching to spot a client doing a barbell squat. Only the trainer's "
        "back and the client's silhouette in deep shadow are visible, no recognizable "
        "faces. Polished dark wood floor, exposed concrete walls, a single squat rack, "
        "rubber-coated weight plates, a wall mirror reflecting warm tungsten light. "
        "Heavy cinematic chiaroscuro, deep shadows, moody dark atmosphere. Color palette: "
        "near-black charcoal #0a0a0a, warm gold tungsten highlights from lighting, no "
        "neon, low saturation, slight film grain. Vertical 4:5 framing. No text, no "
        "logos, no readable signage."
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
