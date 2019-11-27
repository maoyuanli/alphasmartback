from django.db import models


class Order(models.Model):
    ticker = models.CharField(max_length=200, null=True)
    order_type = models.CharField(max_length=100, null=True)
    order_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    order_volumn = models.BigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
