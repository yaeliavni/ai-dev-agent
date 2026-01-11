# AI Dev Agent 

This repository contains a zero-maintenance, serverless AI developer agent built entirely within GitHub Actions. It allows for natural language code modifications directly through GitHub Issue comments.

### Architecture
To ensure maximum reliability, this project uses a **Stateless Overwrite** approach:
* **Robustness:** Bypasses fragile Git patches to prevent "corrupt patch" errors.
* **No Maintenance:** Operates purely on GitHub Actions runners; no external servers or databases required.
* **Universal Provider:** Uses the OpenAI-compatible API format, currently configured for **MiniMax M2.1**.

### How It Works
1. **Trigger:** Mention `@agent-code` in any GitHub Issue comment.
2. **AI Processing:** The runner sends the repository context and your request to the MiniMax API.
3. **Smart Apply:** A custom parser interprets the AI response, creates necessary directories, and overwrites files.
4. **Pull Request:** The agent stages changes, cleans up temporary files, and opens a Pull Request.

### Setup
1. Clone this repository.
2. Add your `AI_KEY`, `AI_BASE_URL`, and `AI_MODEL`.
3. Ensure Workflow Permissions are set to **Read/Write** in repository settings.
