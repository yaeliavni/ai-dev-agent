# ai-dev-agent
# Project Update: Autonomous Dev-Agent POC (MiniMax M2.1)

I’ve finished setting up the infrastructure for the autonomous developer agent. The goal was to create a "hands-off" bridge between GitHub issues and the MiniMax M2.1 model.

### 1. What’s implemented:
* **Event Trigger:** The agent is fully integrated with GitHub Actions. It listens specifically for `@agent` comments on any issue.
* **Interleaved Thinking Parser:** I’ve added logic to extract the `<think>` tags from MiniMax. This allows the team to see the agent's internal reasoning directly in the GitHub thread before it makes changes.
* **Automated Git Flow:** The script handles the full lifecycle: creating a dedicated branch, committing code fixes, and opening a Pull Request (PR) for human review.
* **Simulation Mode:** I've verified the "plumbing" using a simulation script. The PR creation and commenting system are working perfectly.

### 2. Repo Structure:
* `.github/workflows/agent.yml`: The automation trigger.
* `agent_logic.py`: The core bridge script (clean, documented, and modular).
* `.openhands/microagents/repo.md`: Instructions for repo-specific coding standards.

### 3. Final Steps:
The system is currently in "Simulation Mode" to prevent errors. To go live, we just need to:
 **API Key:** Add the `MINIMAX_API_KEY` to the GitHub Secrets.


