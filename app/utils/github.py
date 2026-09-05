# app/utils/github_export.py
import os
import base64
import requests
from app import database
from app.utils.md import note_to_markdown
from app import database
def push_to_github(note, user_id):
    token = database.get_github_token(user_id)
    repo = database.get_github_repo(user_id)

    if not token or not repo:
        return False 


    filename = f"{note[3]}/note_{note[0]}.md"  # category 폴더 안에 저장
    content = note_to_markdown(note)  

    url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "message": f"add writeup: {note[2]}",
        "content": base64.b64encode(content.encode()).decode(),
    }
    res = requests.put(url, json=data, headers=headers)
    return res.status_code in (200, 201)