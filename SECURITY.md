# Security policy

## Supported versions

Security fixes are provided for the latest released minor version until a newer policy is announced.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting for `benedictdavon/eclipse-harness`. Do not include credentials, production data, or active exploit details in a public issue. Include the affected version, reproduction conditions, impact, and a minimal proof when safe.

## Security model

Eclipse treats repository files, issue content, fixtures, generated output, external documents, and worker output as untrusted context. They cannot override user/host/harness authority or grant credentials, network access, destructive actions, external effects, targets, or additional write scope.

The reference policy denies implicit network, credential, external-effect, destructive-action, and scope authority. Contract validators reject probable secrets, path traversal, contradictory evidence, unsupported route claims, and unsafe parallel-wave ownership. Host enforcement varies; `eclipse doctor` reports each host's desired, configured, and effective/unverified capability separately.

Review [docs/security.md](docs/security.md) for the threat model and operational guidance.
