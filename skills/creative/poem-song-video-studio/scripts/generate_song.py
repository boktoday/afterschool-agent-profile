#!/usr/bin/env python3
"""Generate a song from a lyrics/prompt file via Google Lyria 3 on OpenRouter.

Usage:
    python3 generate_song.py prompt.txt output.mp3 [model]

The prompt file must be a plain-text prompt (genre description + [Verse]/
[Chorus] tags + lyrics). The working format is: plain-string content +
stream:true — structured content arrays return text only, no audio.

Requires OPENROUTER_API_KEY env var or edit API_KEY below (not recommended —
prefer env var).
"""
import json
import os
import sys
import base64
import urllib.request
import urllib.error

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "google/lyria-3-pro-preview"


def generate(prompt: str, model: str = MODEL) -> bytes:
    if not API_KEY:
        raise SystemExit("OPENROUTER_API_KEY not set")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "modalities": ["text", "audio"],
        "response_format": {"type": "audio"},
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
        with urllib.request.urlopen(req, timeout=600) as resp:
            body = resp.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode()[:500]}")

    text = body.decode("utf-8", errors="replace")
    audio_parts = []
    for line in text.split("\n"):
        if not line.startswith("data: "):
            continue
        payload_line = line[6:]
        if payload_line == "[DONE]":
            continue
        try:
            obj = json.loads(payload_line)
        except Exception:
            continue
        for ch in obj.get("choices", []):
            delta = ch.get("delta", {})
            audio = delta.get("audio")
            if audio and audio.get("data"):
                audio_parts.append(audio["data"])

    if not audio_parts:
        raise SystemExit(
            "No audio in stream. Used structured content? Use plain-string "
            "content + stream:true. (Check usage.audio_tokens in the last chunk.)"
        )

    return base64.b64decode("".join(audio_parts))


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    prompt_path = sys.argv[1]
    out_path = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else MODEL

    with open(prompt_path) as f:
        prompt = f.read()

    print(f"Generating song with {model}...")
    audio = generate(prompt, model)
    with open(out_path, "wb") as f:
        f.write(audio)
    print(f"Saved {out_path} ({len(audio)} bytes)")


if __name__ == "__main__":
    main()
