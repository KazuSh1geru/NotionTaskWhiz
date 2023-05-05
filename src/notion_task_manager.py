import requests
import os
import dotenv

dotenv.load_dotenv()

integration_token = os.getenv('NOTION_INTEGRATION_TOKEN')
target_task_database_id= os.getenv('TARGET_TASK_DATABASE_ID')

url = f'https://api.notion.com/v1/databases/{target_task_database_id}'

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + integration_token
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.text
    # ここでデータを処理する
    print(data)
else:
    print("エラーが発生しました。ステータスコード:", response.status_code)
