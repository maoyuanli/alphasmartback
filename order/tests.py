from django.test import TestCase

from order.views import OrderView


class ViewTests(TestCase):
    order_api = OrderView()

    def test_post(self):
        self.order_api.post(
            '/api/order',
            {
                'ticker': 'Maotion Technology (MAO)',
                'order_type': 'Limited Buy',
                'order_price': 12.55,
                'order_volumn': 1000
            },
            format='json'
        )

    def test_time(self):
        from django.utils import timezone

        now = timezone.now()
        print(now)