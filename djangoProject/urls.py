from django import views
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from paysystem.views import CreateCheckoutSessionView, SuccessView, CancelView, BuyView

urlpatterns = [
    path('item/1/', BuyView.as_view(), name='buy'),
    path('admin/', admin.site.urls),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('buy/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
