# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |
| 0.x     | No        |

## Reporting a vulnerability

MinuteMosaic processes files you give it locally. The Python side is stdlib-only,
makes no network calls, and never executes anything it reads; the Swift side is
a local model and renderer. If you find a security issue — a crash or resource
exhaustion on hostile input, a path traversal, or a report that leaks transcript
content beyond the line it flags — please report it privately with GitHub's
"Report a vulnerability" button on the Security tab.
