from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from account.models import Account
from .models import Transaction

@login_required
def get_transactions_list(request):
    sender_transaction = Transaction.objects.filter(sender=request.user).order_by("-id")
    receiver_transaction = Transaction.objects.filter(receiver=request.user).order_by("-id")

    context = {
        'sender_transaction':sender_transaction,
        'reciever_transaction':receiver_transaction,

    }
    return render(request, "transaction/transaction-list.html", context)

@login_required
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        'transaction':transaction,

    }
    return render(request, "transaction/transaction-detail.html", context)