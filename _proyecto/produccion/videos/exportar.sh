#!/bin/zsh
# Mezcla voz + música y exporta un video de la campaña a assets/video/ (H.264 + AAC, < 25 MB) con su póster.
# Uso: zsh exportar.sh <carpeta del video, ej. v01> <nombre de salida, ej. v01-trailer> <segundo del póster>
set -e
eval "$(/opt/homebrew/bin/brew shellenv)"
HERE=${0:A:h}; ROOT=${HERE:h:h:h}
SK=~/.claude/skills/editar-reels-claude
cd "$HERE/$1"
[ -f musica.wav ] || (cd "$SK/scripts" && node synthflow_render.cjs music lofi 40 "$HERE/$1/musica.wav")
"$SK/.venv/bin/python" "$SK/scripts/mix.py" --work . --music musica.wav --music-under 14 --video reel-video.mp4 --out _mezcla.mp4
ffmpeg -nostdin -v error -y -i reel-video.mp4 -i master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 22 -maxrate 5M -bufsize 10M \
  -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -shortest -movflags +faststart "$ROOT/assets/video/$2.mp4"
rm -f _mezcla.mp4
ffmpeg -nostdin -v error -y -ss "$3" -i "$ROOT/assets/video/$2.mp4" -frames:v 1 -q:v 3 "$ROOT/assets/video/poster-${1}.jpg"
ffprobe -v error -show_entries format=duration,size -of compact "$ROOT/assets/video/$2.mp4"
ffmpeg -nostdin -hide_banner -i "$ROOT/assets/video/$2.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
