from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from .serializers import OrderSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Order


class OrderView(APIView):
    renderer_classes = (JSONRenderer,)

    @method_decorator(csrf_exempt)
    def post(self, request):
        order = request.data.get('order')

        serializer = OrderSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            order_saved = serializer.save()
        return JsonResponse({"success": "Feedback created successfully: {0} | {1} | {2} | {3}".format(
            order_saved.ticker, order_saved.order_type, order_saved.order_price, order_saved.order_volumn)}, safe=False)

    def get(self, request):
        orders = Order.objects.all()
        order_list = []
        for order in orders:
            order_dict = {}
            order_dict['id'] = order.id
            order_dict['ticker'] = order.ticker
            order_dict['order_type'] = order.order_type
            order_dict['order_price'] = order.order_price
            order_dict['order_volumn'] = order.order_volumn
            order_dict['created_at'] = str(order.created_at).split('.')[0]
            order_list.append(order_dict)
        return JsonResponse({'orders': order_list}, safe=False)
