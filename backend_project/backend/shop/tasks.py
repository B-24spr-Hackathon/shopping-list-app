from backend.celery import app
from django.utils import timezone
from django.conf import settings
from django.db.models import Prefetch
from datetime import timedelta
import requests, calendar
from shop.models import User, List, Item


# リクエストに必要なデータ
url = settings.PUSH_URL
token = settings.CHANNEL_ACCESS_TOKEN
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}


"""
remind_batch
毎日定時にDBからデータを取得し開封確認通知を送るタスクを呼出す
"""
@app.task
def remind_batch():
    # 現在の日にちを取得
    today_datetime = timezone.now()
    today = today_datetime.date()

    # 通知対象のユーザーとそのユーザーの持つ通知対象となるアイテムを抽出
    # アイテムの取得条件のクエリセット
    item_queryset = Item.objects.filter(
        to_list=False,
        remind_by_item=True,
        manage_target=True)

    # アイテムをPrefetch
    item_prefetch = Prefetch("items", queryset=item_queryset,
                             to_attr="item_list")

    # リストのクエリセット
    list_queryset = List.objects.prefetch_related(item_prefetch)

    # リストの紐づけてアイテムをPrefetch
    list_prefetch = Prefetch("list_set", queryset=list_queryset,
                             to_attr="lists")

    # 通知対象となるユーザーを取得し、紐づくアイテムをPrefetch
    users = User.objects.filter(
        line_status=True,
        have_list=True,
        remind=True).prefetch_related("list_set", list_prefetch)

    # データをまとめる
    user_items = []
    for user in users:
        user_item = {
            "line_id": user.line_id,
            "remind_timing": user.remind_timing,
            "remind_time": user.remind_time
        }
        list_items = []
        for list in user.lists:
            for item in list.item_list:
                item_attr = {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "consume_cycle": item.consume_cycle,
                    "last_open_at": item.last_open_at
                }
                list_items.append(item_attr)
        user_item["items"] = list_items
        user_items.append(user_item)

    # まとめたデータよりユーザー毎に通知送信のタスクを実行
    for remind_user in user_items:
        remind_items = []
        for remind_item in remind_user["items"]:
            # アイテムの通知日時を算出（最終開封日+消費頻度+通知タイミング）
            remind_date = remind_item["last_open_at"] + timedelta(days=(remind_item["consume_cycle"] + remind_user["remind_timing"]))

            # 今日が通知日時よりも後の場合
            if today >= remind_date:
                remind_items.append({
                    "item_id": remind_item["item_id"],
                    "item_name": remind_item["item_name"]
                })

        # 通知時間（秒）の設定
        remind_time = (remind_user["remind_time"].hour * 3600) + (remind_user["remind_time"].minute * 60)
        batch_time = (settings.BATCH_HOUR * 3600) + (settings.BATCH_MINUTE * 60)
        count = remind_time - batch_time
        # 通知時間がバッチ処理時間よりも早い場合
        if count < 0:
            count += 24 * 3600

        # remind_itemsが空じゃない場合
        if len(remind_items) > 0:
            # 通知送信のタスクを呼出し
            remind_request.apply_async([remind_user["line_id"], remind_items], countdown=count)


"""
shopping_batch
毎日定時にDBからデータを取得し買い物日前日の通知を送るタスクを呼出す
"""
@app.task
def shopping_batch():
    today = timezone.now()
    year = today.year
    month = today.month
    day = today.day
    time = today.time()

    # 今月の最終日を取得
    _, last_day = calendar.monthrange(year, month)

    # 通知対象となるユーザーを通知時間のタイミング毎に取得
    # early: 通知時間がバッチ処理より早い　normal: それ以外
    early_users = User.objects.filter(remind=True, remind_time__lt=time)
    normal_users = User.objects.filter(remind=True, remind_time__gte=time)

    # normal_usersの処理
    # 今日が今月最終日の場合は買い物日が1のユーザーを取得
    if day == last_day:
        users = normal_users.filter(list__shopping_day=1).exclude(list__shopping_day=None).distinct()

    # 今日が今月最終日前日の場合は買い物日が月末のユーザーを取得
    elif day == last_day - 1:
        users = normal_users.filter(list__shopping_day__gt=day).exclude(list__shopping_day=None).distinct()

    # 今日が上記以外の場合は買い物日が翌日のユーザーを取得
    else:
        day += 1
        users = normal_users.filter(list__shopping_day=day).exclude(list__shopping_day=None).distinct()

    # ユーザーを取出してshopping_requestを呼出す
    for user in users:
        # 通知時間（秒）の設定
        remind_time = (user.remind_time.hour * 3600) + (user.remind_time.minute * 60)
        batch_time = (settings.BATCH_HOUR * 3600) + (settings.BATCH_MINUTE * 60)
        count = remind_time - batch_time
        # 通知時間がバッチ処理時間と同じ場合（10秒後に通知）
        if count == 0:
            count = 10

        # 非同期で通知を送る関数を呼出す
        shopping_request.apply_async([user.line_id], countdown=count)

    # early_usersの処理
    # 今日が今月最終日の前日の場合は買い物日が1のユーザーを取得
    if day == last_day - 1:
        users = early_users.filter(list__shopping_day=1).exclude(list__shopping_day=None).distinct()

    # 今日が今月最終日の2日前の場合は買い物日が月末のユーザーを取得
    elif day == last_day - 2:
        day += 1
        users = early_users.filter(list__shopping_day__gt=day).exclude(list__shopping_day=None).distinct()
    # 今日が上記以外の場合は買い物日が2日後のユーザーを取得
    else:
        day += 2
        users = early_users.filter(list__shopping_day=day).exclude(list__shopping_day=None).distinct()

    # ユーザーを取出してshopping_requestを呼出す
    for user in users:
        # 通知時間（秒）の設定
        remind_time = (user.remind_time.hour * 3600) + (user.remind_time.minute * 60)
        batch_time = (settings.BATCH_HOUR * 3600) + (settings.BATCH_MINUTE * 60)
        count = (24 * 3600) - remind_time - batch_time

        # 非同期で通知を送る関数を呼出す
        shopping_request.apply_async([user.line_id], countdown=count)


"""
remind_request
LINEにPOSTリクエストを送信するタスク
買い物リスト追加を促す通知
"""
@app.task
def remind_request(line_id, items):
    # itemsが複数の場合
    if len(items) > 1:
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
                            "data": item["item_id"],
                        },
                        {
                            "type": "postback",
                            "label": "追加しない",
                            "data": item["item_name"],
                        },
                    ],
                }
                messages["template"]["columns"].append(columns)
                count += 1

            data["messages"].append(messages)

    # itemsが1つの場合
    else:
        item = items[0]
        data = {
            "to": line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "buttons",
                        "text": f"{item['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "追加する",
                                "data": item["item_id"],
                            },
                            {
                                "type": "postback",
                                "label": "追加しない",
                                "data": item["item_name"],
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
