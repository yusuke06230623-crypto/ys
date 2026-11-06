import os
import requests
from google import genai

# 環境変数からAPIキーとLINEアクセストークンを取得
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

def generate_daily_note():
    # Geminiクライアントの初期化（google-genai SDK最新仕様）
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Geminiにデイリーノートを作成してもらう
    prompt = "今日のデイリーノートを作成してください。今日の振り返りやタスク管理に役立つMarkdown形式の簡潔な文章をお願いします。"
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    note_content = response.text
    
    # ノートをファイルとして保存（GitHub Actionsでコミットするため）
    with open("latest_note_draft.md", "w", encoding="utf-8") as f:
        f.write(note_content)
        
    return note_content

def send_line_notification(message):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    # LINEの文字数制限（最大5000文字）に合わせる
    payload = {
        "messages": [
            {
                "type": "text",
                "text": f"【デイリーノート自動生成】\n\n{message[:4900]}"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"LINE Notification Response: {response.status_code}")

if __name__ == "__main__":
    note = generate_daily_note()
    send_line_notification(note)
