from django.contrib import admin
from .models import Transaction, CreditCard
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'status', 'transaction_type', 'receiver', 'sender']
    list_display = ['user', 'amount', 'status', 'transaction_type', 'receiver', 'sender']

class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ['amount', 'card_type']
    list_display = ['user', 'amount', 'card_type']


admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)