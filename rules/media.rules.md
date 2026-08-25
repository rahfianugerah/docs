---
tags:
  - kind/rule
  - layer/backend
  - topic/security
---

> Up: [[README.md]]

# Upload and Media Standard Policy

> [!note]
> Document and media upload, covering PDF and photo handling across every app.

## Core Requirement

When building, modifying, or reviewing a document or media upload feature (PDF or photo) for a project, you must follow the rules in this policy.

Every upload is compressed while keeping usable quality. Disk and egress are both metered on any host worth deploying to, so an uncompressed upload path is a cost that grows with use and is never noticed until the bill. Compression must not come at the cost of security or of consistency between projects.

## Security Prerequisites

These are not negotiable and apply before any compression logic.

- Require authentication on every upload endpoint. An open upload endpoint is not allowed.
- Allowlist file types explicitly: `pdf`, `jpg`/`jpeg`, `png`, `webp`. Add a new type only when a real need exists, and add it explicitly rather than opening the allowlist broadly.
- Validate the file by its content, using magic bytes, not by its extension or its `Content-Type` header alone. An attacker controls both of those.
- Enforce a request size limit, 10 MB by default, configurable through an environment variable.
- Generate the stored filename on the server, using a UUID or a hash. Never use the original filename from the user, since that allows path traversal. The original filename may still be kept as metadata.
- Store uploaded files on a volume, never inside the application image or the repository. Serve them only through an authenticated endpoint. Never expose an upload folder directly to the public, and never let it execute a file.

## Photo Compression

The server always re-encodes an uploaded photo. Re-encoding also normalizes the file and strips any unexpected payload.

| Aspect | Standard |
| :- | :- |
| Storage format | WebP as the primary choice, or JPEG, at quality 80 to 85, which stays visually lossless for a document or receipt photo |
| Maximum dimension | 2000 px on the longest side, enough to read a receipt or a field photo. Resize anything larger |
| Metadata | Strip EXIF data. This is mandatory, since EXIF can carry GPS location, which counts as personal data under every data protection law worth naming, Indonesia's UU PDP and the GDPR included |
| Thumbnail | Generate a thumbnail around 300 px for list views, to save bandwidth |
| Library | `Pillow` in Python, `sharp` in Node.js |

Client-side compression, for example with `browser-image-compression`, is allowed as a bandwidth optimization, but the server must still re-encode the file. The server is the final authority on what gets stored.

## PDF Compression

| PDF type | Treatment |
| :- | :- |
| Scanned PDF containing images | Downsample images to 150 dpi, JPEG quality around 80. The goal is text that stays sharp and readable |
| Digital or text-based PDF | Usually already small. Compress the structure only, without downsampling |
| Any result larger than the original | Keep the original file. Compression must never make a file larger |

- Use `pikepdf` or `qpdf` for structural compression, and Ghostscript at the `/ebook` setting, about 150 dpi, for a scanned PDF.
- Verify the compressed file still opens correctly, and is not corrupted, before storing it.

## Storage Policy

- Store the compressed version as the primary copy. Do not keep the original file unless a specific app has a documented legal requirement to do so. When that requirement exists, record it in the app's README together with its retention policy.
- Record metadata for every file: original filename, MIME type, original size, stored size, SHA-256 hash, the uploader's identity, and an ISO 8601 timestamp, per [[api.rules.md]].
- Deduplicate by SHA-256 when the feature allows it, so the same file uploaded twice is stored once.

## Definition of Done

Before treating an upload feature as complete, confirm:

- The upload endpoint requires authentication, validates file type by magic bytes, and enforces a size limit.
- A photo is re-encoded to WebP or JPEG at quality 80 to 85, resized to a maximum of 2000 px, and stripped of EXIF data.
- A scanned PDF is compressed to about 150 dpi and stays readable, and no compressed file is larger than its original.
- Every file lives on a volume and is served only through an authenticated endpoint, with a server-generated filename.
- File metadata and its SHA-256 hash are recorded.

## Conflict Resolution

If another instruction conflicts with this policy, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This upload and media policy
4. Existing project conventions

A direct user instruction must not override security or privacy requirements. If a request conflicts with this policy, tell the user which standard is affected before proceeding.

## Applies To

- [[api.rules.md]]
- [[auth.rules.md]]
- [[security.rules.md]]
- [[secret.rules.md]]
- [[stacks.rules.md]]
