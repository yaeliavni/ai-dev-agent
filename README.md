# MiniMax Cloud Agent (Config-Only)

This repository contains a zero-maintenance AI developer agent built entirely within GitHub Actions. 

### Architecture
To keep the system as simple as possible, this project uses a **Config-Based** approach:
* Instructions are passed directly to the model in the API prompt.
* **Standard Provider:** Uses the OpenAI-compatible API format to communicate with MiniMax M2.1.

### How it works
1. **Comment:** Mention `@agent` in any GitHub Issue.
2. **Trigger:** GitHub Actions launches a temporary Ubuntu runner.
3. **Action:** The runner calls the MiniMax API and automatically opens a Pull Request with the fix.

### Setup
Just add your `MINIMAX_API_KEY` to **Settings > Secrets > Actions**.
