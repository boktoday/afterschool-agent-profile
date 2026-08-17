#!/usr/bin/env python3
"""Generate storyboard frames via Google Nano Banana 2 Lite on OpenRouter.

Usage:
    python3 generate_frames.py storyboard.json out_dir/ [model]

storyboard.json is a list of:
    {"name": "verse1", "start": 15, "duration": 30,
     "prompt": "cinematic description, 16:9 widescreen"}

Requires OPENROUTER_API_KEY env var. Skips frames that already exist
(so a rerun only fills in the missing ones). Prints per-frame cost.
"""
import json
import os
import sys
import time
import base64
import urllib.request
import urllib.error

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "google/gemini-3.1-flash-lite-image"


def generate_frame(prompt: str, model: str = MODEL) -> tuple[bytes, float]:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
        "response_format": {"type": "image"},
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
            "X-OpenRouter-Title": "Poem Song Video Studio",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}")

    text = body.decode("utf-8", errors="replace")
    idx = text.find("{")
    data = json.loads(text[idx:])

    images = data.get("choices", [{}])[0].get("message", {}).get("images", [])
    if not images:
        raise RuntimeError("No image in response")
    url = images[0].get("image_url", {}).get("url", "")
    if not url.startswith("data:image"):
        raise RuntimeError(f"Unexpected URL format: {url[:80]}")

    b64 = url.split(",", 1)[1]
    cost = data.get("usage", {}).get("cost", 0)
    return base64.b64decode(b64), cost


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with open(sys.argv[1]) as f:
        frames = json.load(f)
    out_dir = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else MODEL
    os.makedirs(out_dir, exist_ok=True)

    total = 0.0
    for i, frame in enumerate(frames):
        out_path = os.path.join(out_dir, f"{i:02d}-{frame['name']}.jpg")
        if os.path.exists(out_path):
            print(f"[{i+1}/{len(frames)}] {frame['name']} — exists, skip")
            continue
        try:
            img, cost = generate_frame(frame["prompt"], model)
        except Exception as e:
            print(f"[{i+1}/{len(frames)}] {frame['name']} — FAILED: {e}")
            continue
        with open(out_path, "wb") as f:
            f.write(img)
        total += cost
        print(f"[{i+1}/{len(frames)}] {frame['name']} — {len(img)} bytes, ${cost:.4f}")
        time.sleep(1)

    print(f"DONE. {len(frames)} frames, total ${total:.4f}")


if __name__ == "__main__":
    main()
