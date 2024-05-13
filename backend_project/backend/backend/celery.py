import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Djangoの設定ファイルを指定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

# celeryの設定ソースとしてDjangoのsettingsモジュールを追加
app.config_from_object("django.conf:settings", namespace="CELERY")

# Celery Beatによるバッチ処理のスケジュール
app.conf.beat_schedule = {
    "shopping-batch": {
        "task": "shop.tasks.shopping_batch",
        "schedule": crontab(hour=(settings.BATCH_TIME), minute=0),
    },
    "remind-batch": {
        "task": "shop.tasks.remind_batch",
        "schedule": crontab(hour=settings.BATCH_TIME, minute=0),
    },
}

# 登録されているDjangoアプリからタスクモジュールを読込み
app.autodiscover_tasks()
