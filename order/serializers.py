from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.Serializer):
    ticker = serializers.CharField(max_length=200, allow_null=True, required=False)
    order_type = serializers.CharField(max_length=100, allow_null=True, required=False)
    order_price = serializers.DecimalField(max_digits=12, decimal_places=4, allow_null=True, required=False)
    order_volumn = serializers.IntegerField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(allow_null=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
