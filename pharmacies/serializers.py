from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Pharmacy


class PharmacySerializer(ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"
