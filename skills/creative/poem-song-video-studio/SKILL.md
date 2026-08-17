---
name: poem-song-video-studio
description: Turn an idea or poem into a poem, an AI song (Lyria 3 via OpenRouter), and/or a storyboard music video with optional poem-text overlay. Use when the user wants a poem set to music, a song, or a video for a poem.
version: 1.0.0
author: Afterschool Agent
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - poetry
    - music
    - video
    - openrouter
    - lyria
    - nano-banana
    - ffmpeg
---

# Poem → Song → Video Studio

One pipeline, three output levels. Ask the user which they want, or
default to the full pipeline when they say "make me a song/video":

- **Mode A — Poem:** write an original poem from a theme or source text
- **Mode B — Song:** Mode A + generate a real MP3 song from the poem
- **Mode C — Video:** Mode B + storyboard images stitched into a music video
  - Optional: overlay the poem's text on the images (subtitles)

Total cost for the full pipeline: **~$0.35** (song $0.08 + ~8 images $0.27).
Audio and video generation are NOT free — confirm spend before running.

## Prerequisites

- `OPENROUTER_API_KEY` in the profile `.env` (never in memory or chat).
  Verify without spending:
  ```bash
  curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $OPENROUTER_API_KEY"
  ```
- `ffmpeg` installed (`which ffmpeg`). Needed only for Mode C.

## Naming pitfall — Lyria vs Lyra

- **Lyria** (with i) = Google's MUSIC GENERATION model. What you want.
- **Lyra** (no i) = Google's SPEECH CODEC for compressing voice calls. It does NOT make music.
- The names sound identical. When a user says "Lyra makes music," they almost always mean Lyria. Check the model list before dismissing the request.

## Models used (all on OpenRouter)

| Model | ID | Cost | Purpose |
|---|---|---|---|
| Lyria 3 Pro | `google/lyria-3-pro-preview` | $0.08/song | Full-length song from text |
| Lyria 3 Clip | `google/lyria-3-clip-preview` | $0.04/30s clip | Short clip / loop |
| Nano Banana 2 Lite | `google/gemini-3.1-flash-lite-image` | ~$0.034/image | Storyboard frames (cheapest) |
| Nano Banana 2 | `google/gemini-3.1-flash-image` | ~$0.08/image | Nicer frames if budget allows |

Cheapest alternative: Nano Banana 1 (`google/gemini-2.5-flash-image`, ~$0.05/image).

---

## Mode A — Write the poem

Ground the poem in the source (a guide chapter, a theme, a person's
story). Pull real details from the source — names, scenes, phrases —
so it doesn't read as generic filler.

Structure it for singing later:
- 3–5 stanzas, roughly 4–6 lines each
- A repeating chorus (the emotional core, the hook)
- A bridge that shifts perspective
- An outro that lands the theme

## Mode B — Turn it into a song

### CRITICAL: the request format that returns audio

The model-page example and structured-content format (`content` as an
array of `{type: text}` blocks) return ONLY the timed lyrics text —
NO audio, even though you're billed. **The working format:**

- `messages[].content` = a PLAIN STRING (full prompt with lyrics inline)
- `stream: true` — REQUIRED (non-stream errors with "Audio output requires stream: true")
- `modalities: ["text", "audio"]` — harmless, sometimes needed
- Audio arrives in the SSE stream as `choices[].delta.audio.data` (base64)

### Prompt structure

- Describe genre/mood/instruments/vocal + dynamic arc up front
- Use `[Intro]`, `[Verse 1]`, `[Chorus]`, `[Bridge]`, `[Outro]` tags
- Put YOUR lyrics under the tags so the model sings your words
- Say "Around 2 minutes" / "3-minute song" to control duration
- The response text gives timed lyrics (e.g. `[15.0:] line text`) — save these; Mode C needs the timings

### Run it

```bash
python3 scripts/generate_song.py "lyrics_prompt.txt" song.mp3
```

See `scripts/generate_song.py` — it calls the API, reads the stream,
extracts `delta.audio.data`, and writes the MP3.

### Verify

```bash
ffprobe -v error -show_format -show_streams song.mp3 2>&1 | grep -E "codec_name|sample_rate|channels=|duration=|bit_rate="
```
Expect: `codec_name=mp3`, 44100 Hz, stereo, ~192 kbps.

---

## Mode C — Build the storyboard video

### Step 1 — Extract section timings from the song

The song response's timed lyrics tell you when each section starts.
Map them to frames. Example from a 178s song:

```json
[
  {"name": "intro",      "start": 0,   "duration": 15, "prompt": "..."},
  {"name": "verse1",     "start": 15,  "duration": 30, "prompt": "..."},
  {"name": "chorus1",    "start": 45,  "duration": 30, "prompt": "..."},
  {"name": "verse2",     "start": 75,  "duration": 30, "prompt": "..."},
  {"name": "bridge",     "start": 105, "duration": 24, "prompt": "..."},
  {"name": "chorus2",    "start": 129, "duration": 30, "prompt": "..."},
  {"name": "finalverse", "start": 159, "duration": 15, "prompt": "..."},
  {"name": "outro",      "start": 174, "duration": 5,  "prompt": "..."}
]
```

Durations must sum to ~song length.

### Step 2 — Write one image prompt per section

Each prompt should match the section's mood AND its lyrics:
- Verse = the specific scene described in those words
- Chorus = the wide emotional landscape
- Bridge = the shift / close-up / detail
- End every prompt with `16:9 widescreen` (frames come out 1376×768)

### Step 3 — Generate the frames

```bash
python3 scripts/generate_frames.py storyboard.json frames_dir/
```

Uses Nano Banana 2 Lite. Saves `00-name.jpg`, `01-name.jpg`, etc.
Costs ~$0.034/frame.

### Step 4 — Stitch + mux with ffmpeg

```bash
bash scripts/build_video.sh frames_dir/ song.mp3 output.mp4 \
  "optional,comma,separated,poem,lines"   # text overlay (or empty string)
```

- Gives each frame a slow Ken Burns zoom (zoompan) so it feels like film
- Concatenates segments, muxes the song audio, trims to audio length
- Optional: if a comma-separated poem/lyric string is passed, renders it
  as centered text over the images (one line per section, `drawtext`)
- Output: H.264 1280×720 + AAC audio, duration = song length

### Verify the video

```bash
ffprobe -v error -show_format -show_streams output.mp4 2>&1 | grep -E "codec_name|codec_type|width|height|duration=|sample_rate|channels="
```
Expect: `h264` video + `aac` audio, ~178s, 1280×720.

---

## Pitfalls

- **Structured content array returns no audio.** Plain string + stream:true is the magic combo.
- **Audio tokens without audio field** = you used the wrong format. `usage.completion_tokens_details.audio_tokens > 0` proves audio was generated even when the wrapper dropped it.
- **Don't pipe curl to python3** — the security scanner blocks it. Write scripts to files and run them.
- **SSE keepalive lines** starting with `:` are comments — skip them before JSON.parse.
- **Costs are real**: song $0.08, image ~$0.034, clip $0.04. State the estimate before generating; confirm spend with the user first.
- **Lyria routes through Google AI Studio only** — no fallback routing.
- **JSON storyboard files can't have comments** — write valid JSON.
- Frame durations must sum to the song length or the video will cut early/late (`-shortest` trims to audio).

## File layout

- `scripts/generate_song.py` — Lyria call + MP3 extraction
- `scripts/generate_frames.py` — Nano Banana batch image generation
- `scripts/build_video.sh` — ffmpeg Ken Burns stitch + audio mux + text overlay

## Related skills

- `songwriting-and-ai-music` — lyric craft, structure, Suno prompts (the craft applies to Lyria too)
- `eight-essentials-curriculum` — source material for poem themes (Silence, Nature, etc.)
