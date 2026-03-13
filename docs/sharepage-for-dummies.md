# Sharing “the exact page I’m on” without leaking your soul

This is harder than it sounds.

## The real problems

- pages are JS + API calls, not static HTML
- POST requests exist
- sessions/cookies exist
- the thing you want to share might contain private data

## WARC to the rescue (kind of)

WARC is a web-archive format that can store request/response pairs.

This repo provides:

```
dasharepage capture https://example.com/
```

This uses `wget --warc-file ...` and produces a `.warc.gz`.

## Warnings

If you’re logged in:
- you might capture private data
- you might capture session-only content
- sharing the archive can leak PII or authenticated state

Treat WARC files as sensitive unless you *know* the capture is public.

## Replay

To replay a WARC like a website you generally need tools like:
- `pywb` (Python Webrecorder)
- ReplayWeb.page / Webrecorder ecosystem

This repo does not vendor those.
