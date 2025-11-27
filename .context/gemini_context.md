# Gemini AI Context

## Instructions
- **Refactoring Philosophy**: Always try to refactor for modularity, but do not over-refactor. Ensure the ability to scale is preserved and modularity is maintained without adding unnecessary complexity.
- **Work Log**: Always update `work_log.md` after completing a task. Maintain the existing table format (`| Date | Time | Feature | Description |`). Import content from old logs if found.
- **Python Environment**: Each workspace has a python venv environment. Do everything related to workspace code in the venv environment only.
- **Avoid Duplication**: Do not create new duplicates or logic when it already exists. Reuse existing structures to prevent overbloating.
