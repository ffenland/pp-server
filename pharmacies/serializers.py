from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Pharmacy, Account


class PharmacyAccountSerializer(ModelSerializer):
    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []

    class Meta:
        model = Account
        fields = (
            "name",
            "ammount",
        )


class PharmacySerializer(ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"
