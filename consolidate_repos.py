#!/usr/bin/env python3
"""
consolidate_repos.py  (v2 — uses git filter-repo)

Merges multiple GitHub repos into a single monorepo, placing each source
repo's content into its own subdirectory with full history preserved.

Prerequisites:
    pip3 install git-filter-repo --break-system-packages
        OR
    brew install git-filter-repo

    gh auth login   # GitHub CLI, authenticated

Usage:
    python3 consolidate_repos.py
"""

import subprocess
import sys
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────────────

GITHUB_USER = "tazzledazzle"

CONSOLIDATIONS = {
    "devtools": [
        "cmake_to_bazel",
        "maple-rewrite",
        "codebase-health-monitor",
        "code-helper",
        "personal-copilot",
    ],
    "cloud-infra": [
        "datadog-terraform",
        "eks-alb-external-dns-autoscaler",
        "block-tor-exit-nodes",
        "sweet-security-autopilot-sensor",
    ],
    "backend-services": [
        "cloud-native-microservices",
        "rideshare-backend",
        "spa-full-stack",
    ],
    "go-projects": [
        "go-cook",
        "bookmark-manager",
    ],
    "web-apps": [
        "interactive-data-dashboard",
        "audio-waveform-editor",
        "my-blog-app",
        "excel-integrated-project-management-system",
        "CloudFileManager",
        "react-todo-spa",
    ],
    "python-tools": [
        "imgannotator",
        "nw-music-review",
        "cooking-with-code",
        "media-encode-pipeline",
    ],
}

# Repos to archive (mark read-only on GitHub, don't merge)
TO_ARCHIVE = [
    "skills-resolve-merge-conflicts",
    "skills-github-pages",
    "skills-introduction-to-github",
]

WORK_DIR = Path.home() / "repo-consolidation"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def run(cmd: list[str], cwd: Path = None, check: bool = True, env: dict = None) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    import os
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=full_env)
    if result.stdout.strip():
        for line in result.stdout.strip().splitlines():
            print(f"    {line}")
    if result.returncode != 0 and result.stderr.strip():
        for line in result.stderr.strip().splitlines():
            print(f"  STDERR: {line}")
    if result.returncode != 0 and check:
        raise RuntimeError(f"Command failed (exit {result.returncode}): {' '.join(str(c) for c in cmd)}")
    return result


def repo_url(name: str) -> str:
    return f"https://github.com/{GITHUB_USER}/{name}.git"


def gh_repo_exists(name: str) -> bool:
    result = run(["gh", "repo", "view", f"{GITHUB_USER}/{name}"], check=False)
    return result.returncode == 0


def check_prerequisites():
    """Verify git, gh, and git-filter-repo are available."""
    missing = []
    for tool in ["git", "gh"]:
        if subprocess.run(["which", tool], capture_output=True).returncode != 0:
            missing.append(tool)

    # git filter-repo is a python script — check via git
    result = subprocess.run(["git", "filter-repo", "--version"], capture_output=True)
    if result.returncode != 0:
        print("  git-filter-repo not found. Installing via pip...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "git-filter-repo", "--break-system-packages"],
            check=False
        )
        # Try brew as fallback
        result2 = subprocess.run(["git", "filter-repo", "--version"], capture_output=True)
        if result2.returncode != 0:
            missing.append("git-filter-repo (install: brew install git-filter-repo)")

    if missing:
        print(f"ERROR: Missing tools: {missing}", file=sys.stderr)
        sys.exit(1)

    result = run(["gh", "auth", "status"], check=False)
    if result.returncode != 0:
        print("ERROR: Not authenticated. Run: gh auth login", file=sys.stderr)
        sys.exit(1)


# ─── Core logic ───────────────────────────────────────────────────────────────

def clone_and_rewrite(source_name: str, target_dir: Path) -> Path:
    """
    Clone source repo into a temp directory, then use git filter-repo
    to rewrite all paths under source_name/ subdirectory.
    Returns path to the rewritten clone.
    """
    clone_dir = WORK_DIR / "_clones" / source_name
    clone_dir.parent.mkdir(parents=True, exist_ok=True)

    # Fresh clone (remove if exists from prior run)
    if clone_dir.exists():
        import shutil
        shutil.rmtree(clone_dir)

    print(f"\n  ── Cloning {source_name}...")
    run(["git", "clone", repo_url(source_name), str(clone_dir)])

    # Rewrite history: move all files under source_name/ subdirectory
    # --to-subdirectory-filter is the clean, purpose-built flag for this
    print(f"  ── Rewriting history → {source_name}/")
    run(
        ["git", "filter-repo", "--to-subdirectory-filter", source_name, "--force"],
        cwd=clone_dir
    )

    return clone_dir


def create_monorepo(target_name: str, source_repos: list[str]):
    """
    Creates a new GitHub repo, then merges each source repo into a
    subdirectory preserving full git history.
    """
    print(f"\n{'='*60}")
    print(f"Creating monorepo: {target_name}")
    print(f"  Sources: {source_repos}")
    print(f"{'='*60}")

    target_dir = WORK_DIR / target_name

    # Skip if already done
    if (target_dir / ".git").exists():
        print(f"  Target dir already exists, skipping init.")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        run(["git", "init", "-b", "main"], cwd=target_dir)
        run(["git", "commit", "--allow-empty", "-m", "chore: initial empty commit"], cwd=target_dir)

    for source_name in source_repos:
        print(f"\n  ── Merging {source_name} → {target_name}/{source_name}/")

        try:
            clone_dir = clone_and_rewrite(source_name, target_dir)
        except RuntimeError as e:
            print(f"  WARNING: Failed to process {source_name}: {e}. Skipping.")
            continue

        # Add rewritten clone as a remote and fetch
        remote_name = f"src-{source_name}"

        # Remove remote if it already exists (re-run safety)
        run(["git", "remote", "remove", remote_name], cwd=target_dir, check=False)
        run(["git", "remote", "add", remote_name, str(clone_dir)], cwd=target_dir)
        run(["git", "fetch", remote_name], cwd=target_dir)

        # Determine the default branch of the source
        default_branch = None
        for branch in ["main", "master"]:
            result = run(
                ["git", "ls-remote", "--heads", remote_name, branch],
                cwd=target_dir, check=False
            )
            if result.stdout.strip():
                default_branch = branch
                break

        if not default_branch:
            print(f"  WARNING: No main/master branch found for {source_name}, skipping.")
            run(["git", "remote", "remove", remote_name], cwd=target_dir, check=False)
            continue

        # Merge with unrelated histories allowed (histories are unrelated between repos)
        run([
            "git", "merge",
            "--allow-unrelated-histories",
            "--no-edit",
            "-m", f"feat: import {source_name} into {source_name}/ subdirectory",
            f"{remote_name}/{default_branch}"
        ], cwd=target_dir)

        # Cleanup remote (keep clone dir for debugging if needed)
        run(["git", "remote", "remove", remote_name], cwd=target_dir)

    # Add root README
    _write_readme(target_dir, target_name, source_repos)

    # Create GitHub repo and push
    print(f"\n  ── Pushing {target_name} to GitHub...")
    if not gh_repo_exists(target_name):
        run([
            "gh", "repo", "create", f"{GITHUB_USER}/{target_name}",
            "--public",
            "--description", f"Monorepo: {', '.join(source_repos)}"
        ])
    else:
        print(f"  Repo {target_name} already exists on GitHub, pushing to it.")

    # Set or update origin
    run(["git", "remote", "remove", "origin"], cwd=target_dir, check=False)
    run(["git", "remote", "add", "origin", repo_url(target_name)], cwd=target_dir)
    run(["git", "push", "-u", "origin", "main"], cwd=target_dir)

    print(f"\n  ✅ Done: https://github.com/{GITHUB_USER}/{target_name}")


def _write_readme(target_dir: Path, target_name: str, source_repos: list[str]):
    readme = target_dir / "README.md"
    if readme.exists():
        return  # Don't overwrite if already committed

    sections = "\n".join(
        f"- [`{r}/`](./{r}/) — formerly "
        f"[`{GITHUB_USER}/{r}`](https://github.com/{GITHUB_USER}/{r})"
        for r in source_repos
    )
    content = f"""# {target_name}

Consolidated monorepo. Each subdirectory is a self-contained project
with its own build system. Full git history is preserved.

## Projects

{sections}
"""
    readme.write_text(content)
    run(["git", "add", "README.md"], cwd=target_dir)
    run(["git", "commit", "-m", "docs: add monorepo root README"], cwd=target_dir)


def archive_repos(repos: list[str]):
    print(f"\n{'='*60}")
    print("Archiving repos...")
    for repo in repos:
        print(f"  Archiving {repo}...")
        run(["gh", "repo", "archive", f"{GITHUB_USER}/{repo}", "--yes"], check=False)
    print("  ✅ Done archiving.")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Consolidate GitHub repos into monorepos")
    parser.add_argument(
        "--only", nargs="+", metavar="REPO",
        help="Only process these target monorepo names (e.g. --only devtools go-projects)"
    )
    parser.add_argument(
        "--skip-archive", action="store_true",
        help="Skip archiving the TO_ARCHIVE repos"
    )
    args = parser.parse_args()

    print(f"Work directory: {WORK_DIR}")
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    check_prerequisites()

    targets = CONSOLIDATIONS
    if args.only:
        targets = {k: v for k, v in CONSOLIDATIONS.items() if k in args.only}
        if not targets:
            print(f"ERROR: None of {args.only} found in CONSOLIDATIONS.", file=sys.stderr)
            sys.exit(1)

    for target_name, source_repos in targets.items():
        create_monorepo(target_name, source_repos)

    if not args.skip_archive:
        archive_repos(TO_ARCHIVE)

    print(f"\n{'='*60}")
    print("🎉 All done!")
    for target, sources in targets.items():
        print(f"  https://github.com/{GITHUB_USER}/{target}  ({len(sources)} merged)")
    if not args.skip_archive:
        print(f"  Archived: {TO_ARCHIVE}")


if __name__ == "__main__":
    main()