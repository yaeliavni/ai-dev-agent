import os
import time
from github import Github

# Get env vars from GitHub Actions
# Need the minimax key, gh token, and some issue context
api_key = os.getenv("MINIMAX_API_KEY")
gh_token = os.getenv("GITHUB_TOKEN")
comment_body = os.getenv("COMMENT_BODY")
issue_number = int(os.getenv("ISSUE_NUMBER"))
repo_name = os.getenv("REPO_NAME")

def call_minimax(prompt, api_key):
    """
    Hit the MiniMax API. 
    Currently in simulation mode until we plug the real key.
    """
    # Real logic will go here: response = requests.post(...)
    
    # Fake response for testing parsing logic
    return "<think>Let's check the request. User wants a math tool. I'll make calc.py.</think> file:calc.py\ncontent:print(10 * 10)"

def parse_and_execute(repo, issue, raw_response):
    """
    Split the AI response into 'Thinking' and 'Actual Code'.
    """
    # 1. Grab the <think> part and post it as a comment so we see what's happening
    if "<think>" in raw_response:
        thought = raw_response.split("<think>")[1].split("</think>")[0]
        issue.create_comment(f"**Agent Thinking Process:**\n> {thought.strip()}")
        action_part = raw_response.split("</think>")[1].strip()
    else:
        action_part = raw_response

    # 2. Simple parsing for file path and content
    if "file:" in action_part:
        # Split by content tag to get the file name and the code
        file_info = action_part.split("\ncontent:")
        file_path = file_info[0].replace("file:", "").strip()
        new_content = file_info[1].strip()
        
        # Build a unique branch name so we don't clash
        branch_name = f"ai-fix-issue-{issue_number}-{int(time.time())}"
        
        # Kick off the Git stuff
        create_pull_request(repo, branch_name, file_path, new_content)
        issue.create_comment(f"Created a PR for: `{file_path}`")

def create_pull_request(repo, branch_name, file_path, new_content):
    """
    The Git heavy lifting: Create branch, commit file, open PR.
    """
    main = repo.get_branch("main")
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main.commit.sha)
    
    try:
        # Check if file exists, if yes - update it
        contents = repo.get_contents(file_path, ref="main")
        repo.update_file(contents.path, "AI Update", new_content, contents.sha, branch=branch_name)
    except:
        # If not found, just create it as new
        repo.create_file(file_path, "AI Create", new_content, branch=branch_name)
    
    # Open the PR so devs can review
    repo.create_pull(
        title=f"AI Fix for #{issue_number}", 
        body=f"Generated via MiniMax M2.1 agent loop.", 
        head=branch_name, 
        base="main"
    )

def run_agent():
    # Make sure we actually have the key before running
    if not api_key or api_key == "waiting_for_key":
        g = Github(gh_token)
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment("System ready. Just waiting for the API Key to go live.")
        return

    # Setup GitHub connection
    g = Github(gh_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)
    
    issue.create_comment("Agent is analyzing the issue...")
    
    # Get the AI result and run it
    raw_ai_response = call_minimax(comment_body, api_key)
    parse_and_execute(repo, issue, raw_ai_response)

if __name__ == "__main__":
    run_agent()
