from django.urls import path
from . import views
from .views import RenewMembershipView, ActivateSubscriptionView, MembersListView

app_name = 'membership'

urlpatterns = [
    path('', views.MembershipCardView.as_view(), name='card'),
    path('login/', views.MembershipLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('process-payment/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('payment-callback/', views.PaymentCallbackView.as_view(), name='payment_callback'),
    path('renew_membership/', RenewMembershipView.as_view(), name='renew_membership'),
    path('activate_subscription/', ActivateSubscriptionView.as_view(), name='activate_subscription'),
    path('members/', MembersListView.as_view(), name='members_list'),
]
