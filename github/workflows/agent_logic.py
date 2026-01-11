import os
import requests
from github import Github

# שליפת נתונים מהסביבה של GitHub
api_key = os.getenv("MINIMAX_API_KEY")
gh_token = os.getenv("GITHUB_TOKEN")
comment_body = os.getenv("COMMENT_BODY")
issue_number = int(os.getenv("ISSUE_NUMBER"))
repo_name = os.getenv("REPO_NAME")

def run_agent():
    g = Github(gh_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)

    # 1. שליחת תגובה ראשונית למפתח
    issue.create_comment(f"🤖 **הסוכן התחיל לעבוד!**\nמפעיל את מודל MiniMax M2.1 לניתוח המשימה...")

    # 2. הכנה לקריאה ל-MiniMax (כאן יבוא החיבור האמיתי)
    if api_key == "waiting_for_key" or not api_key:
        issue.create_comment("⚠️ שגיאה: חסר API Key של MiniMax ב-Secrets.")
        return

    # דוגמה לאיך נטפל ב-Thinking Process של המודל
    # המודל של MiniMax מחזיר טקסט בתוך תגיות <think>
    sample_response = "<think>עלי לבדוק את הקובץ main.py ולתקן את הלוגיקה של החישוב.</think> הנה התיקון שהכנתי..."
    
    # שליפת המחשבה של ה-AI והצגתה למפתח
    if "<think>" in sample_response:
        thought = sample_response.split("<think>")[1].split("</think>")[0]
        issue.create_comment(f"🧠 **תהליך החשיבה של הסוכן:**\n> {thought}")

    issue.create_comment("✅ המשימה הושלמה (במצב סימולציה עד לקבלת מפתח אמיתי).")

if __name__ == "__main__":
    run_agent()
