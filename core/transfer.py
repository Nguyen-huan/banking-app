from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

from .models import Transaction
from account.models import Account

@login_required
def search_users_account_number(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")
    if query:
        account = Account.objects.filter(
            Q(account_number=query) | Q(account_id=query)
        ).distinct()
    context = {
        'account':account,
        "query":query
    }
    return render(request, "transfer/search-user.html", context)

def amount_transfer(request, amount_number):
    try:
        account = Account.objects.get(account_number=amount_number)
    except:
        account = None
        messages.warning(request, "Account number does not exist!")
        return redirect("core:search-account")
    context = {
        'account':account
    }
    return render(request, "transfer/amount-transfer.html", context)

@login_required
def amount_transfer_proccess(request, account_number):
    account = Account.objects.get(account_number=account_number)

    sender = request.user
    receiver = account.user

    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")
        if sender_account.account_balance >= Decimal(amount) and Decimal(amount) > 0:
            new_transaction = Transaction.objects.create(
                user = request.user,
                amount = amount,
                description = description,
                receiver = receiver,
                sender = sender,
                sender_account = sender_account,
                receiver_account = receiver_account,
                status = "processing",
                transaction_type="transfer"
            )
            new_transaction.save()
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "Insufficient fund!")
            return redirect("core:amount-transfer", account.account_number)
    else:
        messages.warning(request, "Error Occured! Try again later!")
        return redirect("account:account")

@login_required
def transfer_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        if transaction.status == "completed":
            messages.warning(request, "You cannot make this transaction")
            return redirect("account:dashboard")
    except:
        messages.warning(request, "Transaction does not exist!")
        return redirect("account:account")
    context = {
        'account':account,
        'transaction':transaction
    }

    return render(request, 'transfer/transfer-confirmation.html', context)

@login_required
def transfer_proccess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user
    receiver = account.user

    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            sender_account.account_balance -= transaction.amount
            sender_account.save()

            receiver_account.account_balance += transaction.amount
            receiver_account.save()

            messages.success(request, "Transfer Successfully")
            return redirect("core:transfer-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Inconnect Pin Number", )
            return redirect("core:transfer-confirmation",account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An Occured, Try again")
        return redirect("account:account")

@login_required
def transfer_completed(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist!")
        return redirect("account:account")
    context = {
        'account':account,
        'transaction':transaction
    }

    return render(request, 'transfer/transfer-completed.html', context)