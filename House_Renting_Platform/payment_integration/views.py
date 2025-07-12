import requests
import uuid
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .models import Payment
from django.contrib import messages
import logging
from payment_integration import urls
is_payment_successful = False
# Set up logging
logger = logging.getLogger(__name__)

# Removed @login_required for testing (re-add when accounts is ready)
def checkout(request):
    if request.method == 'POST':
        amount = request.POST.get('amount', 1000)  # Default to 1000 ETB
        email = request.POST.get('email', 'betselotg87@gmail.com')  # Fallback email
        
        tx_ref = str(uuid.uuid4())

        payment = Payment.objects.create(
            user=None,  # Set to None for testing without authentication
            transaction_id=tx_ref,
            amount=amount,
            customer_email=email or None
        )

        payload = {
            'amount': str(amount),
            'currency': 'ETB',
            'email': email,
            'tx_ref': tx_ref,
            'callback_url': request.build_absolute_uri(reverse('payment_integration:payment_callback')),
            'return_url': request.build_absolute_uri(reverse('payment_integration:payment_success')),
            "phone_number": "0912345678",  # Placeholder phone number
            'first_name': 'Test',  # Placeholder
            'last_name': 'User',   # Placeholder
            'customization[title]': 'Listing Fee Payment',
            'customization[description]': 'Payment to list a property on House Renting Platform'

        }

        headers = {
            'Authorization': f'Bearer {settings.CHAPA_API_KEY}',
            'Content-Type': 'application/json'
        }

        try:
            logger.debug(f"Payload: {payload}")
            logger.debug(f"Headers: {headers}")
            response = requests.post(settings.CHAPA_API_URL, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get('status') == 'success':
                checkout_url = response_data['data']['checkout_url']
                return redirect(checkout_url)
            else:
                logger.error(f"Chapa error response: {response.text}")
                messages.error(request, 'Failed to initialize payment. Please try again.')
                return render(request, 'payment_integration/checkout.html', {'amount': amount})

        except Exception as e:
            logger.error(f"Payment initialization failed: {str(e)}")
            messages.error(request, f'Unexpected error: {str(e)}. Please try again.')
            return render(request, 'payment_integration/checkout.html', {'amount': amount})


    return render(request, 'payment_integration/checkout.html', {'amount': 1000})

def payment_callback(request):
    global is_payment_successful
    tx_ref = request.GET.get('tx_ref')
    if tx_ref:
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            headers = {'Authorization': f'Bearer {settings.CHAPA_API_KEY}'}
            response = requests.get(f"{settings.CHAPA_VERIFY_URL}{tx_ref}", headers=headers)
            response_data = response.json()

            if response_data.get('status') == 'success':
                payment.status = 'success'
                is_payment_successful = True
                payment.save()
            else:
                payment.status = 'failed'
                is_payment_successful = False
                payment.save()
        except Payment.DoesNotExist:
            pass

    return redirect('Listing:new-property' if payment.status == 'success' else 'payment_failure')

def payment_success(request):
    return render(request, 'payment_integration/success.html')

def payment_failure(request):
    return render(request, 'payment_integration/failure.html')