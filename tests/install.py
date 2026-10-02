"""설치·제거·업데이트 검사. 실제 사용자 설정이나 GitHub는 변경하지 않는다."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parents[1]


def run(args, cwd, env, ok=True):
    result = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True)
    assert (result.returncode == 0) == ok, result.stdout + result.stderr
    return result.stdout.strip()


with tempfile.TemporaryDirectory(prefix="djfi install ") as directory:
    root = Path(directory).resolve()
    repo = root / "source repo"
    shutil.copytree(SOURCE, repo, symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    home = root / "test home"
    binary = root / "bin"
    binary.mkdir()
    for name in ("claude", "codex"):
        executable = binary / name
        executable.write_text("#!/bin/sh\nexit 0\n")
        executable.chmod(0o755)
    env = {**os.environ, "DJFI_HOME": str(home), "PATH": str(binary) + os.pathsep + os.environ["PATH"]}
    claude = home / ".claude/skills/dont-just-fix-it"
    codex = home / ".agents/skills/dont-just-fix-it"
    run(["./install.sh", "--check"], repo, env)
    assert not home.exists()
    run(["./install.sh"], repo, env)
    assert claude.resolve() == codex.resolve() == repo / "skills/dont-just-fix-it"
    run(["./install.sh"], repo, env)  # idempotent
    run(["./uninstall.sh"], repo, env)
    assert not claude.is_symlink() and not codex.is_symlink()
    run(["./install.sh", "--claude-only"], repo, env)
    assert claude.is_symlink() and not codex.is_symlink()
    run(["./uninstall.sh", "--claude-only"], repo, env)
    run(["./install.sh", "--codex-only"], repo, env)
    assert codex.is_symlink() and not claude.is_symlink()
    run(["./uninstall.sh"], repo, env)
    codex.mkdir()
    (codex / "user.txt").write_text("keep")
    run(["./install.sh"], repo, env, ok=False)
    assert not claude.exists()  # conflict preflight prevents partial installation
    run(["./uninstall.sh"], repo, env)
    assert (codex / "user.txt").read_text() == "keep"
    (codex / "user.txt").unlink()
    codex.rmdir()
    codex.symlink_to(root / "missing foreign target")
    run(["./install.sh"], repo, env, ok=False)
    run(["./uninstall.sh"], repo, env)
    assert codex.is_symlink()
    codex.unlink()
    for args in (["--unknown"], ["--claude-only", "--codex-only"], ["--check", "--uninstall"]):
        run(["./install.sh", *args], repo, env, ok=False)

    # A local Git remote tests real fast-forward updates without network access.
    remote = root / "remote.git"
    run(["git", "init", "--bare", str(remote)], repo, env)
    run(["git", "init", "-b", "main"], repo, env)
    run(["git", "add", "."], repo, env)
    commit = ["git", "-c", "user.name=Install Test", "-c", "user.email=test@example.invalid", "commit", "-m"]
    run([*commit, "initial"], repo, env)
    run(["git", "remote", "add", "origin", str(remote)], repo, env)
    run(["git", "push", "-u", "origin", "main"], repo, env)
    installed = root / "installed repo"
    run(["git", "clone", "-b", "main", str(remote), str(installed)], repo, env)
    run(["./install.sh", "--codex-only"], installed, env)
    previous_head = run(["git", "rev-parse", "HEAD"], installed, env)
    previous_skill = (codex / "SKILL.md").read_bytes()
    with (repo / "skills/dont-just-fix-it/SKILL.md").open("a") as skill:
        skill.write("\nUpdated skill\n")
    (repo / "release-note.txt").write_text("new release")
    run(["git", "add", "release-note.txt", "skills/dont-just-fix-it/SKILL.md"], repo, env)
    run([*commit, "next"], repo, env)
    run(["git", "push"], repo, env)
    assert "새 커밋: 1" in run(["./update.sh", "--check"], installed, env)
    assert not (installed / "release-note.txt").exists()
    claude.mkdir()
    (claude / "user.txt").write_text("keep")
    run(["./update.sh"], installed, env, ok=False)
    assert run(["git", "rev-parse", "HEAD"], installed, env) == previous_head
    assert (codex / "SKILL.md").read_bytes() == previous_skill
    assert (claude / "user.txt").read_text() == "keep"
    assert not (installed / "release-note.txt").exists()
    (claude / "user.txt").unlink()
    claude.rmdir()
    run(["./update.sh", "--codex-only"], installed, env)
    assert (installed / "release-note.txt").read_text() == "new release"
    assert codex.resolve() == installed / "skills/dont-just-fix-it"
    assert (codex / "SKILL.md").read_bytes() != previous_skill
    (installed / "local.txt").write_text("keep local work")
    run(["./update.sh"], installed, env, ok=False)
    assert (installed / "local.txt").read_text() == "keep local work"
    (installed / "local.txt").unlink()
    run(["git", "switch", "--detach"], installed, env)
    run(["./update.sh"], installed, env, ok=False)
    run(["./uninstall.sh"], installed, env)
    assert not codex.is_symlink()
    print("PASS: install, target selection, idempotency, ownership, conflicts, spaces, check, update preflight, dirty/detached guards")
