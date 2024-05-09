from celery import Celery
import os

# Djangoの設定ファイルを指定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("message")

# celeryの設定ソースとしてDjangoのsettingsモジュールを追加
app.config_from_object("django.conf:settings", namespace="CELERY")

# 登録されているDjangoアプリからタスクモジュールを読込み
app.autodiscover_tasks()