from django.contrib import admin
from .models import Subscription, Membership, PaymentInfo, Profile  # Импортируйте ваши модели

# Регистрация моделей в админке
admin.site.register(Subscription)
admin.site.register(Membership)
admin.site.register(PaymentInfo)
admin.site.register(Profile)