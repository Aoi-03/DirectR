#!/usr/bin/env python3
"""
DirectR Pre-Commit Boundary Guard
Verifies that:
1. No image files (.png, .jpg, etc.) are staged.
2. Changes stay within the collaborator's assigned module folder.
"""

import sys
import subprocess
import os

VALID_EXTENSIONS_BLOCKED = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".ico"}

MODULE_MAP = {
    "feature/narrative": "modules/narrative_screenplay",
    "feature/visual-art": "modules/visual_art_design",
    "feature/audio-studio": "modules/audio_soundscapes",
    "feature/creator-agents": "modules/creator_distribution",
}


def get_staged_files():
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def get_current_branch():
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        branch = result.stdout.strip()
        if branch:
            return branch
    except Exception:
        pass
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "main"


def main():
    staged = get_staged_files()
    if not staged:
        sys.exit(0)

    # 1. Check for blocked image files
    blocked_images = []
    for f in staged:
        ext = os.path.splitext(f)[1].lower()
        if ext in VALID_EXTENSIONS_BLOCKED or "screenshot" in f.lower():
            blocked_images.append(f)

    if blocked_images:
        print("\n❌ [DirectR Guard Error] Blocked image files are staged:")
        for img in blocked_images:
            print(f"   - {img}")
        print("\nImages must not be committed to GitHub. Run: git reset HEAD <file> to unstage them.\n")
        sys.exit(1)

    # 2. Check module boundaries if on a feature branch
    branch = get_current_branch()
    if branch in MODULE_MAP:
        allowed_dir = MODULE_MAP[branch]
        violations = []
        for f in staged:
            # Allow common documentation/setup updates if explicitly intended, but flag other modules
            if f.startswith("modules/") and not f.startswith(allowed_dir):
                violations.append(f)

        if violations:
            print(f"\n⚠️  [DirectR Guard Warning] Branch '{branch}' modified other module files:")
            for v in violations:
                print(f"   - {v}")
            print(f"\nYour assigned directory is: {allowed_dir}")
            print("To keep the repository conflict-free, please only commit files in your assigned module.")
            print("Run: git reset HEAD <file> to unstage external files.\n")
            sys.exit(1)

    print("✅ [DirectR Guard] All staged files adhere to module isolation rules.")
    sys.exit(0)


if __name__ == "__main__":
    main()
