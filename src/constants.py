TASK_STATUS = {"not_started": "Not started", "progress": "In progress", "done": "Done"}

NOTION_MEMBERS = {
    "kusagi": "b07cd955-ae3f-418e-b24e-2495c07d2a42",
}

CREATE_TASK_VIEW = {
	"title": {
		"type": "plain_text",
		"text": "タスクの新規登録 :pencil:",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "送信",
		"emoji": True
	},
	"type": "modal",
	"close": {
		"type": "plain_text",
		"text": "キャンセル",
		"emoji": True
	},
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
					"emoji": True
				}
			},
			"label": {
				"type": "plain_text",
				"text": "件名",
				"emoji": True
			},
			"optional": False
		},
		{
			"type": "input",
			"block_id": "input-assignee",
			"element": {
				"type": "multi_users_select",
				"action_id": "input",
				"placeholder": {
					"type": "plain_text",
					"text": "担当するユーザを選択してください",
					"emoji": True
				}
			},
			"label": {
				"type": "plain_text",
				"text": "担当者",
				"emoji": True
			},
			"optional": True
		},
		{
			"type": "input",
			"block_id": "input-deadline",
			"element": {
				"type": "datepicker",
				"action_id": "input",
				"placeholder": {
					"type": "plain_text",
					"text": "日付を選択してください",
					"emoji": True
				}
			},
			"label": {
				"type": "plain_text",
				"text": "次回状況確認",
				"emoji": True
			},
			"optional": True
		},
		{
			"type": "input",
			"block_id": "input-description",
			"element": {
				"type": "plain_text_input",
				"action_id": "input",
				"multiline": True,
				"placeholder": {
					"type": "plain_text",
					"text": "できるだけ具体的に記入してください",
					"emoji": True
				}
			},
			"label": {
				"type": "plain_text",
				"text": "詳細",
				"emoji": True
			},
			"optional": True
		}
	]
}
