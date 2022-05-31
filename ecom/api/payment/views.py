from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree
# Create your views here.
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="827h7kczn6ydtst3",
        public_key="9r73wk7p8x386kz3",
        private_key="64f7c129e9f8e57538a246b53bbd946b"
    )
)

def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user =  UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False  
    except UserModel.DoesNotExist:
        return False

@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid session,Please login again'})

    return JsonResponse({'client':gateway.client_token.generate(), 'success': True})


@csrf_exempt
def process_payment(request, id,token):
    if not validated_user_session(id, token):
        return JsonResponse({'error':'Invalid session,Please login again'})

    nonce_from_the_client = request.POST["paymentMethodNonce"]
    amount_from_the_client = request.POST["amount"]

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({
            "success":result.is_success,
            "transaction": {'id':result.transaction.id,'amount':result.transaction.amount}})

    else:
        return JsonResponse({'error':True,'success':False})
    