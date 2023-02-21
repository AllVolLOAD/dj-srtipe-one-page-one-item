import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Item
from django.views.generic import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY

class BuyView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        product = Item.objects.get(id=1)
        context = super(BuyView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):


    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Item.objects.get(id=product_id)
        data = json.loads(request.body)
        sum_price = data.get('its_prise')
        sum_quantity = data.get('its_counter')
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name
                        },
                    },
                    'quantity': sum_quantity,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
