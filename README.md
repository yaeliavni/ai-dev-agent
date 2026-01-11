# Dev-Agent: MiniMax + OpenHands

A cloud-native bridge that turns GitHub Issues into Pull Requests using **MiniMax M2.1**. 

Instead of running agents locally on your laptop, this setup lives in GitHub Actions. It stays on standby and "wakes up" when called, thinks through the problem, and either pushes a fix or asks for more info. You just `git pull` the result once the PR is ready.

### How it works
Everything happens in the GitHub cloud:
1. **Trigger:** Open a **GitHub Issue** and comment `@agent <instruction>`.
2. **Reasoning:** The agent uses MiniMax's "Interleaved Thinking" to plan the fix and posts its logic as a comment.
3. **Action/Query:** The agent will either open a **Pull Request** or, if the task is unclear, ask you a follow-up question.

### Tech Stack
* **LLM:** MiniMax M2.1 (Optimized for reasoning and multi-language coding)
* **Automation:** GitHub Actions (Ubuntu runner)
* **Ops:** PyGithub for repo management

### Project Structure
* `.github/workflows/agent.yml` – The "ears" (listens for `@agent` triggers).
* `agent_logic.py` – The bridge (talks to MiniMax and handles Git logic).
* `.openhands/microagents/repo.md` – Repo-specific coding standards for the AI to follow.

### Setup & Installation
If you're setting this up for a new repo:

1. **GitHub Secrets:** Add these under **Settings > Secrets and variables > Actions**:
   * `MINIMAX_API_KEY`: Your key from MiniMax Open Platform.
   * `MY_GITHUB_TOKEN`: A Personal Access Token (PAT) with `repo` and `workflow` scopes.

2. **Permissions:**
   Go to **Settings > Actions > General**. 
   * Set **Workflow permissions** to "Read and write permissions".
   * Check **"Allow GitHub Actions to create and approve pull requests"**.
