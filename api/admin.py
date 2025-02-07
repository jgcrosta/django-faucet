from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet_address", "amount", "status", "created_at", "ip_address")
    list_filter = ("status", "created_at")
    search_fields = ("wallet_address", "ip_address")
