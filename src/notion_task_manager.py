import os
import json
import requests
import dotenv
from src.constants import TASK_STATUS

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


def create_task(task_name, status=TASK_STATUS["not_started"]):
    send_data = {
        "parent": {"database_id": target_task_database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": task_name}}]},
            "Status": {"status": {"name": status}},
        },
    }
    url = f"https://api.notion.com/v1/pages"
    response = requests.post(url, headers=headers, data=json.dumps(send_data))

    if response.status_code == 200:
        res = response.text
        # ここでデータを処理する
        print(res)
    else:
        print("エラーが発生しました。ステータスコード:", response.status_code)


def find_task(task_name):
    url = f"https://api.notion.com/v1/databases/{target_task_database_id}/query"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.text
        # ここでデータを処理する
        print(data)
    else:
        print("エラーが発生しました。ステータスコード:", response.status_code)


# data = {
#     "properties": {
#         "Status": {
#             # "status": { "name": "In progress" }
#             "status": {"name": "Done"}
#         }
#     }
# }


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
    create_task(data)
    # test_response()
