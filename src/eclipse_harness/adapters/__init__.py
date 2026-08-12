"""Host-specific generated wrappers around the vendor-neutral core."""

from .base import AdapterArtifact, install_artifacts
from .codex import CodexAdapter
from .copilot import CopilotAdapter

__all__ = ["AdapterArtifact", "CodexAdapter", "CopilotAdapter", "install_artifacts"]
