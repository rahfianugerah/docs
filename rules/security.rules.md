> Up: [[README.md]]

# Code Security Standard

## Core Requirement

Code is audited against the **OWASP Secure Coding Practices** checklist below. The checklist is technology-agnostic: map each control to whatever language, framework, and platform the code actually uses.

This file is both the standard and the review prompt. Hand it to a reviewer, human or model, and it produces the same audit either way.

## Operating Rules

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

## Applies To

- [[codes.rules.md]]
- [[secret.rules.md]]
- [[env.rules.md]]
