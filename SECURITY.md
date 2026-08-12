# Security policy

## Supported versions

Security fixes are provided for the latest released minor version until a newer policy is announced.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting for `benedictdavon/eclipse-harness`. Do not include credentials, production data, or active exploit details in a public issue. Include the affected version, reproduction conditions, impact, and a minimal proof when safe.

## Security model

Eclipse treats repository files, issue content, fixtures, generated output, external documents, and worker output as untrusted context. They cannot override user/host/harness authority or grant credentials, network access, destructive actions, external effects, targets, or additional write scope.

The default policy denies network access, secrets in contracts, path traversal, symlink escape, run-state writes by workers, unverified route claims, destructive actions without human authority, and unsafe parallel writers. Host enforcement varies; `eclipse doctor` reports desired, configured, and effective/unverified capability separately.

Review [docs/security.md](docs/security.md) for the threat model and operational guidance.
