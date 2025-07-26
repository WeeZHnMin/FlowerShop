from django.db import models
from django.conf import settings
from products.models import Flower

class Order(models.Model):
    """订单模型"""
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('processing', '处理中'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    ORDER_TYPE_CHOICES = (
        ('immediate', '立即购买'),
        ('booking', '预订'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="用户")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价格")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    shipping_address = models.TextField(verbose_name="收货地址")
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='immediate', verbose_name="订单类型")
    booking_date = models.DateTimeField(blank=True, null=True, verbose_name="预订日期")
    delivery_date = models.DateTimeField(blank=True, null=True, verbose_name="配送日期")
    special_requirements = models.TextField(blank=True, null=True, verbose_name="特殊要求")
    recipient_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="收件人姓名")
    recipient_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="收件人电话")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return f"订单 {self.id} - {self.user.username}"

class OrderItem(models.Model):
    """订单项模型"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="订单")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, related_name='order_items', verbose_name="花卉")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")

    class Meta:
        verbose_name = "订单项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"