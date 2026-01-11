# MiniMax Agent

This project is a pure configuration AI agent. It uses GitHub Actions to turn issues into code changes without needing any external Python scripts or complex infrastructure.

### How it works
1. **Trigger:** A developer comments `@agent` on a GitHub Issue.
2. **Cloud Execution:** GitHub Actions wakes up a runner (Ubuntu).
3. **AI Call:** The runner sends the issue text to **MiniMax M2.1** using the standard OpenAI API format.
4. **Auto-PR:** The AI response is used to automatically generate a **Pull Request** using the `create-pull-request` action.

### Why this architecture?
* **Pure YAML:** The entire logic lives in `.github/workflows/agent.yml`.

### Setup
1. Add `MINIMAX_API_KEY` to your **GitHub Secrets**.
2. Tag `@agent` in any issue to start the automation.
