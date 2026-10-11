---
name: yt-dlp-download
description: Use this skill when the user explicitly asks Codex to download, save, extract audio from, inspect, or list downloadable video or audio from a URL using yt-dlp. Trigger on requests such as "下载这个视频", "保存这个音频", "用 yt-dlp 下这个链接", "看看这个播放列表里有什么", or "download this media link". Do not trigger for general article reading, webpage summarization, image downloading, or when the user only pastes a URL without asking to download or inspect media.
---

# yt-dlp Download

Use this skill to turn an explicit video/audio download request into a safe, predictable `yt-dlp` workflow.

## What this skill does

- Download user-provided video or audio URLs with `yt-dlp`.
- Save files under `"$HOME/Downloads/sourcesget"` by default, grouped by media type instead of extractor name.
- Use Chrome browser cookies by default so logged-in sites can work when the user has access in Chrome.
- Avoid accidental bulk downloads by treating playlists and collections carefully.
- Report results in plain language: what was downloaded, where it was saved, and what failed if anything failed.

## Preconditions

Before downloading, check that these commands exist:

```bash
command -v yt-dlp
command -v ffmpeg
```

If either is missing, stop and tell the user what is missing. Do not install tools unless the user explicitly asks.

## Safety and consent

- Only download media from URLs the user provides or clearly references in the current conversation.
- Do not help bypass DRM, paywalls, access controls, or other restrictions.
- Do not run downloads when the user only pasted a URL without asking to download or inspect it.
- If the request is ambiguous, ask a short clarification before downloading.

## Default locations

Use this download root unless the user specifies another folder:

```text
"$HOME/Downloads/sourcesget"
```

Create it if needed. Use a filename template that includes the title and media id so duplicate titles do not overwrite each other. Do not include `%(extractor)s` in the output path; generic webpages otherwise create confusing folders named `generic`.

## Workflows

### Download best video and audio

Use this for a normal "download this video" request:

```bash
mkdir -p "$HOME/Downloads/sourcesget"
yt-dlp \
  --cookies-from-browser chrome \
  --no-playlist \
  --download-archive "$HOME/Downloads/sourcesget/.download-archive-video.txt" \
  --no-overwrites \
  --newline \
  -P "$HOME/Downloads/sourcesget" \
  -o "video/%(title).200B [%(id)s].%(ext)s" \
  -f "bv*+ba/b" \
  "URL"
```

Why: `--no-playlist` prevents accidental collection downloads, while `bv*+ba/b` asks for the best available video and audio.

### Extract audio only

Use this when the user asks for audio, music, mp3, m4a, podcast-style output, or "只要音频":

```bash
mkdir -p "$HOME/Downloads/sourcesget"
yt-dlp \
  --cookies-from-browser chrome \
  --no-playlist \
  --download-archive "$HOME/Downloads/sourcesget/.download-archive-audio.txt" \
  --no-overwrites \
  --newline \
  -P "$HOME/Downloads/sourcesget" \
  -o "audio/%(title).200B [%(id)s].%(ext)s" \
  -x --audio-format m4a \
  "URL"
```

Use `m4a` by default because it is broadly supported on macOS. Keep audio files under the `audio` subfolder so extracting audio never deletes or overwrites a previously downloaded video with the same title and id. If the user asks for `mp3`, use `--audio-format mp3`.

### Inspect a URL without downloading

Use this when the user asks what a link contains or wants details before downloading:

```bash
yt-dlp \
  --cookies-from-browser chrome \
  --dump-single-json \
  --flat-playlist \
  "URL"
```

Summarize only the useful fields: title, site, item count, duration when available, and whether it looks like a single item or a collection.

### Handle playlists and collections

For a URL that may be a playlist, channel, collection, course, or page with multiple media items:

1. First inspect it with `--dump-single-json --flat-playlist`.
2. If it contains multiple entries, do not download everything by default.
3. Show a compact numbered list with titles and ids when available.
4. Ask the user which item numbers to download, unless the user already asked to download all.
5. To download selected items, use `--playlist-items` with the user's selected range.

Example selected download:

```bash
yt-dlp \
  --cookies-from-browser chrome \
  --playlist-items "1,3,5-7" \
  --download-archive "$HOME/Downloads/sourcesget/.download-archive-video.txt" \
  --no-overwrites \
  --newline \
  -P "$HOME/Downloads/sourcesget" \
  -o "playlists/%(playlist_title).200B/%(playlist_index)s - %(title).200B [%(id)s].%(ext)s" \
  -f "bv*+ba/b" \
  "URL"
```

## Error handling

- If Chrome cookie extraction fails, retry without `--cookies-from-browser chrome` for public content, then report which attempt worked.
- If the site requires login and the cookie-based attempt fails, tell the user Chrome login access was not enough for this link.
- If the URL is unsupported, say that `yt-dlp` could not recognize it and include the short error line.
- If a file was skipped because it is already in the download archive, say it was already downloaded before.

## Final response style

Keep the final message short and plain:

- Say whether the download succeeded.
- Give the saved folder or file path.
- Mention any skipped or failed items.
- Avoid command details unless the user asks for them.
