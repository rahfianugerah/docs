---
tags:
  - kind/pattern
  - layer/infra
  - topic/deploy
---

# PowerShell redirection corrupts every file that is read verbatim

> [!danger]
> A plain `>` in PowerShell writes a byte order mark, and on Windows PowerShell 5.1 often writes UTF-16LE. Any file whose bytes are consumed literally is then wrong, and each case fails far from its cause.

- **A secret value written with `>`** aborts the revision before the container runs, with a message about non-UTF8 data. There is no application log at all.
- **A tag pointer file written with `>`** gains an invisible leading character, and the failure appears much later as an image that cannot be found.

Write these with .NET instead, which emits no byte order mark and no trailing newline, then check the byte count before uploading:

```powershell
[System.IO.File]::WriteAllText("$PWD\value.txt", $v, (New-Object System.Text.UTF8Encoding($false)))
(Get-Item value.txt).Length
```

**The byte count identifies the fault without printing the value.** A hex-32 secret is exactly 64 bytes and a base64 256-bit key exactly 44. A byte order mark adds three, a newline one or two.

The same class of problem hits git on Windows. With automatic line-ending conversion on and no `.gitattributes`, a checkout rewrites a shell script to CRLF, the shebang gains a carriage return, and the platform reports the interpreter as missing for a script that is plainly present. **Pin `*.sh`, the container definition, the web server config, and the ignore file to `eol=lf` in `.gitattributes`.** Only a manual upload of the working tree is affected; a trigger clones LF from the remote.

**Why:** every one of these reports a symptom that points at the wrong file. The secret error names the secret rather than the shell that wrote it, and the interpreter error names the script rather than its first line, so the natural response is to inspect the container definition, which is not wrong.

**Applies to:** any deploy run from a Windows machine, and any file whose bytes are consumed literally rather than parsed.

**Source:** an incident outside this repository. This is shell behaviour, not application code; confirm it by checking the byte count of a file written with a plain redirect.

## Related

- [[deploy.cloud.md]]
- [[secret.rules.md]]
- [[docs.rules.md]]
- [[deploy-steps-come-from-the-project-own-runbook-in-both-shells.pattern.md]]
