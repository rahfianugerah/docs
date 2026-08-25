---
tags:
  - kind/rule
  - topic/security
---

> Up: [[README.md]]

# Code Security Standard

## Core Requirement

Code is audited against the **OWASP Secure Coding Practices** checklist below. The checklist is technology-agnostic: map each control to whatever language, framework, and platform the code actually uses.

This file is both the standard and the review prompt. Hand it to a reviewer, human or model, and it produces the same audit either way.

## Operating Rules

> [!warning]
> Review for what the code can be made to do, not only what it is intended to do. Assume any action not specifically denied is allowed.

- **Plan first.** Before touching or changing anything, produce a review plan: the files and modules to inspect, the control categories in scope, and the order of work. Wait for explicit approval. Do not write or modify code before approval.
- **Report, do not silently fix.** For each finding, output the control ID, file and line, severity (Critical / High / Medium / Low), the concrete problem, and a remediation recommendation. Apply fixes only after the plan is approved.
- **Evidence over assumption.** Cite the exact code that triggered each finding. If a control cannot be verified from the code alone, such as server or infrastructure configuration, flag it as "needs verification" rather than passing or failing it.
- **The server is the trust boundary.** Treat every client, and every system outside direct control, as untrusted. Client-side validation, hidden fields, and UI controls carry no security value on their own.
- **Threat model mindset.** Review for what the code *can be made to do*, not only what it is intended to do. Assume any action not specifically denied is allowed.

## Severity Guidance

Rate by impact and exploitability, not by category. Injection, broken authentication, broken access control, secrets in code, and missing transport encryption are Critical or High by default unless context clearly reduces the risk.

## Review Checklist

### 1. Input Validation

- Perform all validation on a trusted system (the server), never relying on the client.
- Identify every data source and classify it as trusted or untrusted; validate all data from untrusted sources, including databases, file streams, and external APIs.
- Route input through a centralized validation routine rather than ad-hoc per-call checks.
- Specify explicit character sets, such as UTF-8, for all input sources.
- Canonicalize input to a common character set *before* validating.
- Reject input on any validation failure; fail closed.
- If UTF-8 extended character sets are supported, validate *after* UTF-8 decoding completes.
- Validate all client-provided data before processing: parameters, URLs, and HTTP headers including cookie names and values, plus automated postbacks from JavaScript or embedded code.
- Verify header values in both requests and responses contain only ASCII characters.
- Validate data arriving from redirects, since an attacker can submit content directly to the redirect target and bypass earlier validation.
- Validate the expected data type.
- Validate the data range.
- Validate the data length.
- Validate against an allow-list of permitted characters wherever possible.
- If hazardous characters must be allowed, add compensating controls: output encoding, task-specific APIs, and downstream-use accounting. Common hazardous characters are `< > " ' % ( ) & + \ \' \"`.
- Where the standard routine cannot cover them, check discretely for null bytes (`%00`), newline characters (`%0d`, `%0a`, `\r`, `\n`), and path traversal sequences (`../`, `..\`, and encoded forms such as `%c0%ae%c0%ae/`), using canonicalization to defeat double encoding and obfuscation.

### 2. Output Encoding

- Perform all encoding on a trusted system (the server).
- Use a standard, tested routine for each type of outbound encoding.
- Contextually output-encode all data returned to the client that originated outside the trust boundary. HTML entity encoding is one example, not a universal answer.
- Encode all characters unless they are known safe for the target interpreter.
- Contextually sanitize all untrusted output sent into SQL, XML, and LDAP queries.
- Sanitize all untrusted output sent into operating system commands.

### 3. Authentication and Password Management

- Require authentication for all pages and resources except those explicitly public.
- Enforce all authentication controls on the server.
- Use standard, tested authentication services wherever possible.
- Centralize all authentication controls, including wrappers around external services.
- Segregate authentication logic from the requested resource, redirecting to and from the centralized control.
- Ensure authentication controls fail securely.
- Make administrative and account management functions at least as secure as primary authentication.
- Store only cryptographically strong, one-way, salted password hashes, and make the credential store writable only by the application. Avoid MD5.
- Implement password hashing on the server.
- Validate authentication data only after all input is complete, especially for multi-page authentication.
- Use identical, non-revealing failure responses ("Invalid username and/or password"), identical in both display and source.
- Authenticate connections to external systems involving sensitive information or functions.
- Encrypt credentials for external services and store them in a protected location on a trusted system, never in source code.
- Transmit authentication credentials only via HTTP POST.
- Send non-temporary passwords only over encrypted connections or as encrypted data.
- Enforce password complexity per policy or regulation.
- Enforce password length per policy or regulation; 8 or more is common, 16 or more and pass phrases are better.
- Obscure password entry on screen.
- Disable accounts after a set number of failed logins, long enough to deter brute force but not to enable denial of service.
- Apply account-creation-level controls to password reset and change operations.
- Ensure reset questions allow sufficiently random answers.
- For email-based resets, send only to a pre-registered address with a temporary link or password.
- Give temporary passwords and links short expiration times.
- Force a change of temporary passwords on next use.
- Notify users when a password reset occurs.
- Prevent password re-use.
- Require passwords to be at least one day old before change, to deter re-use cycling.
- Enforce password changes per policy, and control reset intervals administratively.
- Disable "remember me" for password fields.
- Report last account use, successful or not, at the next successful login.
- Monitor for attacks spraying one password across many accounts, which bypasses per-account lockout.
- Change or disable all vendor-supplied default passwords and user IDs.
- Re-authenticate before critical operations.
- Use multi-factor authentication for highly sensitive or high-value accounts.
- If using third-party authentication code, inspect it for malicious content.

### 4. Session Management

- Use the server or framework session management controls, and accept only those session identifiers as valid.
- Create session identifiers only on the server.
- Use well-vetted algorithms producing sufficiently random session identifiers.
- Set the cookie domain and path for authenticated session cookies to an appropriately restricted value.
- Fully terminate the session and connection on logout.
- Make logout available on every authenticated page.
- Set a short inactivity timeout, balanced against business need; rarely more than a few hours.
- Disallow persistent logins, and enforce periodic termination even for active sessions on sensitive applications.
- If a session existed before login, close it and establish a new session after successful login.
- Generate a new session identifier on any re-authentication.
- Do not allow concurrent logins with the same user ID.
- Never expose session identifiers in URLs, error messages, or logs; keep them in the HTTP cookie header only.
- Protect server-side session data with appropriate access controls.
- Periodically rotate the session identifier and invalidate the old one.
- Generate a new session identifier when connection security changes from HTTP to HTTPS; prefer consistent HTTPS throughout.
- Use per-session strong random tokens for sensitive server-side operations, as a CSRF defense.
- Use per-request strong random tokens for highly sensitive or critical operations.
- Set the `Secure` attribute on cookies sent over TLS.
- Set `HttpOnly` on cookies unless client-side scripts specifically need them.

### 5. Access Control

- Base authorization decisions only on trusted server-side objects, such as the server-side session.
- Use a single site-wide component for authorization checks, including wrappers around external services.
- Ensure access controls fail securely.
- Deny all access if the application cannot reach its security configuration.
- Enforce authorization on every request, including server-side includes, scripts, and asynchronous calls.
- Segregate privileged logic from other application code.
- Restrict access to files and resources, including those outside direct control, to authorized users.
- Restrict access to protected URLs to authorized users.
- Restrict access to protected functions to authorized users.
- Restrict direct object references to authorized users.
- Restrict access to services to authorized users.
- Restrict access to application data to authorized users.
- Restrict access to the user and data attributes and policy information used by access controls.
- Restrict access to security-relevant configuration to authorized users.
- Ensure server-side enforcement and the presentation layer's representation of access rules match.
- If client-stored state is unavoidable, use encryption and server-side integrity checking to catch tampering.
- Enforce application logic flows against business rules.
- Rate-limit transactions per user or device above business need but low enough to deter automation.
- Use the `Referer` header only as a supplemental check, never as the sole authorization control, since it is spoofable.
- For long sessions, periodically re-validate authorization; on a privilege change, log the user out and force re-authentication.
- Audit accounts and disable unused ones, for example 30 days past password expiration.
- Support disabling accounts and terminating sessions when authorization ceases.
- Grant least privilege to service and external-connection accounts.
- Maintain an access control policy documenting business rules, data types, and authorization criteria.

### 6. Cryptographic Practices

- Implement all cryptographic functions protecting secrets on the server.
- Protect master secrets from unauthorized access.
- Ensure cryptographic modules fail securely.
- Generate all random numbers, file names, GUIDs, and strings intended to be unguessable with the crypto module's approved random number generator.
- Use FIPS 140-2 or equivalent compliant cryptographic modules.
- Establish and follow a key management policy and process.

### 7. Error Handling and Logging

- Do not disclose sensitive information, such as system details, session identifiers, or account information, in error responses.
- Use error handlers that suppress debugging and stack trace output.
- Use generic error messages and custom error pages.
- Handle errors in the application rather than relying on server configuration.
- Free allocated memory properly when errors occur.
- Make security-control error logic deny access by default.
- Implement all logging on a trusted system (the server).
- Log both success and failure of specified security events.
- Ensure logs contain important event data: timestamp, severity, security tag, account identity, source IP, outcome, and description.
- Ensure untrusted data in log entries cannot execute as code in the log viewer, defending against log injection.
- Restrict log access to authorized individuals.
- Use a master routine for all logging.
- Never store sensitive information, such as system details, session identifiers, or passwords, in logs.
- Ensure a mechanism exists for log analysis.
- Log all input validation failures.
- Log all authentication attempts, especially failures.
- Log all access control failures.
- Log all apparent tampering, including unexpected state-data changes.
- Log attempts to use invalid or expired session tokens.
- Log all system exceptions.
- Log all administrative functions, including security configuration changes.
- Log all backend TLS connection failures.
- Log cryptographic module failures.
- Use a cryptographic hash to validate log entry integrity.

### 8. Data Protection

- Implement least privilege, restricting users to only the functionality, data, and system information their tasks require.
- Protect cached and temporary copies of sensitive data on the server, and purge them as soon as they are no longer needed.
- Encrypt highly sensitive stored data, such as authentication verification data, even server-side, using vetted algorithms.
- Protect server-side source code from download.
- Never store passwords, connection strings, or sensitive data in clear text or in an insecure client-side format.
- Remove comments in user-accessible production code that reveal backend or sensitive details.
- Remove unnecessary application and system documentation that could aid an attacker.
- Do not put sensitive information in HTTP GET parameters.
- Disable autocomplete on forms containing sensitive information, including authentication.
- Disable client-side caching on pages with sensitive information, using `Cache-Control: no-store` plus `Pragma: no-cache` for HTTP/1.0.
- Support removal of sensitive data when it is no longer required.
- Apply appropriate access controls to sensitive server-side data, including cached data and temporary files.

### 9. Communication Security

- Encrypt transmission of all sensitive information, using TLS for the connection plus discrete encryption where needed.
- Ensure TLS certificates are valid, correctly named, unexpired, and installed with intermediate certificates.
- Do not let failed TLS connections fall back to insecure connections.
- Use TLS for all authenticated access and all other sensitive information.
- Use TLS for external-system connections involving sensitive information or functions.
- Use a single, correctly configured, standard TLS implementation.
- Specify character encodings for all connections.
- Filter sensitive parameters out of the HTTP `Referer` when linking externally.

### 10. System Configuration

- Run the latest approved versions of servers, frameworks, and components.
- Apply all patches issued for the versions in use.
- Turn off directory listings.
- Restrict web server, process, and service accounts to least privilege.
- Fail securely when exceptions occur.
- Remove all unnecessary functionality and files.
- Remove test code and non-production functionality before deployment.
- Prevent directory-structure disclosure in `robots.txt` by isolating non-public directories under one parent and disallowing that parent.
- Define which HTTP methods the application supports and how they differ per page.
- Disable unnecessary HTTP methods, and protect any required file-handling methods with vetted authentication.
- Configure HTTP 1.0 and 1.1 handling consistently, or understand the differences.
- Strip unnecessary operating system, server version, and framework details from HTTP response headers.
- Make the security configuration store output in human-readable form to support auditing.
- Implement an asset management system and register components and software in it.
- Isolate development environments from the production network, granting access only to authorized groups.
- Implement a change-control system to manage and record code changes in development and production.

### 11. Database Security

- Use strongly typed parameterized queries.
- Apply input validation and output encoding including meta-characters, and do not run the command if these fail.
- Ensure variables are strongly typed.
- Access the database with the lowest possible privilege level.
- Use secure database credentials.
- Never hard-code connection strings; store them encrypted in a separate configuration file on a trusted system.
- Use stored procedures to abstract data access and allow removing base-table permissions.
- Close database connections as soon as possible.
- Remove or change all default database administrator passwords, and use strong passwords or multi-factor authentication.
- Turn off unnecessary database functionality to reduce the surface area.
- Remove default vendor content, such as sample schemas.
- Disable default accounts not required by business needs.
- Connect with different credentials for each trust distinction: user, read-only, guest, administrator.

### 12. File Management

- Never pass user-supplied data directly to a dynamic include function.
- Require authentication before allowing file upload.
- Limit uploadable file types to those needed for business purposes.
- Validate uploaded file type by inspecting file headers, not the extension alone.
- Do not save uploaded files in the application's web context; use a content server or a database.
- Prevent or restrict upload of any file the web server could interpret or execute.
- Turn off execution privileges on upload directories.
- Implement safe uploading on UNIX via a mounted logical drive or a chroot.
- When referencing existing files, use an allow-list of names and types, rejecting or defaulting on a mismatch.
- Never pass user-supplied data into a dynamic redirect; if unavoidable, accept only validated relative-path URLs.
- Do not pass directory or file paths; use index values mapped to a predefined path list.
- Never send absolute file paths to the client.
- Ensure application files and resources are read-only.
- Scan user-uploaded files for viruses and malware.

### 13. Memory Management

- Apply input and output control for untrusted data.
- Verify the buffer is as large as specified.
- With byte-count copy functions such as `strncpy()`, remember equal source and destination sizes may leave the string non-NULL-terminated.
- Check buffer boundaries in loops to avoid writing past allocated space.
- Truncate input strings to a reasonable length before copy or concatenation.
- Close resources explicitly rather than relying on garbage collection, including connections and file handles.
- Use non-executable stacks where available.
- Avoid known-vulnerable functions such as `printf`, `strcat`, and `strcpy`.
- Free allocated memory at function completion and at every exit point.

### 14. General Coding Practices

- Prefer tested, approved managed code over new unmanaged code for common tasks.
- Use task-specific built-in APIs for operating system tasks; never issue commands directly to the operating system, especially through a command shell.
- Use checksums or hashes to verify the integrity of interpreted code, libraries, executables, and configuration files.
- Use locking or synchronization to prevent race conditions and simultaneous-request hazards.
- Protect shared variables and resources from inappropriate concurrent access.
- Explicitly initialize all variables and data stores at declaration or before first use.
- When running with elevated privileges, raise them as late as possible and drop them as soon as possible.
- Understand the language's numeric representation to avoid calculation errors: byte size, precision, signed and unsigned, truncation, casting, NaN, overflow and underflow.
- Never pass user-supplied data to a dynamic execution function.
- Restrict users from generating new code or altering existing code.
- Review all secondary applications, third-party code, and libraries for business necessity and safe functionality.
- Implement safe updating: sign code cryptographically, verify signatures on the client, and transfer over encrypted channels.

## Output Format

Produce, after the plan is approved:

1. **Summary**: counts by severity and by control category.
2. **Findings**: a table with columns: Control Category, File:Line, Severity, Issue, Recommendation.
3. **Needs verification**: controls that cannot be confirmed from source alone: infrastructure, configuration, runtime.
4. **Passed**: controls verified as satisfied, listed briefly for coverage assurance.

## Stack Controls

These extend the checklist above rather than replacing it. Where a control here and a checklist item cover the same ground, the concrete one here is the one to follow, because it names the library and the failure this stack actually produces.

### Secrets and Configuration

- Store secrets only in an environment file or a secret manager. Never hardcode a secret in source code, a compose file, or a web UI form. [[secret.rules.md]] decides which values go to a secret manager and which are plain environment variables.
- `.env` stays gitignored. `.env.example` lists every required variable with a placeholder value, never a real one.
- **Fail fast:** an app refuses to start when a required secret is empty or still set to its default. Do not let it run silently with a weak value.
- Treat any secret that was ever committed as leaked. Rotate it; removing it from the file is not enough.
- Never enable a debug mode in production.

### HTTP Surface

- Disable the interactive API docs and the OpenAPI schema in production, or require authentication for them.
- Configure CORS with an explicit origin list. Never use `*`.
- Apply rate limiting to the login endpoint and to any other sensitive one. Store lockout state in a shared store, such as a database or cache. Never store it only in the memory of a single worker.
- Require authentication on every upload endpoint.
- Bind services to `127.0.0.1` on the host, behind a reverse proxy. Never bind a database to `0.0.0.0`.
- Terminate TLS at the proxy and serve every host over HTTPS.
- Set `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` or an equivalent CSP directive, and `Referrer-Policy` on responses.
- Serve a Content Security Policy. Start from `default-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'`, and widen it only for a source the app genuinely loads. A CSP is the last line of defence when an XSS bug reaches production.
- **Never use `unsafe-inline` or `unsafe-eval` in a CSP.** They remove most of what the policy is for.
- Send `Strict-Transport-Security` on every HTTPS response.

### Untrusted Input

Anything that arrives from outside the process is untrusted: a request body, a query parameter, a path parameter, a header, a cookie, an uploaded file and its name, a webhook payload, a model response, and any value read back from another service's API. Trusted means written by this codebase, not sent by your own frontend.

- Validate at the boundary with a Pydantic v2 model, per [[api.rules.md]]. Never read a raw `dict` out of a request and pass it into logic.
- Set `model_config = ConfigDict(extra="forbid")` on a request model, so an unexpected field is rejected rather than silently ignored.
- **Never bind a request body straight onto an ORM model.** Declare an explicit input schema listing only the fields a client may set, or a client will eventually set `role`, `is_admin`, or `tenant_id` on a record it does not own.
- Bound every string with a maximum length and every number with a range. An unbounded string is a memory and storage problem before it is a security one.
- Validate on the server even when the same rule already runs in the browser. Client-side validation is a convenience for the user, never a control.
- Reject rather than repair. Do not strip characters and continue; a value that fails validation returns a `422`, per [[api.rules.md]].
- Never build a regular expression from user input, and keep app-side patterns free of nested quantifiers, which can be driven into catastrophic backtracking.

### Files and Paths

These extend [[media.rules.md]], which owns the upload feature itself.

- **Never build a filesystem path from a client-supplied name.** Generate a new server-side name, such as a UUID, and store the original name as a label only.
- Reject a path segment containing `..`, a leading separator, a null byte, or an absolute path, and resolve the final path to confirm it is still inside the intended directory.
- Determine the file type from its content, not from its extension or its `Content-Type` header.
- Serve an upload with `Content-Disposition: attachment` and a non-executable content type, so an uploaded HTML or SVG file cannot run in the app's own origin.
- Store uploads outside the web root, and require authentication on the endpoint that serves them.

### Command Execution, Deserialization, and Templates

- **Never pass user input to a shell.** Use an argument list and never `shell=True`; a shell is what turns a filename into a command.
- **Never deserialize untrusted data with `pickle`, `yaml.load`, or an equivalent.** Use JSON, or `yaml.safe_load`. `pickle` executes arbitrary code, which makes a downloaded model file a remote code execution vector; prefer `safetensors` or a JSON format.
- Never build a template from user input. A user value is passed to a template as data, never concatenated into the template source.
- Never let a request name a module, a class, or a function to import or call.

### Dependencies

- Pin dependencies and commit the lock file, so a build is reproducible and a compromised release cannot arrive silently, per [[stacks.rules.md]].
- Run a vulnerability audit as part of CI, and treat a high-severity finding in a direct dependency as a blocker.
- Prefer a maintained library over a hand-rolled implementation for anything cryptographic, and never write your own password hashing, token signing, or encryption.

### API Keys Between Services

- Scope every key with a `resource:action` format, for example `report:read` or `user:read`. A key must only be able to perform what it is scoped for.
- Issue one key per client. Never share a single global key across every client, so each key can be revoked and audited independently.
- Send the key in an `X-API-Key` header. Store only its hash on the receiving side where possible.
- Never issue a key with full administrative access.

### SQL Injection

> [!danger]
> A user value that reaches SQL as text rather than as a bound parameter is an injection, whatever built the string. This is the single highest-cost prohibition here, because one such line reads the whole database.

The stack runs SQLAlchemy 2.x on PostgreSQL, per [[stacks.rules.md]]. Used normally it is safe; the failures come from stepping around it.

Build queries with the ORM expression API, which parameterizes automatically:

```python
stmt = select(User).where(User.email == email)          # correct
```

When raw SQL is genuinely required, use `text()` with bound parameters, never string formatting:

```python
db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})   # correct
db.execute(text(f"SELECT * FROM users WHERE email = '{email}'"))                 # forbidden
```

- The rule covers every way a string is joined: an f-string, `%`, `.format()`, `+`, and `str.join`. If a user value reaches SQL text rather than a parameter dictionary, it is an injection.
- **An identifier cannot be bound.** A table name, a column name, a sort column, and a sort direction that come from a request are matched against an allowlist in code, and anything not on the list is rejected:

```python
SORT_COLUMNS = {"name": User.name, "created_at": User.created_at}
column = SORT_COLUMNS.get(sort_by)
if column is None:
    raise HTTPException(422, "Unknown sort column")
```

- `LIMIT` and `OFFSET` are integers validated to a range, never interpolated text. Cap the page size, per [[api.rules.md]].
- Escape `%`, `_`, and `\` in a value used inside a `LIKE` or `ILIKE` pattern. Unescaped, a user's `%` turns a prefix search into a full scan, which is a denial of service on a large table. See [[search.component.md]] for the search path itself.
- Never let a request choose a raw SQL fragment, a `WHERE` clause, or a JSON path expression, however convenient the filter API becomes.
- Grant the app's database role only what it needs. It does not need superuser, and it does not need `DROP` on tables it only reads.

### Cross-Site Scripting

React escapes text by default, so an XSS bug in this stack almost always comes from one of a small number of deliberate escapes from that default.

- **Never use `dangerouslySetInnerHTML`.** If rendering stored HTML is genuinely required, sanitize it with a maintained sanitizer at render time, and record the deviation in the project README.
- Never write to `innerHTML`, `outerHTML`, `document.write`, or `insertAdjacentHTML` with a value that is not a literal in the source.
- Never pass a user value to `eval`, `new Function`, `setTimeout` with a string body, or a dynamic `import()` of a user-supplied path.
- Validate any URL before putting it in `href` or `src`. Allow `http:` and `https:` only, so `javascript:`, `data:`, and `vbscript:` cannot execute. This applies to a link stored in the database as much as to one typed in a form.
- **Never build a highlighted search result by concatenating HTML around the matched text.** Split the string and render the parts as children, so the user's own query cannot become markup. This is the most likely XSS in an app that has a search box, per [[search.component.md]].
- Never inject a server value into an inline `<script>` block or into a global state assignment on `window`. Send it through the API as JSON.
- Set `Content-Type: application/json` on every JSON response and never `text/html`, so a reflected value cannot be rendered as a document.
- Treat a model response as untrusted input. It is generated from data a person typed, so it can carry markup or a prompt aimed at whatever renders it. Never render it as HTML.

### Authorization and Object Access

Authentication says who is calling. Authorization says whether that caller may touch this specific row, and it is the control most often missing.

- Check ownership or entitlement on every object read, update, and delete, not only on the endpoint. An authenticated user changing an `id` in a URL must not reach another user's record.
- **Scope the query itself rather than fetching and then comparing.** `where(Document.id == id, Document.tenant_id == user.tenant_id)` cannot leak a row that a later `if` might forget to check.
- Never rely on an unguessable identifier as the control. A UUID is not an authorization decision.
- Enforce the role check on the server. Hiding a button in the frontend is presentation, not a permission.
- Return the same `404` for a record that does not exist and for one the caller may not see, so the API does not confirm that a record exists.
- Apply the same checks to an export, a report, a bulk endpoint, and a search. A filter enforced on the list endpoint and forgotten on the export is a data leak, and it is the failure [[search.component.md]] requires one shared filter function to prevent.

### Cross-Site Request Forgery

Sessions are `HttpOnly` cookies, per [[auth.rules.md]], so the browser attaches them to a cross-site request automatically. Cookie auth without a CSRF control is exploitable.

- Set `SameSite=Lax` at minimum on the session cookie, plus `Secure` and `HttpOnly`. Use `SameSite=Strict` where the app never needs to be entered from an external link.
- Add a CSRF token, checked on every state-changing request, when any flow requires `SameSite=None`.
- **Never perform a state change on a `GET`.** A `GET` that deletes something is exploitable through an image tag.
- Keep the CORS origin list explicit, as above. `Access-Control-Allow-Credentials: true` combined with a reflected origin is equivalent to having no origin check at all.

### Redirects and Outbound Requests

- Validate every redirect target against an allowlist of known app origins. A `next` parameter in a login flow is the live example: unchecked, it turns a trusted login URL into a redirect to an attacker's page that looks like it came from the product.
- Never redirect to a target taken from a request without that check, including one taken from the `Referer` header.
- Validate every URL the server itself fetches. A user-supplied URL must not be able to reach `localhost`, a private range, or a cloud metadata address, which is how an internal service gets read from outside.
- Give every outbound request a timeout and a size cap.

## Personal Data

Personal data means anything that identifies a person: a name, a national identity number, a bank account, a phone number, an email address, a location, a photograph of a face. Most data protection law treats it the same way, and the rules below satisfy the common core rather than any one statute.

- **Redact personal data before it reaches a model or a memory layer.** Extract text first, redact the extracted text, then send it. Raw bytes cannot be redacted.
- Use a provider whose region satisfies the project's obligations, and record that choice in the README.
- **Log access to personal data:** who accessed it, what data, and when. This is mandatory for any project holding employee or customer records.
- Minimize collection. Do not store or log personal data that is not required, and never write it into application logs.
- Store confidential material only in the memory scope reserved for it. Never expose it to a general recall scope, per [[memory.rules.md]].
- A model can memorize its training data. Know that before publishing weights trained on anything private.

## Audit Trail

- Log important actions, such as a login, a failed login, a configuration change, and a destructive action, together with the acting identity and a timestamp.
- **Any write action performed by a model requires a confirmation flow and an audit trail** recording who approved it.
- An audit entry is append-only. A record that can be edited by the same role it audits is not an audit trail.

## Python and Machine Learning Notes

The checklist is technology-agnostic. These are where this stack maps onto it most often.

| Control | What it means here |
| :- | :- |
| 1, 11 | Never build SQL with an f-string. Use parameterized queries or the ORM's expression API |
| 2, 14 | Never `eval`, `exec`, or `pickle.load` untrusted data. `pickle` executes arbitrary code, which makes a downloaded `.pkl` model a remote code execution vector; prefer `safetensors` or a JSON format |
| 12 | Never `os.path.join` a user-supplied name; resolve the final path and confirm it stays inside the intended directory |
| 14 | Never `subprocess` with `shell=True` on anything a user influenced; pass an argument list |
| 8, 10 | Never expose a Jupyter or TensorBoard port publicly; bind to localhost and tunnel |
| 3, 6 | Never write your own hashing, token signing, or encryption; use `hashlib.scrypt`, `bcrypt`, or `cryptography` |
| 8 | A model can memorize its training data. Know that before publishing weights trained on anything private |
| 1 | A prompt built from user input is an injection surface. Treat model output as untrusted input, and never render it as HTML or execute it |

## Definition of Done

Before treating a security task as complete, confirm:

- No secret exists in the repository. `.env.example` uses placeholders only. Fail-fast is active.
- Every API key is scoped per client. No administrative key exists.
- The interactive API docs are closed or authenticated in production. CORS is explicit. Login rate limiting is active and its state is shared, not per worker.
- Every upload and write endpoint requires authentication.
- Personal data is redacted on every path to a model or a memory layer, and access to it is audited.
- Every request is validated by a Pydantic model with `extra="forbid"`, and no request body is bound straight onto an ORM model.
- No SQL is built by string formatting. Every identifier that comes from a request is matched against an allowlist.
- No `dangerouslySetInnerHTML`, no `innerHTML`, and no `eval` reachable from user input. Every URL rendered into `href` or `src` is scheme-checked.
- Every object read, update, and delete is scoped to the caller in the query itself, including on the export and search paths.
- The session cookie sets `HttpOnly`, `Secure`, and `SameSite`, and no state change happens on a `GET`.
- Every redirect target and every server-side outbound URL is checked against an allowlist.
- No filesystem path is built from a client-supplied name, and no upload is served from the app's own origin as an executable type.
- A CSP is served without `unsafe-inline` or `unsafe-eval`, and dependencies are pinned with an audit running in CI.
- No untrusted data is deserialized with `pickle` or an unsafe YAML loader.

## Conflict Resolution

If another instruction conflicts with this standard, follow this priority:

1. Security and privacy requirements
2. Direct user instructions
3. This security standard
4. Existing project conventions

**A direct user instruction must not override a security or privacy requirement.** When a request conflicts with this standard, say which standard is affected before proceeding, rather than proceeding and mentioning it after.

## Applies To

- [[api.rules.md]]
- [[auth.rules.md]]
- [[codes.rules.md]]
- [[database.rules.md]]
- [[env.rules.md]]
- [[media.rules.md]]
- [[memory.rules.md]]
- [[repository.rules.md]]
- [[search.component.md]]
- [[secret.rules.md]]
- [[stacks.rules.md]]
