from pprint import pprint
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.notion_task_manager import create_task
from src.constants import TASK_STATUS

from dotenv import load_dotenv

load_dotenv()

# Install the Slack app and get xoxb- token in advance
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.command("/create-task")
def create_task_command(ack, body, say):
    ack()
    print(body)
    task_name = body["text"]
    create_task(task_name=task_name)
    say("Task: " + task_name + " を作成しました")


@app.command("/done_task")
def done_task_command(ack, body, say):
    ack()
    print(body)
    task_name = body["text"]
    data = {
        "properties": {
            "Status": {"status": {"name": TASK_STATUS["done"]}},
        },
    }
    create_task(data)
    say("Task: " + task_name + " を完了しました")


@app.command("/hello-socket-mode")
def hello_command(ack, body, logger, command):
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")


@app.event("app_mention")
def event_test(event, say):
    # メッセージを取得する
    message = event["blocks"][0]["elements"][0]["elements"][1]["text"]

    data = {
        "parent": {"database_id": os.getenv("TARGET_TASK_DATABASE_ID")},
        "properties": {
            "Name": {"title": [{"text": {"content": message}}]},
            "Status": {"status": {"name": "In progress"}},
        },
    }
    create_task(data)

    say("Task: " + message + " を作成しました")


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
