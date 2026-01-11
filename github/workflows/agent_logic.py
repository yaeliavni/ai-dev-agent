import os
import requests
from github import Github

# שליפת נתונים מהסביבה של GitHub
api_key = os.getenv("MINIMAX_API_KEY")
gh_token = os.getenv("GITHUB_TOKEN")
comment_body = os.getenv("COMMENT_BODY")
issue_number = int(os.getenv("ISSUE_NUMBER"))
repo_name = os.getenv("REPO_NAME")

def call_minimax(prompt, api_key):
    url = "https://api.minimax.io/v1/text/chat/completions_pro"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "MiniMax-M2.1", # המודל שהמנהל בחר
        "messages": [{"role": "user", "content": prompt}],
        "tokens_to_generate": 4096,
        "temperature": 0.01 # טמפרטורה נמוכה לקוד מדויק
    }
    # כאן תבוא הפקודה: response = requests.post(url, json=payload, headers=headers)
    # בינתיים נחזיר תשובה דמה עם תגיות מחשבה לניסוי
    return "<think>אני מנתח את הבקשה ויוצר קובץ חדש.</think> הנה הקוד המבוקש..."

def extract_thinking_and_respond(issue, raw_response):
    # חיפוש תגיות המחשבה של MiniMax
    if "<think>" in raw_response:
        parts = raw_response.split("<think>")
        # החלק שאחרי תגית הפתיחה ולפני תגית הסגירה
        thought_content = parts[1].split("</think>")[0]
        # החלק שנשאר הוא הקוד או התשובה הסופית
        final_answer = parts[1].split("</think>")[1]
        
        # פרסום המחשבה בתגובה בגיטהאב
        issue.create_comment(f"🧠 **תהליך החשיבה של הסוכן:**\n> {thought_content.strip()}")
        return final_answer.strip()
    return raw_response

def create_pull_request(repo, branch_name, file_path, new_content):
    # 1. יצירת ענף (Branch) חדש
    main_branch = repo.get_branch("main")
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_branch.commit.sha)
    
    # 2. עדכון הקובץ
    contents = repo.get_contents(file_path, ref="main")
    repo.update_file(contents.path, "AI bug fix", new_content, contents.sha, branch=branch_name)
    
    # 3. פתיחת PR
    repo.create_pull(title=f"AI Fix: {file_path}", body="תיקון אוטומטי על ידי MiniMax M2.1", head=branch_name, base="main")

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
