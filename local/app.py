from pprint import pprint
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.notion_task_manager import create_task, status_change
from src.constants import TASK_STATUS

from dotenv import load_dotenv

load_dotenv()

# Install the Slack app and get xoxb- token in advance
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.command("/create-task")
def create_task_command(ack, body, logger):
    client = app.client
    trigger_id = body["trigger_id"]
    view = {
        "title": {"type": "plain_text", "text": "タスクの新規登録 :pencil:", "emoji": True},
        "submit": {"type": "plain_text", "text": "送信", "emoji": True},
        "type": "modal",
        "close": {"type": "plain_text", "text": "キャンセル", "emoji": True},
        "blocks": [
            {
                "type": "input",
                "block_id": "input-title",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "件名を入力してください",
                        "emoji": True,
                    },
                },
                "label": {"type": "plain_text", "text": "件名", "emoji": True},
                "optional": False,
            }
        ],
    }
    try:
        response = client.views_open(trigger_id=trigger_id, view=view)
        logger.info(response)

        # モーダルで送信ボタンが押された時の処理
        @app.view("")
        def handle_create_task(ack, body, logger):
            logger.info(body)
            try:
                task_name = body["view"]["state"]["values"]["input-title"]["input"][
                    "value"
                ]
                create_task(task_name=task_name)
                ack()
                app.client.chat_postMessage(
                    channel=os.getenv("SLACK_CHANNEL_ID"), text=f"{task_name} を作成しました！"
                )
            except Exception as e:
                logger.error(str(e))

    except Exception as e:
        print(e)
    ack()


@app.command("/done-task")
def done_task_command(ack, body, say):
    ack()
    print(body)
    task_name = body["text"]
    status_change(task_name=task_name, status=TASK_STATUS["done"])
    say(f"{task_name} Done!")


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
