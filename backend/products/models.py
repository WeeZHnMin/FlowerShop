from django.db import models
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.conf import settings

class Flower(models.Model):
    BOUQUET_TYPE_CHOICES = (
        ('single', '单支花'),
        ('small', '小花束'),
        ('medium', '中花束'),
        ('large', '大花束'),
        ('luxury', '豪华花束'),
    )
    
    SIZE_CHOICES = (
        ('mini', '迷你型'),
        ('small', '小型'),
        ('medium', '中型'),
        ('large', '大型'),
        ('extra_large', '特大型'),
    )
    
    name = models.CharField(max_length=100, verbose_name="花卉名称")
    usage = models.CharField(max_length=255, blank=True, null=True, verbose_name="用途")
    season = models.CharField(max_length=255, blank=True, null=True, verbose_name="季节")
    origin = models.CharField(max_length=100, blank=True, null=True, verbose_name="产地")
    flower_language = models.CharField(max_length=255, blank=True, null=True, verbose_name="花语")
    care_requirements = models.TextField(blank=True, null=True, verbose_name="养护要求")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存数量")
    image = models.ImageField(upload_to='flowers/', blank=True, null=True, verbose_name="图片")
    bouquet_type = models.CharField(max_length=20, choices=BOUQUET_TYPE_CHOICES, default='single', verbose_name="花束类型")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='medium', verbose_name="花束大小")
    is_available_for_booking = models.BooleanField(default=True, verbose_name="可预订")

    class Meta:
        verbose_name = "花卉"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            pil_img = Image.open(self.image)
            target_size = (800, 600)
            width, height = pil_img.size
            target_ratio = target_size[0] / target_size[1]
            current_ratio = width / height
            if current_ratio > target_ratio:
                new_height = target_size[1]
                new_width = int(new_height * current_ratio)
                pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                left = (new_width - target_size[0]) / 2
                top = 0
                right = left + target_size[0]
                bottom = new_height
                pil_img = pil_img.crop((left, top, right, bottom))
            else:
                new_width = target_size[0]
                new_height = int(new_width / current_ratio)
                pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                left = 0
                top = (new_height - target_size[1]) / 2
                right = new_width
                bottom = top + target_size[1]
                pil_img = pil_img.crop((left, top, right, bottom))
            buffer = BytesIO()
            pil_img.save(buffer, format='JPEG', quality=90)
            buffer.seek(0)
            self.image.save(self.image.name, ContentFile(buffer.read()), save=False)
        super().save(*args, **kwargs)

class Medicine(models.Model):
    """药品信息模型"""
    name = models.CharField(max_length=100, verbose_name="药品名称")
    symptoms = models.TextField(verbose_name="适用病虫害症状")

    class Meta:
        verbose_name = "药品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'Like by {self.user} on {self.post}'
