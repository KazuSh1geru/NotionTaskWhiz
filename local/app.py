import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv

load_dotenv()


# Install the Slack app and get xoxb- token in advance
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.command("/hello-socket-mode")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")


@app.event("app_mention")
def event_test(say):
    say("Hi there!")


if __name__ == "__main__":
    print(os.getenv("SLACK_BOT_TOKEN"))
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
