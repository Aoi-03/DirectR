# DirectR: Team Collaboration & Git Workflow Guide

Welcome to the **DirectR** project! This guide is written specifically for our 4-person team. We are building 4 distinct AI modules on separate computers, unified by a single GitHub repository: `https://github.com/Aoi-03/DirectR`.

---

## 📌 The Golden Rules of DirectR Development

1. **Strict Folder Ownership (Edit ONLY Your Assigned Module)**:
   - Each friend is assigned **one primary module directory**.
   - You may write, edit, and delete files **only** inside your designated folder.
   - You must **never** modify files in another friend's module folder.

2. **Full Read & Import Access**:
   - You can read, inspect, import, and test against any code written by your teammates.
   - For example, Member 3 (Audio) can import schemas and scene data from Member 1 (Narrative) to test tension-based music generation.

3. **Shared Contracts in `core/` Require Consensus**:
   - The `core/` folder contains shared schemas (`core/schemas.py`) and the swarm orchestrator (`core/orchestrator.py`).
   - If you need a new field in a shared data model, discuss it in team chat or propose it via a dedicated Pull Request. Do not make unilateral changes to `core/`.

4. **Never Commit Images or Large Media Binaries**:
   - `.gitignore` is pre-configured to ignore all `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, and video files.
   - Keep generated test images/audio local or link them using cloud URLs or mocks.

---

## 👥 Module Assignment Matrix

| Collaborator | Assigned Directory | Branch Name | Track Role |
| :--- | :--- | :--- | :--- |
| **Friend 1** | `modules/narrative_screenplay/` | `feature/narrative` | **Storytelling & Co-Writers** |
| **Friend 2** | `modules/visual_art_design/` | `feature/visual-art` | **Visual Art & Design Assist** |
| **Friend 3** | `modules/audio_soundscapes/` | `feature/audio-studio` | **Music & Audio Studios** |
| **Friend 4** | `modules/creator_distribution/` | `feature/creator-agents` | **Autonomous Creator Agents** |

---

## 🛠️ Phase 1: Initial Setup (Do this once on your computer)

### Step 1: Clone the Repository
Open PowerShell or your terminal and clone the repository:
```bash
git clone https://github.com/Aoi-03/DirectR.git
cd DirectR
```

### Step 2: Configure Your Git Identity
Ensure your name and GitHub email are properly set:
```bash
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

### Step 3: Set Up Python Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate it:
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Install dependencies:
pip install -r requirements.txt
```

### Step 4: Create and Switch to Your Personal Feature Branch
Find your assigned branch name from the matrix above and create it:

```bash
# Friend 1:
git checkout -b feature/narrative

# Friend 2:
git checkout -b feature/visual-art

# Friend 3:
git checkout -b feature/audio-studio

# Friend 4:
git checkout -b feature/creator-agents
```

Push your branch to GitHub to track it remotely:
```bash
git push -u origin <your-branch-name>
```

---

## 🔄 Phase 2: Daily Working Routine (Repeat everyday)

Follow this simple 4-step routine every time you sit down to code:

### Step 1: Pull the Latest Updates from Your Teammates
Before writing any new code, grab everything your friends worked on:
```bash
# 1. Switch to main and pull the latest changes
git checkout main
git pull origin main

# 2. Switch back to your feature branch
git checkout <your-branch-name>

# 3. Bring teammates' latest updates into your branch
git merge main
```
> **Tip:** You now have all updates made by the other 3 friends, and your branch is completely up-to-date!

### Step 2: Develop and Test in Your Folder
Write your code, add your tests, and verify your implementation inside your assigned module:
- Friend 1 writes inside `modules/narrative_screenplay/`
- Friend 2 writes inside `modules/visual_art_design/`
- Friend 3 writes inside `modules/audio_soundscapes/`
- Friend 4 writes inside `modules/creator_distribution/`

To test your specific module:
```bash
pytest modules/<your-module>/
```

To test the entire integrated pipeline with teammates' modules:
```bash
python main.py
```

### Step 3: Stage and Commit ONLY Your Module's Files
When you are ready to save your work, **do not run a blind `git add .`**. Always stage specifically your own directory:

```bash
# Check what has changed
git status

# Stage ONLY your module directory
git add modules/<your-module>/

# Commit with a clear descriptive message
git commit -m "feat(<module-name>): implement character psychology validator"
```

### Step 4: Push to Your Branch on GitHub
```bash
git push origin <your-branch-name>
```

---

## 🔀 Phase 3: Merging Your Work into `main` via Pull Request (PR)

When you complete a milestone or feature:

1. **Open a Pull Request on GitHub**:
   - Go to `https://github.com/Aoi-03/DirectR/pulls`
   - Click **New Pull Request**
   - Base: `main` ⟵ Compare: `<your-branch-name>`
   - Give it a clear title, e.g., `[Narrative] Add dialect adaptation & branching memory trees`.
2. **Automated CI Check**:
   - GitHub Actions will automatically run the test suite to ensure no breaking changes exist.
3. **Peer Review**:
   - Notify the team in group chat.
   - At least one teammate checks and approves the PR.
4. **Merge**:
   - Click **Merge Pull Request** (Squash and merge or rebase).
5. **Notify the Team**:
   - Announce: *"My PR is merged into main! Please run `git checkout main && git pull`."*

---

## ⚠️ Merge Conflict Prevention & Resolution

Because everyone works in separate directories, **merge conflicts should be virtually zero**. However, if two people both touch a root file (like `requirements.txt` or `README.md`), a conflict could occur.

### If git reports a conflict during `git merge main`:
1. Run `git status` to see which file has conflicting changes.
2. Open the file in your code editor (look for `<<<<<<< HEAD`, `=======`, and `>>>>>>> main`).
3. Keep both sets of additions (for example, if both of you added dependencies to `requirements.txt`, keep both lines).
4. Save the file.
5. Stage and finalize the merge:
   ```bash
   git add <conflicted-file>
   git commit -m "chore: resolve merge conflict with main"
   git push origin <your-branch-name>
   ```

---

## 📋 Pre-Push Checklist

Before you push your commits to GitHub, verify:
- [ ] Have I edited files **only** in my assigned directory?
- [ ] Did I verify that no `.png` or image files are staged (`git status`)?
- [ ] Do all local tests pass (`pytest`)?
- [ ] Did I run `python main.py` to confirm the integration runs without syntax errors?
- [ ] Is my commit message clear and concise?

---

## 💡 Quick Reference: Git Command Cheat Sheet

| Action | Command |
| :--- | :--- |
| **Check current branch & modified files** | `git status` |
| **Switch to another branch** | `git checkout <branch-name>` |
| **Pull latest changes from main** | `git pull origin main` |
| **Merge main into current branch** | `git merge main` |
| **Stage changes in your module** | `git add modules/<your-module>/` |
| **Commit staged changes** | `git commit -m "feat(...): message"` |
| **Push your branch to GitHub** | `git push origin <your-branch-name>` |
| **Discard local uncommitted changes** | `git restore <file>` |
