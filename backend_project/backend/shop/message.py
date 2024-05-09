from backend.backend.celery import app
from django.conf import settings
import requests


# リクエストに必要なデータ
url = settings.PUSH_URL
token = settings.CHANNEL_ACCESS_TOKEN
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

"""
batch_task
毎日定時にDBからデータを取得しLINEに通知を送る処理を呼出す
"""
@app.task
def batch_task():
    return


"""
remind_request
LINEにPOSTリクエストを送信するタスク
買い物リスト追加を促す通知
"""
@app.task
def remind_request(line_id, items):
    # itemsが複数（リスト)の場合
    if type(items) == list:
        # 1度のメッセージで送信できるアイテム数は10
        # 1度のリクエストで送信できるメッセージ数は5
        message_num = (len(items) // 10) + 1

        data = {"to": line_id, "messages": []}

        for i in range(message_num):
            messages = {
                "type": "template",
                "altText": "開封確認",
                "template": {"type": "carousel", "columns": []},
            }
            count = 0
            for j in range(len(items) - (i * 10)):
                if count == 10:
                    break

                item = items[(i * 10) + j]
                columns = {
                    "text": f"{item['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                    "actions": [
                        {
                            "type": "postback",
                            "label": "追加する",
                            "data": "to_list=true",
                        },
                        {
                            "type": "postback",
                            "label": "追加しない",
                            "data": "to_list=false",
                        },
                    ],
                }
                messages["template"]["columns"].append(columns)
                count += 1

            data["messages"].append(messages)

    # itemsが1つの場合
    else:
        data = {
            "to": line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "buttons",
                        "text": f"{items.item_name}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "追加する",
                                "data": "to_list=true",
                            },
                            {
                                "type": "postback",
                                "label": "追加しない",
                                "data": "to_list=false",
                            },
                        ],
                    },
                },
            ],
        }

    # 通知を送信
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"{line_id}への開封通知を適切に送信しました")
    else:
        print(f"{line_id}への開封通知に失敗しました")


"""
shopping_request
LINEにPOSTリクエストを送信するタスク
買い物日前日の通知
"""
@app.task
def shopping_request(line_id, date):
    data = {
        "to": line_id,
        "messages": [
            {
                "type": "template",
                "altText": "買い物日通知",
                "template": {
                    "type": "buttons",
                    "text": f"{date}は買い物予定日です！",
                    "actions": [
                        {
                            "type": "uri",
                            "label": "買い物リストを表示する",
                            "uri": settings.SHOPPING_LIST_URL,
                        }
                    ]
                }
            }
        ]
    }

    # 通知を送信
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"{line_id}への買い物日通知を適切に送信しました")
    else:
        print(f"{line_id}への買い物日通知に失敗しました")