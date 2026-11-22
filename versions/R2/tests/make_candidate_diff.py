"""Write a repository-relative unified diff for the 18 approved Skill changes."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILLS = (
    "problem-parser", "method-selector", "workflow-orchestrator",
    "model-code-analyzer", "python-code-reviewer", "matlab-code-reviewer",
)
ROOTS = (".claude/skills", ".codex/skills", "plugins/mathmodeling-skills/skills")


def main():
    baseline, candidate, output = map(Path, sys.argv[1:4])
    chunks = []
    with tempfile.TemporaryDirectory(prefix="p11-diff-") as temp_dir:
        temp = Path(temp_dir)
        for root in ROOTS:
            for skill in SKILLS:
                rel = Path(root) / skill / "SKILL.md"
                before = temp / "baseline" / rel
                after = temp / "candidate" / rel
                before.parent.mkdir(parents=True, exist_ok=True)
                after.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(baseline / rel, before)
                shutil.copyfile(candidate / rel, after)
                command = ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "-C", str(temp), "diff", "--no-index", "--no-ext-diff", "--src-prefix=a/", "--dst-prefix=b/", "--", f"baseline/{rel.as_posix()}", f"candidate/{rel.as_posix()}"]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                if result.returncode not in (0, 1):
                    raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
                chunk = result.stdout.replace(b"a/baseline/", b"a/").replace(b"b/candidate/", b"b/")
                chunks.append(chunk)
    output.write_bytes(b"".join(chunks))


if __name__ == "__main__":
    main()
