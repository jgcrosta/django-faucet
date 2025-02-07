from django.db import models


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    wallet_address = models.CharField(max_length=42)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(
        max_length=20, choices=[("SUCCESS", "Success"), ("FAILED", "Failed")]
    )

    def __str__(self):
        return f"{self.wallet_address} - {self.amount} - {self.status}"
