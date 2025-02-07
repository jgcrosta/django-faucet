from rest_framework import serializers
from web3 import Web3


class FundRequestSerializer(serializers.Serializer):
    wallet_address = serializers.CharField(
        max_length=42,
        min_length=42,
        error_messages={
            "max_length": "Ethereum address must be exactly 42 characters long.",
            "min_length": "Ethereum address must be exactly 42 characters long.",
            "required": "Ethereum address is required.",
            "blank": "Ethereum address cannot be blank.",
        },
    )

    def validate_wallet_address(self, value):
        if not Web3.is_address(value):
            raise serializers.ValidationError("Invalid Ethereum address")
        return value


class StatsSerializer(serializers.Serializer):
    successful_transactions = serializers.IntegerField()
    failed_transactions = serializers.IntegerField()
