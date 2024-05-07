from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
REMIND_TIMING_CHOICES = [(i, i) for i in range(1, 11)]
SHOPPING_CYCLE_CHOICES = [(0,'毎月'), (1,'隔週'), (2,'毎週'),]
SHOPPING_DAY = [(i, i) for i in range(1, 31)]
DAY_OF_WEEK = [(0,'月'), (1,'火'), (2,'水'), (3,'木'), (4,'金'), (5,'土'), (6,'日'),]
# フロントエンドからのカラー設定連絡待ち
COLOR_CHOICES = [(0, '赤'), (1, '青'), (2, '緑')]

class User(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    # password = models.CharField(max_length=128)
    # AbstractUserがもともと持っているusernameフィールドは使わない(除外せず、空白可としておく)
    username = models.CharField(max_length=50, blank=True, null=True)

    line_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    user_icon = models.CharField(max_length=100, blank=True, null=True)
    invitation = models.BooleanField(default=False)
    request = models.BooleanField(default=False)
    have_list = models.BooleanField(default=False)
    default_list = models.BooleanField(default=True)
    remind = models.BooleanField(default=False)
    remind_timing = models.IntegerField(choices=REMIND_TIMING_CHOICES,  blank=True, null=True)    
    remind_time = models.TimeField( blank=True, null=True)

    # ユーザーを一意に識別するフィールド
    USERNAME_FIELD = 'user_id'    
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.user_id


class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=50)
    shopping_cycle = models.IntegerField(choices=SHOPPING_CYCLE_CHOICES,  default=0)
    shopping_day = models.IntegerField(choices=SHOPPING_DAY, blank=True, null=True)
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK, blank=True, null=True)

    class Meta:
        db_table = 'lists'
    def __str__(self):
        return self.list_name

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='members')
    invitee_id = models.ForeignKey(User, on_delete=models.CASCADE)
    authority = models.BooleanField(default=False)

    class Meta:
        db_table = 'members'
    def __str__(self):
        return self.invitee_id.user_name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50) 
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    color = models.IntegerField(choices=COLOR_CHOICES, blank=True, null=True)
    consume_cycle = models.IntegerField(default=30)
    last_purchase_at = models.DateField(blank=True, null=True)
    last_open_at = models.DateField(blank=True, null=True)
    item_url = models.CharField(max_length=255, blank=True, null=True)
    to_list = models.BooleanField(default=False,blank=True, null=True)
    remind_by_item = models.BooleanField(default=True)
    manage_target = models.BooleanField(default=True)

    class Meta:
        db_table = 'items'           
    def __str__(self):
        return self.item_name
