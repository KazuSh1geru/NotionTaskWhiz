from pprint import pprint
import os
import json
import requests
import dotenv
from src.constants import TASK_STATUS

dotenv.load_dotenv()

integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
target_task_database_id = os.getenv("TARGET_TASK_DATABASE_ID")


HEADERS = {
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + integration_token,
}


def create_task(task_name, status=TASK_STATUS["not_started"]):
    send_data = {
        "parent": {"database_id": target_task_database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": task_name}}]},
            "Status": {"status": {"name": status}},
        },
    }
    url = f"https://api.notion.com/v1/pages"
    response = requests.post(url, headers=HEADERS, data=json.dumps(send_data))

    if response.status_code == 200:
        res = response.text
        # ここでデータを処理する
        pprint(res)
    else:
        pprint("エラーが発生しました。ステータスコード:", response.status_code)


# task_name から page_id を取得する
def find_task(task_name):
    payload = {"filter": {"property": "Name", "title": {"equals": task_name}}}
    url = f"https://api.notion.com/v1/databases/{target_task_database_id}/query"
    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        res = response.json()
        # ここでデータを処理する
        page_id = res["results"][0]["id"]
        pprint(page_id)
        return page_id
    else:
        print("エラーが発生しました。ステータスコード:", response.status_code)


# task_name から page_id を取得して、ステータスを更新する
def status_change(task_name, status=TASK_STATUS["done"]):
    page_id = find_task(task_name=task_name)
    data = {"properties": {"Status": {"status": {"name": status}}}}
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.patch(url, headers=HEADERS, data=json.dumps(data))

    if response.status_code == 200:
        pprint("更新が成功しました")
    else:
        pprint("エラーが発生しました。ステータスコード:", response.status_code)


def test_response():
    payload = {"page_size": 100}
    url = f"https://api.notion.com/v1/databases/{target_task_database_id}/query"
    response = requests.post(url, json=payload, headers=HEADERS)

    # url = f'https://api.notion.com/v1/databases/{target_task_database_id}'
    # response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        # ここでデータを処理する
        pprint(data)
    else:
        pprint("エラーが発生しました。ステータスコード:", response.status_code)


if __name__ == "__main__":
    # create_task(data)
    # test_response()
    # find_task("ティッシュ買う")
    status_change("ティッシュ買う")
