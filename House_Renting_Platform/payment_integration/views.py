import requests
import uuid
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .models import Payment
from django.contrib import messages
import logging
from payment_integration import urls
import json
from requests.exceptions import RequestException, ConnectionError, HTTPError

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

        request.session['current_payment_tx_ref'] = tx_ref
        request.session.set_expiry(100)

        payload = {
            'amount': str(amount),
            'currency': 'ETB',
            'email': email,
            'tx_ref': tx_ref,
            'callback_url': request.build_absolute_uri(reverse('payment_integration:payment_callback')),
            'return_url': request.build_absolute_uri(reverse('payment_integration:payment_callback')),
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
                request.session['is_payment_successfull'] = "True"
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
    tx_ref = request.session['current_payment_tx_ref']

    logger.debug(f"Payment callback received. GET params: {request.GET}")
    logger.debug(f"Extracted tx_ref: {tx_ref}")

    if not tx_ref:
        logger.warning("Payment callback received without 'trx_ref' parameter in GET. Redirecting to failure.")
        messages.error(request, "Payment confirmation failed: Missing transaction reference from gateway.")
        return redirect(reverse('payment_integration:payment_failure') + '?status=missing_ref')

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
        logger.info(f"Processing callback for payment {tx_ref}. Current DB status: {payment.status}")

        if payment.status == 'success':
            messages.info(request, "This payment has already been confirmed as successful.")
            request.session['payment_status'] = 'success'
            request.session.set_expiry(200)
            return redirect(reverse('Listing:new-property') + '?payment_status=already_success&tx_ref=' + tx_ref)
        
        elif payment.status == 'failed':
            logger.warning(f"Payment {tx_ref} was previously marked as failed. Re-verifying as requested...")

        headers = {
            'Authorization': f'Bearer {settings.CHAPA_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.get(
            f"{settings.CHAPA_VERIFY_URL}{tx_ref}", 
            headers=headers,
            timeout=15
        )
        response.raise_for_status() 
        response_data = response.json()
        logger.debug(f"Chapa verification API response for {tx_ref}: {response_data}")

        if response_data.get('status') == 'success':
            payment.status = 'success'
            payment.gateway_transaction_id = response_data.get('data', {}).get('id')
            payment.gateway_response = response_data 
            payment.save()
            logger.info(f"Payment {tx_ref} successfully verified and updated to 'success'.")
            request.session['payment_status'] = 'success'
            return redirect(reverse('Listing:new-property') + '?payment_status=success&tx_ref=' + tx_ref)
        else:
            chapa_message = response_data.get('message', 'Payment verification failed.')
            payment.status = 'failed'
            payment.gateway_response = response_data
            payment.save()
            logger.warning(f"Chapa verification for {tx_ref} returned non-success status: '{response_data.get('status')}'. Message: {chapa_message}")
            messages.error(request, f"Your payment failed: {chapa_message}. Please try again.")
            return redirect(reverse('payment_integration:payment_failure') + '?payment_status=failed&tx_ref=' + tx_ref)

    except Payment.DoesNotExist:
        logger.error(f"Payment with transaction_id '{tx_ref}' not found in database during Chapa callback.", exc_info=True)
        messages.error(request, "Payment confirmation failed: The transaction could not be found in our records.")
        return redirect(reverse('payment_integration:payment_failure') + '?payment_status=not_found&tx_ref=' + tx_ref)
    
    except RequestException as e:
        logger.error(f"An unexpected requests error occurred for tx_ref {tx_ref}: {e}", exc_info=True)
        messages.error(request, "An unexpected error occurred during payment verification. Please try again.")
        if 'payment' in locals() and payment.status != 'failed':
            payment.status = 'failed'
            payment.gateway_response = {'error': 'RequestException', 'message': str(e)}
            payment.save()
        return redirect(reverse('payment_integration:payment_failure') + '?payment_status=request_error&tx_ref=' + tx_ref)
    
    except Exception as e:
        logger.critical(f"An unhandled error occurred in payment_callback for tx_ref {tx_ref}: {e}", exc_info=True)
        messages.error(request, "An internal error occurred. Please contact support.")
        if 'payment' in locals() and payment.status != 'failed':
            payment.status = 'failed'
            payment.gateway_response = {'error': 'Unhandled error', 'message': str(e)}
            payment.save()
        return redirect(reverse('payment_integration:payment_failure') + '?payment_status=internal_error&tx_ref=' + tx_ref)

def payment_success(request):
    return render(request, 'payment_integration/success.html')

def payment_failure(request):
    return render(request, 'payment_integration/failure.html')