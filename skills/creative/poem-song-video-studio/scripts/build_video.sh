#!/bin/bash
# Build a storyboard music video: Ken Burns zoom on each frame, concat,
# mux song audio, optional poem-text overlay.
#
# Usage:
#   bash build_video.sh frames_dir/ song.mp3 output.mp4 \
#       "line one,line two,line three"   # text overlay (or "")
#
# frames_dir/ must contain 00-name.jpg, 01-name.jpg, ... in section order.
# Frame durations come from a parallel DURATIONS array — edit below to match
# your song's section timings.
set -euo pipefail

FRAMES_DIR="${1:?frames dir required}"
SONG="${2:?song mp3 required}"
OUT="${3:?output mp4 required}"
OVERLAY_TEXT="${4:-}"   # comma-separated lines, one per section; empty = no overlay

WORK_DIR="$(dirname "$OUT")/video-build-$(basename "$OUT" .mp4)"
FPS=25
mkdir -p "$WORK_DIR"

# Section durations (seconds) — MUST match your song's Lyria section timings.
# One per frame file in alphabetical order (00, 01, 02, ...).
DURATIONS=(15 30 30 30 24 30 15 5)

mapfile -t IMAGES < <(ls "$FRAMES_DIR"/*.jpg | sort)
if [ "${#IMAGES[@]}" -ne "${#DURATIONS[@]}" ]; then
  echo "ERROR: ${#IMAGES[@]} images but ${#DURATIONS[@]} durations" >&2
  exit 1
fi

# Step 1: Ken Burns zoom per segment
SEGMENTS=()
for i in "${!IMAGES[@]}"; do
  dur=${DURATIONS[$i]}
  frames=$((dur * FPS))
  seg="$WORK_DIR/seg$i.mp4"
  echo "==> Segment $i: $(basename "${IMAGES[$i]}") (${dur}s)"
  ffmpeg -y -loglevel error -i "${IMAGES[$i]}" \
    -filter_complex "zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${frames}:s=1280x720:fps=${FPS}" \
    -frames:v "$frames" -c:v libx264 -pix_fmt yuv420p -r "$FPS" "$seg"
  SEGMENTS+=("$seg")
done

# Step 2: concat
CONCAT="$WORK_DIR/concat.txt"
: > "$CONCAT"
for seg in "${SEGMENTS[@]}"; do
  echo "file '$seg'" >> "$CONCAT"
done
echo "==> Concatenating"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$CONCAT" -c copy "$WORK_DIR/silent.mp4"

# Step 3: optional text overlay (poem lines over the frames)
VIDEO_IN="$WORK_DIR/silent.mp4"
if [ -n "$OVERLAY_TEXT" ]; then
  echo "==> Adding text overlay"
  IFS=',' read -ra LINES <<< "$OVERLAY_TEXT"
  # Build one drawtext chain: each line appears on its own y position.
  FILTER=""
  y=520
  for line in "${LINES[@]}"; do
    escaped="${line//\'/\\\'}"
    FILTER="${FILTER}drawtext=text='${escaped}':fontcolor=white:fontsize=36:borderw=2:bordercolor=black@0.6:x=(w-text_w)/2:y=${y},"
    y=$((y + 50))
  done
  FILTER="${FILTER%,}"
  ffmpeg -y -loglevel error -i "$VIDEO_IN" -vf "$FILTER" -c:a copy "$WORK_DIR/overlay.mp4"
  VIDEO_IN="$WORK_DIR/overlay.mp4"
fi

# Step 4: mux audio, trim to song length
echo "==> Muxing audio"
ffmpeg -y -loglevel error -i "$VIDEO_IN" -i "$SONG" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"

echo "==> DONE: $OUT"
