from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from .models import *
from django.conf import settings
from yookassa import Configuration, Payment
import uuid
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
import hmac
import hashlib
import base64
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from decimal import Decimal
import logging
from django.contrib import messages
from .forms import RegistrationForm
from datetime import timedelta, datetime
from .models import Profile
from django.utils import timezone

logger = logging.getLogger(__name__)

# Инициализация YooKassa
Configuration.account_id = settings.YOOKASSA_SETTINGS['SHOP_ID']
Configuration.secret_key = settings.YOOKASSA_SETTINGS['SECRET_KEY']

class IndexView(ListView):
    template_name = 'membership/index.html'
    context_object_name = 'objects'
    
    def get_queryset(self):
        return []

class MembershipCardView(LoginRequiredMixin, TemplateView):
    template_name = 'membership/card.html'
    login_url = reverse_lazy('membership:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subscriptions = Subscription.objects.all()  # Получаем все подписки
        context['subscriptions'] = subscriptions
        return context

class MembershipLoginView(LoginView):
    template_name = 'membership/login.html'
    success_url = reverse_lazy('membership:card')
    
    def get_success_url(self):
        return self.success_url

@method_decorator(csrf_exempt, name='dispatch')
class PaymentCallbackView(View):
    def get(self, request, *args, **kwargs):
        try:
            logger.info("=== Payment return handler started ===")
            
            # Получаем ID платежа из сессии
            payment_id = request.session.get('pending_payment_id')
            logger.info(f"Payment ID from session: {payment_id}")
            
            if payment_id:
                # Проверяем статус платежа
                payment = Payment.find_one(payment_id)
                logger.info(f"Payment status: {payment.status}")
                
                if payment.status == 'succeeded':
                    # Получаем user_id из metadata
                    user_id = payment.metadata.get('user_id')
                    amount = Decimal(payment.amount.value)
                    
                    logger.info(f"Processing payment for user {user_id}, amount {amount}")
                    
                    # Обновляем баланс
                    profile = Profile.objects.get(user_id=user_id)
                    old_balance = profile.balance
                    profile.balance += amount
                    profile.save()
                    
                    logger.info(f"Balance updated: {old_balance} -> {profile.balance}")
                    
                    # Очищаем ID платежа из сессии
                    del request.session['pending_payment_id']
                    
                    messages.success(request, f'Оплата успешно проведена. Баланс пополнен на {amount} ₽')
                else:
                    logger.warning(f"Payment not succeeded: {payment.status}")
                    messages.warning(request, 'Платеж не был завершен')
            
            logger.info("=== Payment return handler finished ===")
            return redirect('membership:card')
            
        except Exception as e:
            logger.error(f"Error in payment return: {str(e)}")
            messages.error(request, 'Произошла ошибка при обработке платежа')
            return redirect('membership:card')

class ProcessPaymentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            amount = request.POST.get('amount')
            
            # Создаем идентификатор платежа
            payment_id = str(uuid.uuid4())
            
            payment_data = {
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.build_absolute_uri(
                        reverse_lazy('membership:payment_callback') + f'?payment_id={payment_id}'
                    )
                },
                "capture": True,
                "description": f"Оплата членского взноса для {request.user.email}",
                "metadata": {
                    "user_id": str(request.user.id),
                    "payment_id": payment_id
                }
            }
            
            logger.info(f"Creating payment with data: {payment_data}")
            payment = Payment.create(payment_data)
            logger.info(f"Payment created: {payment.id}")
            
            # Сохраняем ID платежа в сессии
            request.session['pending_payment_id'] = payment.id
            
            return JsonResponse({
                'status': 'success',
                'payment_url': payment.confirmation.confirmation_url
            })
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

class RegisterView(CreateView):
    template_name = 'membership/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('membership:login')

    def form_valid(self, form):
        # Сохранение формы с файлами
        form.save()
        return super().form_valid(form)

class ActivateSubscriptionView(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        subscription_cost = 1000  # Стоимость подписки
        payment_method = request.POST.get('payment_method')

        if payment_method == 'balance':
            if profile.balance >= subscription_cost:
                # Списываем деньги с баланса
                profile.balance -= subscription_cost
                profile.subscription_active = True  # Активируем подписку
                
                # Проверяем, инициализировано ли поле valid_until
                if profile.valid_until is None:
                    profile.valid_until = datetime.now()  # Устанавливаем на текущую дату, если None
                
                profile.valid_until += timedelta(days=365)  # Продлеваем на 1 год
                profile.save()
                messages.success(request, 'Подписка успешно активирована с баланса!')
            else:
                messages.error(request, 'Недостаточно средств на балансе для активации подписки.')
        elif payment_method == 'card':
            # Здесь можно добавить логику для оплаты картой
            messages.info(request, 'Вы выбрали оплату картой. Пожалуйста, используйте кнопку "Оплатить".')

        return redirect('membership:card')  # Перенаправление на страницу карточки

class RenewMembershipView(View):
    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        subscription_cost = 1000  # Стоимость подписки

        if profile.balance >= subscription_cost:
            # Списываем деньги с баланса
            profile.balance -= subscription_cost
            profile.valid_until = profile.valid_until + timedelta(days=365)  # Продлеваем на 1 год
            profile.subscription_active = True  # Активируем подписку
            profile.save()
            messages.success(request, 'Ваше членство успешно продлено!')
        else:
            messages.error(request, 'Недостаточно средств на балансе для продления членства.')

        return redirect('membership:card')  # Перенаправление на страницу карточки

class MembersListView(ListView):
    model = Profile
    template_name = 'membership/members_list.html'  # Укажите имя вашего шаблона
    context_object_name = 'members'

    def get_queryset(self):
        return Profile.objects.filter(valid_until__gte=timezone.now())  # Фильтруем только активные подписки

def membership_card(request):
    subscriptions = Subscription.objects.all()  # Получаем все подписки
    return render(request, 'membership/card.html', {'subscriptions': subscriptions})

def register_view(request):
    days = list(range(1, 32))  # Список дней от 1 до 31
    years = list(range(1900, 2023))  # Список годов от 1900 до 2022
    return render(request, 'membership/register.html', {
        'days': days,
        'years': years,
    })
