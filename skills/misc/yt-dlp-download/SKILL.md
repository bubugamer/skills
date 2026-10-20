---
name: yt-dlp-download
description: Download or inspect user-specified video and audio with yt-dlp. Use for explicit requests to save media, extract audio, inspect a media URL, or list and select playlist items. A bare URL alone does not request a download. Article reading, image downloads, and transcription use other workflows.
---

# yt-dlp Download

Use the existing yt-dlp CLI directly. Read [commands.md](references/commands.md) for inspection, video, audio, and collection recipes; keep downloads within the user's requested scope.

## Resolve the request

Establish the referenced URL, download versus inspection, media type, target format, destination, and any collection selection. Use existing context and preferences rather than asking for decisions already made.

Inspect the URL before downloading. Distinguish a single item, a video with a playlist parameter, and a collection. Flat metadata can omit duration or other fields; report those as unknown. For large collections, use a bounded preview and make its limits clear.

For a collection, use the user's selected items or explicit request for all. If the range is still unspecified, show a compact list and ask for it. Do not silently choose the first item. `--no-playlist` only resolves certain video-plus-playlist URLs; it is not a general collection-size limit. The single-item recipes add `--playlist-items 1` as a scope guard after the intended item is established.

## Preserve preferences and existing files

Use the user's destination, otherwise `$HOME/Downloads/sourcesget`. Group video under `video/` and audio under `audio/<target-format>/`; include title and media ID, and preserve existing files with `--no-overwrites`. Leave old directories and download archives intact.

Use M4A for audio unless another format is requested. Give each target audio format its own archive and output folder. A prior M4A download must not satisfy an MP3 request or be deleted while making it. Check for a usable file in the requested format before treating an archive skip as completion; the reference describes a narrow recovery when the file is missing.

## Tools and access

Check for yt-dlp before inspecting or downloading. Check for ffmpeg when extraction, conversion, or stream merging needs it. Report missing tools; install only when the user requests installation.

Try public content without browser cookies. For content that needs the user's authorized login, use the browser they specified or the existing Chrome preference. Keep the selected access method consistent between inspection and download. If access fails, explain the failure and stop rather than treating unavailable content as downloaded.

## Verify and report

Inspect the resulting files, not just the command's exit code. Check existence, requested media type and format, selected item count, and preservation of prior files. Use ffprobe when needed to distinguish audio, video, and codec/container details.

Report what succeeded, what was already present, and what failed, with actual file links or locations. An inspection-only request returns information without saving media. Keep the reply brief and use the conversation's language.
