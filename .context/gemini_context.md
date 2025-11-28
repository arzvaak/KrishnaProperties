# Gemini AI Context

## Instructions
- **Refactoring Philosophy**: Always try to refactor for modularity, but do not over-refactor. Ensure the ability to scale is preserved and modularity is- Execute tasks step-by-step, allowing for user feedback at each stage.
- **CRITICAL**: ALWAYS update `task.md` (check off items) and `work_log.md` (add entry) IMMEDIATELY after completing a feature. Do not wait for the user to remind you. This is a strict requirement.
- **Testing Rule**: "New Component = New Test". Every new component MUST have a corresponding unit test file.
- **Database/Storage**: ALWAYS use Firebase (Firestore/Storage) for any database or file storage requirements. Do not use local files (except for temporary caching like localStorage) or other databases unless explicitly requested. Do everything related to workspace code in the venv environment only.
- **Avoid Duplication**: Do not create new duplicates or logic when it already exists. Reuse existing structures to prevent overbloating.
