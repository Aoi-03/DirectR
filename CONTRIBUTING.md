# Contributing to DirectR

Thank you for contributing to DirectR! To keep our 4-person parallel development smooth and conflict-free, please adhere to these guidelines.

---

## 🌿 Branching Model

1. **`main` Branch**: Contains tested, production-ready code. Direct pushes to `main` are restricted.
2. **Feature Branches**: Every collaborator works in their assigned branch:
   - Friend 1: `feature/narrative`
   - Friend 2: `feature/visual-art`
   - Friend 3: `feature/audio-studio`
   - Friend 4: `feature/creator-agents`

---

## 📝 Commit Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```text
<type>(<scope>): <short description>
```

### Allowed Types:
- `feat`: A new feature or capability.
- `fix`: A bug fix.
- `refactor`: Code restructuring without changing external behavior.
- `test`: Adding or updating unit tests.
- `docs`: Documentation updates.
- `chore`: Maintenance tasks, dependency updates.

### Allowed Scopes:
- `narrative`: Changes in `modules/narrative_screenplay/`
- `visual`: Changes in `modules/visual_art_design/`
- `audio`: Changes in `modules/audio_soundscapes/`
- `creator`: Changes in `modules/creator_distribution/`
- `core`: Changes in `core/` (requires consensus)

### Examples:
- `feat(narrative): implement dialect adaptation rule engine`
- `feat(visual): add multi-angle turnaround generator`
- `feat(audio): implement tension-based dynamic stem mixer`
- `feat(creator): add A/B thumbnail heatmap scorer`
- `test(narrative): add test coverage for character psychology trees`

---

## 📬 Pull Request Process

1. Ensure all tests pass: `pytest`.
2. Ensure you haven't modified files outside your assigned directory.
3. Push your feature branch to GitHub: `git push origin <your-branch>`.
4. Open a Pull Request on GitHub against `main`.
5. Request review from teammates.
6. Once approved and CI passes, merge into `main`.
