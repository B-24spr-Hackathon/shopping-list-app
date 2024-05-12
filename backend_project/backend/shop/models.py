from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, user_id, email, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The given user_id must be set')
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_id, email, password, **extra_fields)
    
# Create your models here.
REMIND_TIMING_CHOICES = [(i, i) for i in range(1, 11)]
SHOPPING_DAY = [(i, i) for i in range(1, 31)]
# フロントエンドからのカラー設定連絡待ち
COLOR_CHOICES = [(0, '赤'), (1, 'ピンク'), (2, 'オレンジ'),(3, '黄'), (4, '黄緑'), (5, '緑'),(6, '水色'), (7, '青'), (8, '薄紫'),(9, '紫'), (10, 'グレー'),]
MEMBER_STATUS_CHOICES = [(0, '追加済み'), (1, '招待中'), (2,'申請中')]

class User(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    # password = models.CharField(max_length=128)
    # AbstractUserがもともと持っているusernameフィールドは使わない(除外せず、空白可としておく)
    username = models.CharField(max_length=50, blank=True, null=True)

    line_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    line_status = models.BooleanField(default=False)
    user_icon = models.CharField(max_length=100, blank=True, null=True)
    invitation = models.BooleanField(default=False)
    request = models.BooleanField(default=False)
    have_list = models.BooleanField(default=False)
    default_list = models.BooleanField(default=True)
    remind = models.BooleanField(default=False)
    remind_timing = models.IntegerField(choices=REMIND_TIMING_CHOICES,  blank=True, null=True)    
    remind_time = models.TimeField(blank=True, null=True)

    objects = UserManager()

    # ユーザーを一意に識別するフィールド
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.user_id


class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner_id')
    list_name = models.CharField(max_length=50)
    shopping_day = models.IntegerField(choices=SHOPPING_DAY, blank=True, null=True)

    class Meta:
        db_table = 'lists'
    def __str__(self):
        return self.list_name

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='members', db_column='list_id')
    invitee_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='invitee_id')
    authority = models.BooleanField(default=False)
    status = models.IntegerField(choices=MEMBER_STATUS_CHOICES, blank=False, null=False)

    class Meta:
        db_table = 'members'
    def __str__(self):
        return self.invitee_id.user_name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50) 
    list_id = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items', db_column='list_id')
    color = models.IntegerField(choices=COLOR_CHOICES, blank=True, null=True)
    consume_cycle = models.IntegerField(default=30)
    last_purchase_at = models.DateField(blank=True, null=True)
    last_open_at = models.DateField(blank=True, null=True)
    item_url = models.CharField(max_length=255, blank=True, null=True)
    to_list = models.BooleanField(default=False,blank=True, null=True)
    remind_by_item = models.BooleanField(default=False)
    manage_target = models.BooleanField(default=True)

    class Meta:
        db_table = 'items'           
    def __str__(self):
        return self.item_name
