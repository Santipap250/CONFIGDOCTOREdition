#!/usr/bin/env python3
"""Safely test, commit, push, and open a PR for the Landing Elite changes.

Requires Python 3.10+, Git, pytest, and an already-authenticated GitHub CLI (gh).
This script never stores GitHub credentials and never pushes from a default branch.
Run from the repository: python3 scripts/commit_push_pr.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_TITLE = "feat: add Premium Elite landing page"
DEFAULT_BODY = """## Summary
- Install the Premium Elite Landing stylesheet in both static asset locations.
- Preserve dynamic tool/group counts and existing Landing workflows.
- Add Landing regression tests.

## Validation
- `pytest -q`
- `git diff --check`

Production is not deployed by this script."""
REQUIRED_FILES = [
    "static/css/landing-elite.css",
    "public/static/css/landing-elite.css",
    "templates/landing.html",
    "tests/test_landing_elite.py",
]
PROTECTED_BRANCHES = {"main", "master", "production", "prod"}


class WorkflowError(RuntimeError):
    pass


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None,
        capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("\n$ " + " ".join(command), flush=True)
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if check and result.returncode != 0:
        details = (result.stderr or result.stdout or "").strip() if capture else ""
        raise WorkflowError(f"Command failed ({result.returncode}): {' '.join(command)}" + (f"\n{details}" if details else ""))
    return result


def find_repo_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise WorkflowError("Run this script from inside a Git working tree with Git installed.") from exc
    return Path(result.stdout.strip()).resolve()


def parse_github_repo(remote_url: str) -> str:
    match = re.search(r"github\.com(?::|/)([^/]+)/([^/]+?)(?:\.git)?$", remote_url.strip(), re.IGNORECASE)
    if not match:
        raise WorkflowError("Could not identify a GitHub OWNER/REPO from the origin URL. Check the origin remote without sharing embedded credentials.")
    return f"{match.group(1)}/{match.group(2)}"


def git_config(root: Path, key: str) -> str:
    result = run(["git", "config", "--get", key], cwd=root, capture=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def confirm_or_exit(args: argparse.Namespace, *, branch: str, base: str,
                    repo: str, files: list[str]) -> None:
    print("\nPlanned GitHub operation")
    print(f"  Repository: {repo}")
    print(f"  Push branch: {branch}")
    print(f"  PR base: {base}")
    print(f"  Commit: {args.commit_message}")
    print(f"  PR title: {args.title}")
    print("  Files to stage:")
    for item in files:
        print(f"    - {item}")
    if args.dry_run:
        print("\nDry run complete. No files were staged; no commit, push, or PR was created.")
        return
    if args.yes:
        return
    if not sys.stdin.isatty():
        raise WorkflowError("Non-interactive run requires --yes. No commit, push, or PR was performed.")
    answer = input("\nContinue with commit, push, and PR creation? [y/N] ").strip().lower()
    if answer not in {"y", "yes"}:
        raise WorkflowError("Cancelled by user. No commit, push, or PR was performed.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Test, commit, push, and open a GitHub PR for Landing Elite.")
    parser.add_argument("--base", default="main", help="PR base branch (default: main)")
    parser.add_argument("--repo", help="PR target OWNER/REPO; defaults to the origin repository")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Pull request title")
    parser.add_argument("--body", default=DEFAULT_BODY, help="Pull request body")
    parser.add_argument("--commit-message", default=DEFAULT_TITLE, help="Git commit message")
    parser.add_argument("--yes", action="store_true", help="Skip the final interactive confirmation")
    parser.add_argument("--dry-run", action="store_true", help="Run checks and show the plan, but do not stage or publish")
    args = parser.parse_args()

    try:
        root = find_repo_root()
        if not args.dry_run:
            if not shutil.which("gh"):
                raise WorkflowError("GitHub CLI `gh` is required. Install it and authenticate separately; this script will not store credentials.")
            run(["gh", "auth", "status", "--hostname", "github.com"], cwd=root)

        branch = run(["git", "branch", "--show-current"], cwd=root, capture=True).stdout.strip()
        if not branch:
            raise WorkflowError("Detached HEAD detected. Switch to a named feature branch first.")
        if branch.lower() in PROTECTED_BRANCHES:
            raise WorkflowError(f"Refusing to commit or push from protected/default branch '{branch}'. Switch to a feature branch first.")

        remote_url = run(["git", "remote", "get-url", "origin"], cwd=root, capture=True).stdout.strip()
        origin_repo = parse_github_repo(remote_url)
        target_repo = args.repo or origin_repo
        if not re.fullmatch(r"[^/\s]+/[^/\s]+", target_repo):
            raise WorkflowError("--repo must be in OWNER/REPO form.")
        owner = origin_repo.split("/", 1)[0]
        pr_head = branch if target_repo.casefold() == origin_repo.casefold() else f"{owner}:{branch}"

        ref_check = run(["git", "check-ref-format", "--branch", args.base], cwd=root, check=False)
        if ref_check.returncode != 0:
            raise WorkflowError(f"Invalid base branch name: {args.base}")

        files = list(REQUIRED_FILES)
        script_path = Path(__file__).resolve()
        try:
            script_rel = script_path.relative_to(root).as_posix()
            if script_rel not in files:
                files.append(script_rel)
        except ValueError:
            print("Note: script is outside the repository; it will not be included in the commit.")

        missing = [item for item in REQUIRED_FILES if not (root / item).is_file()]
        if missing:
            raise WorkflowError("Missing expected Landing Elite files: " + ", ".join(missing))

        # Fetch the destination branch and refuse to publish a branch that is behind it.
        # Dry-run does not update any remote refs; no automatic merge or rebase is performed.
        if target_repo.casefold() == origin_repo.casefold():
            if args.dry_run:
                print(f"Dry run: would fetch origin/{args.base} and verify the feature branch contains it.")
            else:
                refspec = f"+refs/heads/{args.base}:refs/remotes/origin/{args.base}"
                run(["git", "fetch", "--no-tags", "origin", refspec], cwd=root)
                ancestry = run(["git", "merge-base", "--is-ancestor", f"origin/{args.base}", "HEAD"], cwd=root, check=False)
                if ancestry.returncode != 0:
                    raise WorkflowError(f"Current branch does not include origin/{args.base}. Rebase/merge the latest base manually, rerun tests, then retry.")
        else:
            print("Note: target repo differs from origin; automatic base-ancestry check is skipped.")

        if not args.dry_run and (git_config(root, "user.name") == "" or git_config(root, "user.email") == ""):
            raise WorkflowError("Git commit identity is not configured. Set user.name and user.email locally, then rerun; this script will not change Git configuration.")

        staged = run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False)
        if staged.returncode != 0:
            raise WorkflowError("The index already contains staged changes. Commit or unstage them first so this script cannot include unrelated work.")

        run(["git", "diff", "--check"], cwd=root)
        fd, test_db = tempfile.mkstemp(prefix="configdoctor-pr-", suffix=".sqlite3")
        os.close(fd)
        os.unlink(test_db)
        env = os.environ.copy()
        for key in ("DATABASE_URL", "POSTGRES_URL", "REDIS_URL"):
            env.pop(key, None)
        env["PYTHON_DOTENV_DISABLED"] = "1"
        env["DATABASE_PATH"] = test_db
        try:
            run([sys.executable, "-m", "pytest", "-q"], cwd=root, env=env)
        finally:
            try:
                os.unlink(test_db)
            except FileNotFoundError:
                pass

        confirm_or_exit(args, branch=branch, base=args.base, repo=target_repo, files=files)
        if args.dry_run:
            return 0

        run(["git", "add", "--", *files], cwd=root)
        cached = run(["git", "diff", "--cached", "--quiet"], cwd=root, check=False)
        if cached.returncode == 0:
            raise WorkflowError("No changes were staged. Confirm the Landing Elite files differ from the current branch.")
        run(["git", "diff", "--cached", "--check"], cwd=root)
        run(["git", "commit", "-m", args.commit_message], cwd=root)
        run(["git", "push", "--set-upstream", "origin", branch], cwd=root)

        prs = run([
            "gh", "pr", "list", "--repo", target_repo, "--head", pr_head,
            "--base", args.base, "--state", "open", "--json", "url",
        ], cwd=root, capture=True)
        existing = json.loads((prs.stdout or "").strip() or "[]")
        if existing:
            print(f"\nAn open PR already exists; pushed branch updated: {existing[0]['url']}")
            return 0

        created = run([
            "gh", "pr", "create", "--repo", target_repo, "--base", args.base,
            "--head", pr_head, "--title", args.title, "--body", args.body,
        ], cwd=root, capture=True)
        print("\nPull request created:")
        print((created.stdout or "").strip())
        return 0

    except WorkflowError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"\nERROR: Required command not found: {exc.filename}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"\nERROR: Command failed with exit code {exc.returncode}: {exc.cmd}", file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
