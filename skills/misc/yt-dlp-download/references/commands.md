# yt-dlp command recipes

Run each recipe in one shell invocation with the chosen inputs. Replace placeholders with the user's URL and destination; quote arguments as data. These are CLI recipes, not a separate downloader.

## Choose inputs

```bash
media_url='URL'
media_root="$HOME/Downloads/sourcesget"
audio_format=m4a
auth_args=(--no-cookies --no-cookies-from-browser)
```

Use the user's directory when specified. `audio_format` is the requested output format, such as m4a or mp3. The default auth arguments prevent browser and cookie-file access for public content while leaving unrelated yt-dlp settings alone.

When authorized content needs login, replace the auth array with `auth_args=(--no-cookies --cookies-from-browser chrome)`, or the browser specified by the user. Use the same choice for inspection and download. If that access fails, report it. Never print cookie contents.

## Inspect

```bash
yt-dlp "${auth_args[@]}" \
  --no-playlist --dump-single-json --flat-playlist \
  -- "$media_url"
```

Interpret the result before choosing a download recipe. `--no-playlist` can select the video in a video-plus-playlist URL, but a pure collection still returns entries. If the user explicitly wants that playlist, inspect with `--yes-playlist` instead. Use a bounded `--playlist-end` preview when appropriate, noting that it is not a total count. Flat entries may lack duration or full metadata.

## Single video

Use only after the intended single item is established. The first-item guard is not permission to choose an item from an unresolved collection.

```bash
mkdir -p "$media_root"
yt-dlp "${auth_args[@]}" \
  --no-playlist --playlist-items 1 \
  --download-archive "$media_root/.download-archive-video.txt" \
  --no-overwrites --newline --no-simulate --print after_move:filepath \
  -P "$media_root" \
  -o 'video/%(title).200B [%(id)s].%(ext)s' \
  -f 'bv*+ba/b' \
  -- "$media_url"
```

The format selector requests the best available video and audio, falling back to a combined format. ffmpeg is needed when separate streams must be merged. Check the actual output path and media streams.

## Single audio

```bash
mkdir -p "$media_root"
yt-dlp "${auth_args[@]}" \
  --no-playlist --playlist-items 1 \
  --download-archive "$media_root/.download-archive-audio-${audio_format}.txt" \
  --no-overwrites --newline --no-simulate --print after_move:filepath \
  -P "$media_root" \
  -o "audio/${audio_format}/%(title).200B [%(id)s].%(ext)s" \
  -x --audio-format "$audio_format" \
  -- "$media_url"
```

Separate archives let the same media be requested in different formats. Separate format folders also protect an existing M4A when an MP3 conversion uses an M4A source as an intermediate. Keep the video folder separate and verify the final format with ffprobe when necessary.

Do not use the old shared `.download-archive-audio.txt` for new format-specific decisions, and do not delete or rewrite it. Existing legacy files can be reused when their actual format matches the request; their old location does not need to be changed.

## Selected collection

Set `media_items` to the user-confirmed selection, for example `1,3,5-7`. Use `1:` only when the user explicitly requested all items. Inspection and the user's scope decision come first.

```bash
: "${media_items:?Set the user-confirmed selection first}"
mkdir -p "$media_root"
yt-dlp "${auth_args[@]}" \
  --yes-playlist --playlist-items "$media_items" \
  --download-archive "$media_root/.download-archive-video.txt" \
  --no-overwrites --newline --no-simulate --print after_move:filepath \
  -P "$media_root" \
  -o 'video/%(title).200B [%(id)s].%(ext)s' \
  -f 'bv*+ba/b' \
  -- "$media_url"
```

For collection audio, use the single-audio recipe with `--no-playlist --playlist-items 1` replaced by `--yes-playlist --playlist-items "$media_items"`. Keep its target-format archive and folder. When the user asks only to list a collection, stop after inspection.

## Existing files and recovery

An archive records media IDs, not whether a requested file still exists. After a skip, locate and verify the actual file before reporting success. If the correct file already exists, return its location.

If the authorized item is recorded but its matching file is missing, repeat just that selected scope with `--no-download-archive` instead of the archive option. Keep `--no-overwrites`, the same format, and the same selection. Leave the existing archive intact. Do not broaden the download to repair one missing item.

If a site is unsupported, access fails, or postprocessing does not produce the requested format, return a short error and the actual partial outcome. ffprobe can inspect saved files with `ffprobe -v error -show_streams -show_format -of json FILE`.
