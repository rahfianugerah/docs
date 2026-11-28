---
name: <agent-name, kebab-case, the same as the file name>
description: <One line: what the agent does, and the event that launches it.>
tier: <deep, build, or fast>
tools: <The smallest set from read, search, edit, run, web>
---
## Job
<One or two sentences: the single job, and what done looks like.>
## Read first
<The rule files it follows, by file name, and the brief fields it relies on; nothing more.>
## Do
<Numbered steps in order, ending with the report and the closing JSON.>
## Never
<The lines it must not cross: a path outside its brief, a push, grading its own work.>
## Ask the advisor when
<The hard-to-reverse or ambiguous decisions it takes to advisor. Delete this heading for a deep agent.>
## Output
<The report path pattern, then one JSON object and nothing after it: status, report, summary, next.>
