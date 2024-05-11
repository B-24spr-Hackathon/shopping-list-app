from backend.backend.celery import app
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
import requests, calendar
from shop.models import User


# リクエストに必要なデータ
url = settings.PUSH_URL
token = settings.CHANNEL_ACCESS_TOKEN
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

"""
shopping_batch
毎日定時にDBからデータを取得し買い物日前日の通知を送るタスクを呼出す
"""
@app.task
def shopping_batch():
    # 買い物日を通知するタスクを呼出す
    today = timezone.now()
    year = today.year
    month = today.month
    day = today.day

    # 今月の最終日を取得
    _, last_day = calendar.monthrange(year, month)

    # 今日が今月最終日に場合は買い物日が1のユーザーを取得
    if day == last_day:
        users = User.objects.raw("""
            SELECT u.line_id, u.remind_time FROM users AS u
            INNER JOIN lists AS l ON u.user_id = l.owner_id
            WHERE u.remind = 1 AND l.shopping_day = 1;
            """)
    # 今日が今月最終日前日の場合は買い物日が月末のユーザーを取得
    elif day == last_day - 1:
        users = User.objects.raw("""
            SELECT u.line_id, u.remind_time FROM users AS u
            INNER JOIN lists AS l ON u.user_id = l.owner_id
            WHERE u.remind = 1 AND l.shopping_day > %s;
            """, [day])
    # 今日が上記以外の場合は買い物日が翌日のユーザーを取得
    else:
        day += 1
        users = User.objects.raw("""
            SELECT u.line_id, u.remind_time FROM users AS u
            INNER JOIN lists AS l ON u.user_id = l.owner_id
            WHERE u.remind = 1 AND l.shopping_day = %s;
            """, [day])

    # ユーザーを取出してshopping_requestを呼出す
    for user in users:
        # 通知時間の設定
        hour = user.remind_time - settings.BATCH_TIME
        if hour < 0:
            hour += 24
        count = hour * 3600

        shopping_request.apply_async(args=[user.line_id], countdown=count)


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
    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception:
        print(f"{line_id}への開封通知でネットワークエラー発生")

    if response.ok:
        print(f"{line_id}への開封通知を適切に送信しました")
    else:
        print(f"{line_id}への開封通知に失敗しました")


"""
shopping_request
LINEにPOSTリクエストを送信するタスク
買い物日前日の通知
"""
@app.task
def shopping_request(line_id):
    data = {
        "to": line_id,
        "messages": [
            {
                "type": "template",
                "altText": "買い物日通知",
                "template": {
                    "type": "buttons",
                    "text": "明日は買い物予定日です！",
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
    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception:
        print(f"{line_id}への買い物日通知でネットワークエラー発生")

    if response.ok:
        print(f"{line_id}への買い物日通知を適切に送信しました")
    else:
        print(f"{line_id}への買い物日通知に失敗しました")
