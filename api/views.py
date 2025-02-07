from decimal import Decimal
import logging
import os
from rest_framework.decorators import api_view
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from web3 import Web3
from .models import Transaction
from .serializer import FundRequestSerializer, StatsSerializer

logger = logging.getLogger("api")

w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
ETH_AMOUNT = Decimal(os.getenv("ETH_AMOUNT", "0.0001"))
RATE_LIMIT = os.getenv("RATE_LIMIT", "1")


@api_view(["POST"])
@ratelimit(key="ip", rate=f"{RATE_LIMIT}/m")
@ratelimit(key="post:wallet_address", rate=f"{RATE_LIMIT}/m")
def fund(request):
    logger.info(f"Fund request received from {request.META.get('REMOTE_ADDR')}")

    serializer = FundRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    wallet_address = serializer.validated_data["wallet_address"]
    ip_address = request.META.get("REMOTE_ADDR")

    try:
        # Prepare transaction
        nonce = w3.eth.get_transaction_count(
            w3.eth.account.from_key(WALLET_PRIVATE_KEY).address
        )
        transaction = {
            "nonce": nonce,
            "to": wallet_address,
            "value": w3.to_wei(ETH_AMOUNT, "ether"),
            "gas": 21000,
            "gasPrice": w3.eth.gas_price,
            "chainId": 11155111,
        }
        # Sign and send transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        Transaction.objects.create(
            wallet_address=wallet_address,
            ip_address=ip_address,
            amount=ETH_AMOUNT,
            status="SUCCESS",
        )

        logger.info(f"Fund request sent to {wallet_address} with amount {ETH_AMOUNT}")
        return Response({"transaction_hash": tx_hash.hex()})
    except Exception as e:
        Transaction.objects.create(
            wallet_address=wallet_address,
            ip_address=ip_address,
            amount=ETH_AMOUNT,
            status="FAILED",
        )
        logger.error(f"Fund request failed for {wallet_address}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def stats(request):
    logger.info("Stats request received")
    last_24h = timezone.now() - timedelta(days=1)

    successful_transactions = Transaction.objects.filter(
        status="SUCCESS", created_at__gte=last_24h
    ).count()

    failed_transactions = Transaction.objects.filter(
        status="FAILED",
        created_at__gte=last_24h,
    ).count()

    serializer = StatsSerializer(
        data={
            "successful_transactions": successful_transactions,
            "failed_transactions": failed_transactions,
        }
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.info("Stats request successful")
    return Response(serializer.data)
