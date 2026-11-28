# Trigger Setup

One runner per project and trigger, kept in `~/.agentic-outer/`, outside every repository. A schedule starts the runner; the runner starts at most one `/agentic-orchestrate` run, in its own worktree, on its own local branch.

## The Headless Command

The flags below were checked against `claude --help` and `claude -p --help` (Claude Code 2.1.317). Check them again after an update.

```text
claude -p "<prompt>" --output-format stream-json --verbose --max-budget-usd <limit> --permission-mode acceptEdits --permission-prompts none --disallowedTools "Bash(git push *)" "Bash(gh pr *)" "Bash(git merge *)"
```

| Flag | Why |
| :- | :- |
| `-p` | Non-interactive: runs the prompt and exits. It skips the workspace trust dialog, so run it only in the owner's own repositories |
| `--output-format stream-json --verbose` | The transcript, one JSON event per line, which `python scripts/harness/usage.py` turns into tokens per agent and per tier |
| `--max-budget-usd <limit>` | The budget limit: the run stops once it is spent |
| `--permission-mode acceptEdits` | File edits proceed. Commands still need the allow list in the project's settings, so put the test command there |
| `--permission-prompts none` | Anything that would ask is denied, since nobody is there to answer |
| `--disallowedTools ...` | Denies push, pull request, and merge whatever the settings allow. Drop one only when the owner allowed it in this trigger's setup |

- **The turn limit is a time limit.** This version lists no turn-limit flag, so the scheduler enforces wall-clock time: `ExecutionTimeLimit` in Task Scheduler, `timeout` in cron. If a later `claude -p --help` lists a turn-limit flag, add it to the runner.
- Never `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, or `--permission-mode bypassPermissions`.
- Another tool runs the same way through its own non-interactive mode, with the same two limits, once its `--help` confirms the flags.

## The Runner, PowerShell

Save as `~/.agentic-outer/<project>-<trigger>.ps1`, and fill in the values in angle brackets.

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\<you>\<project>'; $project = '<project>'; $trigger = 'schedule'; $base = 'main'; $budgetUsd = '5'
$request = '<the request this trigger carries>'
$out = "$HOME\.agentic-outer"; New-Item -ItemType Directory -Force "$out\logs" | Out-Null
$seenFile = "$out\$project-$trigger.seen"; $seen = @(if (Test-Path $seenFile) { Get-Content $seenFile })
Set-Location $repo

# A poller trigger pastes its block here: it sets $request, or returns when there is nothing new.

$request = $request -replace '"', "'"
$stamp = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([datetime]::UtcNow, 'SE Asia Standard Time').ToString('yyyyMMdd-HH_mm_ss')
$branch = "outer/$trigger-$stamp"; $tree = "$repo-outer-$stamp"
$prompt = "/agentic-orchestrate Project: $project. Trigger: $trigger. Request: $request This run is unattended: stop at any gate with a Needs Decision report. Never push, open a pull request, or merge. End with the local branch $branch and a report."
$claudeArgs = @('-p', $prompt, '--output-format', 'stream-json', '--verbose', '--max-budget-usd', $budgetUsd, '--permission-mode', 'acceptEdits', '--permission-prompts', 'none', '--disallowedTools', 'Bash(git push *)', 'Bash(gh pr *)', 'Bash(git merge *)')
if ($DryRun) { "git worktree add -b $branch $tree $base"; "claude $($claudeArgs -join ' ')"; return }
git worktree add -b $branch $tree $base
Set-Location $tree
$log = "$out\logs\$project-$trigger-$stamp.jsonl"; $lines = claude @claudeArgs
[IO.File]::WriteAllLines($log, [string[]]$lines)
Set-Location "$HOME\agentic"; python scripts/harness/usage.py $log --label "outer-$project-$trigger-$stamp"
```

The `-replace` line keeps a double quote in a comment or an alert from splitting the prompt into several arguments, which Windows PowerShell 5.1 does to native commands. `WriteAllLines` saves the transcript without the byte order mark `Out-File` adds, which the usage script would not parse.

## The Runner, Bash

Save as `~/.agentic-outer/<project>-<trigger>.sh`, and make it executable.

```bash
#!/usr/bin/env bash
set -euo pipefail
repo="$HOME/<project>"; project="<project>"; trigger="schedule"; base="main"; budget_usd=5
request="<the request this trigger carries>"
out="$HOME/.agentic-outer"; mkdir -p "$out/logs"; seen_file="$out/$project-$trigger.seen"; touch "$seen_file"
dry_run=false; [ "${1:-}" = "--dry-run" ] && dry_run=true
cd "$repo"

# A poller trigger pastes its block here: it sets request, or exits 0 when there is nothing new.

stamp=$(TZ=UTC-7 date +%Y%m%d-%H_%M_%S)
branch="outer/$trigger-$stamp"; tree="$repo-outer-$stamp"
prompt="/agentic-orchestrate Project: $project. Trigger: $trigger. Request: $request This run is unattended: stop at any gate with a Needs Decision report. Never push, open a pull request, or merge. End with the local branch $branch and a report."
args=(-p "$prompt" --output-format stream-json --verbose --max-budget-usd "$budget_usd" --permission-mode acceptEdits --permission-prompts none --disallowedTools "Bash(git push *)" "Bash(gh pr *)" "Bash(git merge *)")
if $dry_run; then echo "git worktree add -b $branch $tree $base"; echo "claude ${args[*]}"; exit 0; fi
git worktree add -b "$branch" "$tree" "$base"
cd "$tree"
log="$out/logs/$project-$trigger-$stamp.jsonl"; claude "${args[@]}" > "$log"
cd "$HOME/agentic" && python scripts/harness/usage.py "$log" --label "outer-$project-$trigger-$stamp"
```

## Schedule

No poller. The request is fixed in the runner, such as "Run the full test suite and fix what fails". Pick a time when the machine is on and the owner is not working in the same repository.

## CI Failure

Poll the CI the project already has; never add one. Only failures on the default branch start a run, since the run branches from it. PowerShell:

```powershell
$runs = gh run list --status failure --branch main --limit 5 --json databaseId,displayTitle | ConvertFrom-Json
$new = $runs | Where-Object { "$($_.databaseId)" -notin $seen } | Select-Object -First 1
if (-not $new) { return }
if (-not $DryRun) { Add-Content $seenFile "$($new.databaseId)" }
$request = "Find the root cause of failed CI run $($new.databaseId), $($new.displayTitle), and fix it. Read the failure with: gh run view $($new.databaseId) --log-failed"
```

For Cloud Build, read the failures with `gcloud builds list --filter="status=FAILURE" --limit=5 --format=json`, key on each build's `id`, and point the request at `gcloud builds log <id>`. The event goes into the seen file before the run starts, so a run that crashes is not retried in a loop.

## Issue or Pull Request Comment

A comment starts a run only when the owner wrote it and it begins with `/agentic`. Anyone else's comment is ignored: on a public repository it is untrusted text that would otherwise spend the owner's budget. PowerShell:

```powershell
$login = '<the owner GitHub login>'
$since = (Get-Date).ToUniversalTime().AddHours(-1).ToString('yyyy-MM-ddTHH:mm:ssZ')
$comments = gh api "repos/{owner}/{repo}/issues/comments?since=$since" | ConvertFrom-Json
$new = $comments | Where-Object { $_.user.login -eq $login -and $_.body.StartsWith('/agentic') -and "$($_.id)" -notin $seen } | Select-Object -First 1
if (-not $new) { return }
if (-not $DryRun) { Add-Content $seenFile "$($new.id)" }
$text = $new.body.Substring(8).Trim(); $text = $text.Substring(0, [Math]::Min(500, $text.Length))
$request = "Do what the owner's comment at $($new.html_url) asks: $text"
```

- The issue comments endpoint covers pull request conversations too, since a pull request is an issue to it.
- The run never replies on the issue: a comment is a write to a hosted service, made only when the owner allowed it in this setup.
- Poll at least as often as the `since` window, one hour above, or comments are missed.

## Error Alert

Poll the log source the project already has, and start at most one run per cooldown window, six hours by default, however many errors arrive. The request carries the query, never the log text, which can hold personal data. PowerShell, for a Cloud Run service:

```powershell
$cooldownHours = 6
$last = if ($seen) { [datetime]$seen[-1] } else { [datetime]::MinValue }
if (((Get-Date) - $last).TotalHours -lt $cooldownHours) { return }
$query = 'severity>=ERROR AND resource.labels.service_name=<service>'
$entries = gcloud logging read $query --freshness=30m --limit=50 --format=json | ConvertFrom-Json
if (-not $entries) { return }
if (-not $DryRun) { Add-Content $seenFile (Get-Date -Format o) }
$request = "Find the root cause of the $(@($entries).Count) errors logged in the last 30 minutes, readable with: gcloud logging read '$query' --freshness=30m --limit=50, and fix it."
```

Any other alert source works the same way: a read-only check command, a cooldown, and a request that points at the source.

## Install

Show the owner the command, and run it only after a yes.

**Windows Task Scheduler**, in PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy RemoteSigned -File `"$HOME\.agentic-outer\<project>-<trigger>.ps1`""
$when = New-ScheduledTaskTrigger -Daily -At 2am
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName 'agentic-outer-<project>-<trigger>' -Action $action -Trigger $when -Settings $settings
```

A poller repeats instead: `$when = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)`. Remove a task with `Unregister-ScheduledTask -TaskName 'agentic-outer-<project>-<trigger>' -Confirm:$false`.

**cron**, one line in `crontab -e`:

```text
0 2 * * * timeout 2h flock -n /tmp/agentic-outer-<project>-<trigger>.lock "$HOME/.agentic-outer/<project>-<trigger>.sh" >> "$HOME/.agentic-outer/logs/<project>-<trigger>.log" 2>&1
```

`timeout` is the time limit, and `flock -n` skips a start while the last run still holds the lock. A poller runs every 30 minutes with `*/30 * * * *`. Remove the line to remove the trigger.

## Reviewing a Run

- The result is the branch `outer/<trigger>-<stamp>` in the worktree `<repo>-outer-<stamp>`, and a report in `~/agentic/report/<project>/`. The run's transcript is in `~/.agentic-outer/logs/`, and its token log in `harness/usage/`.
- The owner reads the report, then merges or discards the branch. Remove the worktree after: `git worktree remove <repo>-outer-<stamp>`.

## Hosted Workflow, Only on Request

Written only when the owner asks for one in so many words, since the owner allows no hosted CI and no billable service by default. Where they do:

- It runs the same headless command, with the same budget and time limits.
- The key lives in the host's secret store, never in the workflow file.
- It gets read-only repository permission, unless the owner granted a push in this setup.
- A hosted runner leaves no local branch behind, so its branch and report are uploaded as the run's artifact unless the owner granted a push.
