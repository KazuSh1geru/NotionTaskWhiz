import os
import json
import requests
import dotenv

dotenv.load_dotenv()

integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
target_task_database_id = os.getenv("TARGET_TASK_DATABASE_ID")
sample_page_id = os.getenv("SAMPLE_PAGE_ID")


headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + integration_token,
}

payload = {"page_size": 100}

data = {
    "properties": {
        "Status": {
            # "status": { "name": "In progress" }
            "status": {"name": "Done"}
        }
    }
}


def test_status_change(sample_page_id, data):
    url = f"https://api.notion.com/v1/pages/{sample_page_id}"
    response = requests.patch(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("更新が成功しました")
    else:
        print("エラーが発生しました。ステータスコード:", response.status_code)


def test_response():
    url = f"https://api.notion.com/v1/databases/{target_task_database_id}/query"
    response = requests.post(url, json=payload, headers=headers)

    # url = f'https://api.notion.com/v1/databases/{target_task_database_id}'
    # response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.text
        # ここでデータを処理する
        print(data)
    else:
        print("エラーが発生しました。ステータスコード:", response.status_code)


if __name__ == "__main__":
    test_status_change(sample_page_id, data)
    # test_response()
