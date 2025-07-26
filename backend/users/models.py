from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', '店主'),
        ('customer', '客户'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name='角色')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name='手机号')
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='邮箱')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00, verbose_name='余额')

    def __str__(self):
        return self.username