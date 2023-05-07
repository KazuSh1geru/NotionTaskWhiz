from pprint import pprint
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.notion_task_manager import create_task, status_change
from src.constants import TASK_STATUS, CREATE_TASK_VIEW

from dotenv import load_dotenv

load_dotenv()

# Install the Slack app and get xoxb- token in advance
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.command("/create-task")
def create_task_command(ack, body, logger):
    ack()
    logger.info(body)
    client = app.client
    trigger_id = body["trigger_id"]
    view = CREATE_TASK_VIEW
    try:
        response = client.views_open(trigger_id=trigger_id, view=view)
        logger.info(response)

        # モーダルで送信ボタンが押された時の処理
        @app.view("")
        def handle_create_task(ack, body, logger):
            # API通信に時間がかかるので、先にackを返す
            ack()
            logger.info(body)
            print("###"*10)
            print(body)
            try:
                task_name = body["view"]["state"]["values"]["input-title"]["input"][
                    "value"
                ]
                start_data = body["view"]["state"]["values"]["input-deadline"]["input"][
                    "selected_date"
                ]
                create_task(task_name=task_name, start_date=start_data)
                ack()
                app.client.chat_postMessage(
                    channel=os.getenv("SLACK_CHANNEL_ID"), text=f"{task_name} を作成しました！"
                )
            except Exception as e:
                logger.error(str(e))

    except Exception as e:
        print(e)


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
