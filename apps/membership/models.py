from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.

class Subscription(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    duration_days = models.PositiveIntegerField(verbose_name="Длительность (дней)")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name="Подписка")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Дата начала")
    end_date = models.DateTimeField(default=timezone.now, verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    payment_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID платежа")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Членство"
        verbose_name_plural = "Членства"

    def __str__(self):
        return f"{self.user.username} - {self.subscription.name}"

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.subscription.duration_days)
        super().save(*args, **kwargs)

class PaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    payment_type = models.CharField(max_length=50, default='membership')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Информация оп платежах"
        verbose_name_plural = "Информация оп платежах"

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_until = models.DateTimeField(null=True, blank=True)
    membership_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    # Новые поля
    education = models.CharField(max_length=255, blank=True, null=True, verbose_name="Образование")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Profile for {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
